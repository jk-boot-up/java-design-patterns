package com.jk.explore.messagechannelrabbitmq;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

/**
 * Six acts against a real RabbitMQ broker, started and stopped by this program.
 *
 * <p>The shop and the warehouse are two separate systems. The first act calls one from the
 * other and shows what that costs. The rest put a channel between them and show what the
 * broker does that a queue inside one program cannot.
 */
public class RabbitMessageChannelDemo {

    public static void main(String[] args) {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                System.out.println(Broker.WOULD_NOT_START_ADVICE);
                return;
            }
            one();
            two(broker);
            three(broker);
            four(broker);
            five(broker);
            six(broker);
        }
    }

    /** The shop calls the warehouse and waits for an answer. The warehouse is away. */
    private static void one() {
        System.out.println("ONE. Checkout calls the warehouse.");
        Warehouse warehouse = new Warehouse();
        warehouse.goDown();
        int failed = 0;
        for (int i = 1; i <= 3; i++) {
            try {
                warehouse.pick(PickOrder.of(i));
            } catch (IllegalStateException e) {
                failed++;
            }
        }
        System.out.println("  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: " + failed + ".");
        System.out.println("  the shop cannot sell while another system is away, though selling does not need it to answer yet.");
    }

    /** A real broker between them. Checkout puts orders in and returns. */
    private static void two(Broker broker) {
        System.out.println("TWO. A real channel between them.");
        // The broker hands messages over on its own thread, so the list is a synchronised one.
        List<String> picked = Collections.synchronizedList(new ArrayList<>());
        try (Channel checkout = broker.channel("pick-orders").openWrittenDown();
             Channel warehouse = broker.channel("pick-orders").openWrittenDown()) {
            warehouse.receiveEachInto(order -> picked.add(order.orderId()));
            for (int i = 1; i <= 3; i++) {
                checkout.send(PickOrder.of(i));
            }
            System.out.println("  a RabbitMQ broker is running in a container. checkout sends 3 pick orders and carries on.");
            Poll.until("the warehouse to be handed all three orders", () -> picked.size() == 3);
            Poll.until("the channel to be empty", () -> checkout.waiting() == 0);
            System.out.println("  the warehouse is listening and takes them, each once: " + picked + ". left waiting: " + checkout.waiting() + ".");
        }
    }

    /** Nobody is listening. The broker holds the messages until somebody is. */
    private static void three(Broker broker) {
        System.out.println("THREE. Nobody is listening yet.");
        Warehouse warehouse = new Warehouse();
        warehouse.goDown();
        try (Channel checkout = broker.channel("pick-orders-waiting").openWrittenDown()) {
            for (int i = 1; i <= 3; i++) {
                checkout.send(PickOrder.of(i));
            }
            Poll.until("the broker to have all three orders", () -> checkout.waiting() == 3);
            System.out.println("  the warehouse is not running, so no receiver exists. checkout sends 3, and none fail. the broker is holding: " + checkout.waiting() + ".");
            warehouse.comeBack();
            try (Channel late = broker.channel("pick-orders-waiting").openWrittenDown()) {
                late.receiveEachInto(warehouse::pick);
                Poll.until("the warehouse to work through the backlog", () -> warehouse.picked().size() == 3);
                System.out.println("  the warehouse starts up afterwards and works through them, in order: " + warehouse.picked() + ".");
            }
        }
    }

    /** A receiver that takes a message and dies before saying it is done. */
    private static void four(Broker broker) {
        System.out.println("FOUR. Saying done.");
        try (Channel watch = broker.channel("pick-orders-in-progress").openWrittenDown()) {
            watch.send(PickOrder.of(1));
            Poll.until("the order to be waiting", () -> watch.waiting() == 1);

            int deliveries = 0;
            int picked = 0;

            Channel firstPicker = broker.channel("pick-orders-in-progress").openWrittenDown();
            Channel.Taken firstTry = take(firstPicker);
            deliveries++;
            firstPicker.crash();
            Poll.until("the broker to put the order back", () -> watch.waiting() == 1);
            System.out.println("  a picker takes " + firstTry.order().orderId() + " and crashes before saying it is done. the broker puts it back. waiting again: " + watch.waiting() + ".");

            try (Channel secondPicker = broker.channel("pick-orders-in-progress").openWrittenDown()) {
                Channel.Taken secondTry = take(secondPicker);
                deliveries++;
                secondPicker.sayDone(secondTry);
                picked++;
                Poll.until("the channel to be empty", () -> watch.waiting() == 0);
                System.out.println("  a second picker is handed the same " + secondTry.order().orderId() + ", marked as seen before: " + secondTry.seenBefore() + ", and says done. deliveries: " + deliveries + ", orders picked: " + picked + ", waiting: " + watch.waiting() + ".");
            }
        }

        System.out.println("  two pickers share one channel, one slow and one fast. checkout sends " + SHARED_ORDERS + " orders.");
        Split noLimit = shareBetweenASlowAndAFastPicker(broker, "pick-orders-shared", 0);
        System.out.println("  with no limit on unfinished orders, the broker hands them all out at once, in turn: slow picker " + noLimit.slow() + ", fast picker " + noLimit.fast() + ". the fast one finishes and stands idle while the slow one works through its pile.");
        Split limitOfOne = shareBetweenASlowAndAFastPicker(broker, "pick-orders-shared-one-at-a-time", 1);
        System.out.println("  with a limit of 1 unfinished order each, the broker waits for a picker to say done before handing it another: " + limitOfOne.describe() + ".");
    }

    /** How many orders each picker was handed, when two of them share one channel. */
    record Split(int slow, int fast) {

        /** The spread depends on the broker's timing, so it is described, never counted out. */
        String describe() {
            return fast > slow ? "the fast picker took most of them" : "the slow picker kept up, which it should not have";
        }
    }

    static final int SHARED_ORDERS = 10;

    /**
     * Two pickers, one slow and one fast, listen on the same channel, and checkout sends ten
     * orders. The limit is how many unfinished orders the broker may hand one picker before it
     * waits for that picker to say done; RabbitMQ calls it prefetch, and 0 means no limit.
     */
    static Split shareBetweenASlowAndAFastPicker(Broker broker, String queue, int limit) {
        Picker slow = Picker.slow();
        Picker fast = Picker.fast();
        try (Channel checkout = broker.channel(queue).openWrittenDown();
             Channel slowPicker = broker.channel(queue).openWrittenDown().handAtMost(limit);
             Channel fastPicker = broker.channel(queue).openWrittenDown().handAtMost(limit)) {
            slowPicker.receiveEachInto(slow::pick);
            fastPicker.receiveEachInto(fast::pick);
            for (int i = 1; i <= SHARED_ORDERS; i++) {
                checkout.send(PickOrder.of(i));
            }
            Poll.until("both pickers to finish every order", () -> slow.count() + fast.count() == SHARED_ORDERS);
            return new Split(slow.count(), fast.count());
        }
    }

    private static Channel.Taken take(Channel channel) {
        Channel.Taken[] holder = new Channel.Taken[1];
        Poll.until("a message to be handed over", () -> (holder[0] = channel.takeWithoutSayingDone()) != null);
        return holder[0];
    }

    /** What a restart of the broker keeps, and what it throws away. */
    private static void five(Broker broker) {
        System.out.println("FIVE. Written to disk, or only held in memory.");
        try (Channel kept = broker.channel("pick-orders-kept").openWrittenDown();
             Channel quick = broker.channel("pick-orders-quick").openWrittenDown()) {
            for (int i = 1; i <= 3; i++) {
                kept.send(PickOrder.of(i));
                quick.sendWithoutWritingDown(PickOrder.of(i));
            }
            Poll.until("both channels to hold three", () -> kept.waiting() == 3 && quick.waiting() == 3);
            System.out.println("  two channels hold " + kept.waiting() + " orders each. the broker is asked to write one channel's messages to disk and to hold the other's in memory only.");
        }
        broker.restart();
        try (Channel kept = broker.channel("pick-orders-kept");
             Channel quick = broker.channel("pick-orders-quick")) {
            Poll.until("the written-down orders to come back", () -> kept.waiting() == 3);
            System.out.println("  the broker program is stopped and started again. written to disk: " + kept.waiting() + " orders still waiting. held in memory only: " + quick.waiting() + ".");
            System.out.println("  a channel that outlives the sender, the receiver and the broker itself is the whole reason to pay for a broker.");
        }
    }

    /** What the channel costs. */
    private static void six(Broker broker) {
        System.out.println("SIX. The bill.");
        try (Channel bounded = broker.channel("pick-orders-bounded").openWithRoomFor(5).askForReceipts()) {
            int accepted = 0;
            int refused = 0;
            for (int i = 1; i <= 8; i++) {
                if (bounded.sendAndHearBack(PickOrder.of(i))) {
                    accepted++;
                } else {
                    refused++;
                }
            }
            System.out.println("  the warehouse stays down and a channel with room for 5 is given 8: " + accepted + " accepted, " + refused + " refused. a channel must have a limit, and somebody must decide what to do at it.");
        }
        System.out.println("  and the sender no longer learns whether the warehouse picked the order. it learns only that the broker took the message.");
        System.out.println("  and a broker is a third system to run, secure, upgrade and watch: this demo needed 1 container for 1 shop and 1 warehouse.");
    }
}
