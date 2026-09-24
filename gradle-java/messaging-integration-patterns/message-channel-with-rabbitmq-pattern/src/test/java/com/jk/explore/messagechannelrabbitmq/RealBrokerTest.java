package com.jk.explore.messagechannelrabbitmq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What the real broker does, asked of it directly.
 *
 * <p>One broker is started for the whole class, because starting it is the slow part. Every
 * wait here is a bounded poll on something the broker can actually be asked about; there is
 * no sleep anywhere in this file, so a slow machine waits longer and a fast one does not.
 */
class RealBrokerTest {

    private static Broker broker;

    @BeforeAll
    static void startTheBroker() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        broker = new Broker();
        broker.start();
    }

    @AfterAll
    static void stopTheBroker() {
        if (broker != null) {
            broker.close();
        }
    }

    @Test
    void aMessageWaitsInTheChannelWhileNobodyIsListening() {
        try (Channel channel = broker.channel("waits-for-a-receiver").openWrittenDown()) {
            for (int i = 1; i <= 3; i++) {
                channel.send(PickOrder.of(i));
            }
            Poll.until("all three orders to be waiting", () -> channel.waiting() == 3);
            assertEquals(3, channel.waiting());
        }
    }

    @Test
    void theOrdersComeOutInTheOrderTheyWentIn() {
        List<String> picked = Collections.synchronizedList(new ArrayList<>());
        try (Channel sender = broker.channel("keeps-the-order").openWrittenDown();
             Channel receiver = broker.channel("keeps-the-order").openWrittenDown()) {
            for (int i = 1; i <= 5; i++) {
                sender.send(PickOrder.of(i));
            }
            receiver.receiveEachInto(order -> picked.add(order.orderId()));
            Poll.until("all five orders to arrive", () -> picked.size() == 5);
            assertEquals(List.of("ORD-1", "ORD-2", "ORD-3", "ORD-4", "ORD-5"), picked);
        }
    }

    @Test
    void anOrderTakenButNeverAcknowledgedGoesBackIntoTheChannel() {
        try (Channel watch = broker.channel("returns-what-is-dropped").openWrittenDown()) {
            watch.send(PickOrder.of(1));
            Poll.until("the order to be waiting", () -> watch.waiting() == 1);

            Channel firstPicker = broker.channel("returns-what-is-dropped").openWrittenDown();
            Channel.Taken firstTry = takeOne(firstPicker);
            assertEquals("ORD-1", firstTry.order().orderId());
            assertFalse(firstTry.seenBefore(), "the first delivery is not a redelivery");
            Poll.until("the broker to hand nothing else out", () -> watch.waiting() == 0);

            firstPicker.crash();
            Poll.until("the broker to put the order back", () -> watch.waiting() == 1);

            try (Channel secondPicker = broker.channel("returns-what-is-dropped").openWrittenDown()) {
                Channel.Taken secondTry = takeOne(secondPicker);
                assertEquals("ORD-1", secondTry.order().orderId());
                assertTrue(secondTry.seenBefore(), "the second delivery is marked as one seen before");
                secondPicker.sayDone(secondTry);
                Poll.until("the channel to be empty for good", () -> watch.waiting() == 0);
                assertEquals(0, watch.waiting());
            }
        }
    }

    /**
     * Two pickers share one channel, one slow and one fast. With no limit on unfinished
     * orders the broker deals them out in turn before any work is done, so the split is
     * exact. With a limit of one, the split depends on the broker's timing, so it is asserted
     * as a range: the fast picker takes most of them.
     */
    @Test
    void aLimitOfOneUnfinishedOrderLetsTheFastPickerTakeMostOfThem() {
        RabbitMessageChannelDemo.Split noLimit =
                RabbitMessageChannelDemo.shareBetweenASlowAndAFastPicker(broker, "shared-no-limit", 0);
        assertEquals(5, noLimit.slow());
        assertEquals(5, noLimit.fast());

        RabbitMessageChannelDemo.Split limitOfOne =
                RabbitMessageChannelDemo.shareBetweenASlowAndAFastPicker(broker, "shared-limit-of-one", 1);
        assertEquals(10, limitOfOne.slow() + limitOfOne.fast());
        assertTrue(limitOfOne.fast() >= 7, "the fast picker should take most: " + limitOfOne);
        assertTrue(limitOfOne.slow() <= 3, "the slow picker should take only a few: " + limitOfOne);
    }

    @Test
    void aChannelWithARoomLimitRefusesRatherThanQuietlyDropping() {
        try (Channel bounded = broker.channel("room-for-five").openWithRoomFor(5).askForReceipts()) {
            int accepted = 0;
            int refused = 0;
            for (int i = 1; i <= 8; i++) {
                if (bounded.sendAndHearBack(PickOrder.of(i))) {
                    accepted++;
                } else {
                    refused++;
                }
            }
            assertEquals(5, accepted);
            assertEquals(3, refused);
            assertEquals(5, bounded.waiting());
        }
    }

    /**
     * The broker is stopped and started again, which is the only honest way to show that a
     * channel outlives the processes around it. This test is last in the class by name on
     * purpose: it is the slow one.
     */
    @Test
    void whatIsWrittenToDiskSurvivesTheBrokerStoppingAndWhatIsNotDoesNot() {
        try (Channel kept = broker.channel("survives-a-restart").openWrittenDown();
             Channel quick = broker.channel("does-not-survive-a-restart").openWrittenDown()) {
            for (int i = 1; i <= 3; i++) {
                kept.send(PickOrder.of(i));
                quick.sendWithoutWritingDown(PickOrder.of(i));
            }
            Poll.until("both channels to hold three", () -> kept.waiting() == 3 && quick.waiting() == 3);
        }
        broker.restart();
        try (Channel kept = broker.channel("survives-a-restart");
             Channel quick = broker.channel("does-not-survive-a-restart")) {
            Poll.until("the written-down orders to come back", () -> kept.waiting() == 3);
            assertEquals(3, kept.waiting());
            assertEquals(0, quick.waiting());
        }
    }

    private static Channel.Taken takeOne(Channel channel) {
        Channel.Taken[] holder = new Channel.Taken[1];
        Poll.until("a message to be handed over", () -> (holder[0] = channel.takeWithoutSayingDone()) != null);
        return holder[0];
    }
}
