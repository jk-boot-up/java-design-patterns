package com.jk.explore.competingconsumersrabbitmq;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

/**
 * What the real broker does with several pickers on one queue, asked of it directly.
 *
 * <p>One broker is started for the whole class, because starting it is the slow part, and each
 * test uses its own queue. Every wait is a bounded poll on something the broker or a picker can
 * actually be asked about; there is no sleep anywhere in this file.
 *
 * <p>Most counts here are exact, because the tests hold a picker still until the count has been
 * read. One is not: how the broker spreads orders between equal pickers is its own scheduling,
 * and that test asserts a range.
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
    void theBrokerListensOnAPortTestcontainersPickedAtRandom() {
        String address = broker.address();
        int port = Integer.parseInt(address.substring(address.lastIndexOf(':') + 1));
        // Inside the container the broker is on RabbitMQ's usual 5672. On this machine it is on
        // whatever free port Testcontainers was given, so nothing else on 5672 can get in the way.
        assertTrue(port > 0 && port != 5672, address);
    }

    @Test
    void withNoLimitTheFirstPickerIsHandedTheWholeQueue() {
        try (OrderQueue queue = new OrderQueue(broker, "test-no-limit")) {
            queue.sendOrders(1, 12);
            try (Picker slow = Picker.withNoLimit("slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start()) {
                Poll.until("everything to be handed to the slow picker", () -> slow.handedOver() == 12 && queue.waiting() == 0);
                try (Picker fast = Picker.withNoLimit("fast", broker, queue.name(), new Stock()).start()) {
                    Poll.until("the fast picker to be listening", () -> queue.pickersListening() == 2);
                    slow.release();
                    Poll.until("the slow picker to finish", () -> slow.picked().size() == 12);
                    assertEquals(0, fast.handedOver());
                    assertEquals(0, fast.picked().size());
                }
            }
        }
    }

    @Test
    void prefetchTenHandsTenToEachPickerHoweverSlowOneOfThemIs() {
        try (OrderQueue queue = new OrderQueue(broker, "test-prefetch-ten")) {
            queue.sendOrders(1, 20);
            try (Picker slow = Picker.holdingUpTo(10, "slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start()) {
                Poll.until("ten to be handed to the slow picker", () -> slow.handedOver() == 10 && queue.waiting() == 10);
                try (Picker fast = Picker.holdingUpTo(10, "fast", broker, queue.name(), new Stock()).start()) {
                    Poll.until("the fast picker to finish its ten", () -> fast.picked().size() == 10 && queue.waiting() == 0);
                    assertEquals(10, fast.handedOver());
                    assertEquals(10, slow.holding());
                    slow.release();
                    Poll.until("the slow picker to finish", () -> slow.picked().size() == 10);
                }
            }
        }
    }

    @Test
    void prefetchOneLetsTheFastPickerTakeEverythingTheSlowOneIsNotHolding() {
        try (OrderQueue queue = new OrderQueue(broker, "test-prefetch-one")) {
            queue.sendOrders(1, 20);
            try (Picker slow = Picker.oneAtATime("slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start()) {
                Poll.until("one to be handed to the slow picker", () -> slow.busy() && queue.waiting() == 19);
                try (Picker fast = Picker.oneAtATime("fast", broker, queue.name(), new Stock()).start()) {
                    Poll.until("the fast picker to pick nineteen", () -> fast.picked().size() == 19 && queue.waiting() == 0);
                    assertEquals(1, slow.holding());
                    slow.release();
                    Poll.until("the slow picker to finish", () -> slow.picked().size() == 1);
                }
            }
        }
    }

    @Test
    void aPickerThatDiesMidWorkHandsBackEverythingItHeldAllMarkedSeenBefore() {
        Stock stock = new Stock();
        try (OrderQueue queue = new OrderQueue(broker, "test-crash")) {
            queue.sendOrders(1, 5);
            Picker first = Picker.holdingUpTo(5, "A", broker, queue.name(), stock)
                    .stallingOn(order -> order.orderId().equals("ORD-3")).start();
            Poll.until("A to be half-way through ORD-3",
                    () -> first.handedOver() == 5 && first.picked().size() == 2 && "ORD-3".equals(first.inHand()));
            first.crash();
            Poll.until("the broker to notice", () -> queue.pickersListening() == 0);
            Poll.until("the three held orders to come back", () -> queue.waiting() == 3);
            try (Picker second = Picker.holdingUpTo(5, "B", broker, queue.name(), stock).start()) {
                Poll.until("B to pick them", () -> second.picked().size() == 3);
                assertEquals(Set.of("ORD-3", "ORD-4", "ORD-5"), new HashSet<>(second.handedOrders()));
                assertEquals(3, second.markedSeenBefore());
                assertEquals(2, stock.timesReserved("ORD-3"));
                assertEquals(1, stock.timesReserved("ORD-4"));
                assertEquals(0, queue.waiting());
            }
        }
    }

    @Test
    void withAutomaticAcknowledgementACrashLosesWhatThePickerHeld() {
        try (OrderQueue queue = new OrderQueue(broker, "test-auto")) {
            queue.sendOrders(1, 5);
            Picker careless = Picker.forgettingOnHandover("A", broker, queue.name(), new Stock())
                    .stallingOn(order -> order.orderId().equals("ORD-3")).start();
            Poll.until("A to be half-way through ORD-3",
                    () -> careless.handedOver() == 5 && careless.picked().size() == 2 && "ORD-3".equals(careless.inHand()));
            assertEquals(0, queue.waiting(), "the broker forgot each order as it handed it over");
            careless.crash();
            Poll.until("the broker to notice", () -> queue.pickersListening() == 0);
            assertEquals(0, queue.waiting());
        }
    }

    @Test
    void aPoisonOrderGoesRoundForeverAndTheMarkSaysOnlySeenBefore() {
        try (OrderQueue queue = new OrderQueue(broker, "test-poison")) {
            queue.send(PickOrder.of(13));
            int deliveries = 0;
            int seenBefore = 0;
            for (int i = 0; i < 3; i++) {
                Picker picker = Picker.oneAtATime("p" + i, broker, queue.name(), new Stock()).stallingOnTheFirst().start();
                Poll.until("the picker to take ORD-13", picker::busy);
                deliveries += picker.handedOver();
                seenBefore += picker.markedSeenBefore();
                picker.crash();
                Poll.until("the broker to notice", () -> queue.pickersListening() == 0);
                Poll.until("ORD-13 to be back", () -> queue.waiting() == 1);
            }
            assertEquals(3, deliveries);
            assertEquals(2, seenBefore);
        }
    }

    /**
     * The one count this class cannot pin to a number. Three equal pickers each taking one at a
     * time share 300 orders, and how many each gets is the broker's own scheduling. So the test
     * asserts what the demo prints in words: all 300 picked once each, every picker did some,
     * and none did more than half.
     */
    @Test
    void theSpreadAcrossEqualPickersIsTheBrokersChoiceSoItIsARange() {
        try (OrderQueue queue = new OrderQueue(broker, "test-spread")) {
            List<Picker> pickers = new ArrayList<>();
            for (String name : new String[]{"A", "B", "C"}) {
                pickers.add(Picker.oneAtATime(name, broker, queue.name(), new Stock()).start());
            }
            try {
                Poll.until("all three to be listening", () -> queue.pickersListening() == 3);
                queue.sendOrders(1, 300);
                Poll.until("all 300 to be picked", () -> pickers.stream().mapToInt(p -> p.picked().size()).sum() == 300);
                Set<String> distinct = new HashSet<>();
                for (Picker p : pickers) {
                    distinct.addAll(p.picked());
                    int share = p.picked().size();
                    System.out.println("spread: picker " + p.name() + " picked " + share);
                    assertTrue(share >= 1 && share <= 150, "picker " + p.name() + " picked " + share);
                }
                assertEquals(300, distinct.size());
                assertEquals("every picker did some, and none did more than half",
                        RabbitCompetingConsumersDemo.describeSpread(pickers, 300));
            } finally {
                pickers.forEach(Picker::close);
            }
        }
    }
}
