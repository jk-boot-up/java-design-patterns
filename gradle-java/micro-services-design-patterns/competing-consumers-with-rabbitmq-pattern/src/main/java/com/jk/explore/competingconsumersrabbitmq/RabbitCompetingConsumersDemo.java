package com.jk.explore.competingconsumersrabbitmq;

import java.util.HashSet;
import java.util.List;
import java.util.Set;

/**
 * Six acts against a real RabbitMQ broker, started and stopped by this program.
 *
 * <p>Several warehouse pickers share one queue of pick orders. The first act shows why more
 * than one is needed. The rest show the two settings the broker makes you choose that the
 * hand-built version never asked about: how many orders one picker may hold at once, and when
 * an order counts as done.
 */
public class RabbitCompetingConsumersDemo {

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
            one(broker);
            int hoarded = two(broker);
            three(broker);
            int[] crash = four(broker);
            five(broker);
            six(broker, hoarded, crash);
        }
    }

    /** One picker falls behind; three share the queue, and the broker decides who gets what. */
    private static void one(Broker broker) {
        System.out.println("ONE. One picker, then three.");
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-one")) {
            queue.sendOrders(1, 12);
            Picker only = Picker.oneAtATime("A", broker, queue.name(), new Stock()).stallingOnTheFirst().start();
            Poll.until("one order to be in hand and eleven waiting", () -> only.busy() && queue.waiting() == 11);
            System.out.println("  12 orders, one picker taking one at a time. being picked: 1. waiting: " + queue.waiting() + ".");
            only.close();
            Poll.until("the order to go back when the picker leaves", () -> queue.waiting() == 12);

            List<Picker> three = startPickers(broker, queue.name(), 3, true);
            Poll.until("three orders in hand and nine waiting",
                    () -> three.stream().allMatch(Picker::busy) && queue.waiting() == 9);
            System.out.println("  the same 12, three pickers on the same queue. being picked: "
                    + three.stream().filter(Picker::busy).count() + ". waiting: " + queue.waiting() + ".");
            three.forEach(Picker::release);
            Poll.until("the twelve to be picked", () -> totalPicked(three) == 12);
            three.forEach(Picker::close);
        }
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-many")) {
            List<Picker> three = startPickers(broker, queue.name(), 3, false);
            Poll.until("all three pickers to be listening", () -> queue.pickersListening() == 3);
            queue.sendOrders(1, 300);
            Poll.until("all 300 orders to be picked", () -> totalPicked(three) == 300);
            System.out.println("  300 orders, three pickers: " + totalPicked(three) + " picked, " + distinctPicked(three)
                    + " different orders. " + describeSpread(three, 300) + ".");
            System.out.println("  who got which order is the broker's choice, and it changes from run to run.");
            three.forEach(Picker::close);
        }
    }

    /** The describing words the first act prints, chosen from the real counts. */
    static String describeSpread(List<Picker> pickers, int total) {
        boolean everyoneDidSome = pickers.stream().allMatch(p -> !p.picked().isEmpty());
        boolean noneMoreThanHalf = pickers.stream().allMatch(p -> p.picked().size() * 2 <= total);
        return (everyoneDidSome ? "every picker did some" : "a picker did none")
                + (noneMoreThanHalf ? ", and none did more than half" : ", and one did more than half");
    }

    /** No limit set: the first picker to listen is handed the whole queue. */
    private static int two(Broker broker) {
        System.out.println("TWO. No limit: the first picker takes everything.");
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-no-limit")) {
            queue.sendOrders(1, 12);
            Picker slow = Picker.withNoLimit("slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start();
            Poll.until("the broker to hand the slow picker everything",
                    () -> slow.handedOver() == 12 && queue.waiting() == 0);
            Picker fast = Picker.withNoLimit("fast", broker, queue.name(), new Stock()).start();
            Poll.until("the fast picker to be listening", () -> queue.pickersListening() == 2);
            System.out.println("  12 orders waiting. a slow picker starts first, with no limit set. handed to it: "
                    + slow.handedOver() + ". waiting: " + queue.waiting() + ".");
            System.out.println("  a fast picker joins a moment later. handed to it: " + fast.handedOver()
                    + ". it stands idle while the slow one holds " + slow.holding() + ".");
            slow.release();
            Poll.until("the slow picker to work through all twelve", () -> slow.picked().size() == 12);
            System.out.println("  picked by the slow picker: " + slow.picked().size() + ". by the fast one: "
                    + fast.picked().size() + ". RabbitMQ's default is no limit.");
            int hoarded = slow.picked().size();
            fast.close();
            slow.close();
            return hoarded;
        }
    }

    /** The same slow and fast pickers, with a limit of ten and then a limit of one. */
    private static void three(Broker broker) {
        System.out.println("THREE. Prefetch: how many a picker may hold.");
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-prefetch-ten")) {
            queue.sendOrders(1, 20);
            Picker slow = Picker.holdingUpTo(10, "slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start();
            Poll.until("the slow picker to be handed ten", () -> slow.handedOver() == 10 && queue.waiting() == 10);
            Picker fast = Picker.holdingUpTo(10, "fast", broker, queue.name(), new Stock()).start();
            Poll.until("the fast picker to finish what it was handed",
                    () -> fast.picked().size() == 10 && !fast.busy() && queue.waiting() == 0);
            System.out.println("  20 orders, prefetch 10. handed to the slow picker: " + slow.handedOver()
                    + ". to the fast one: " + fast.handedOver() + ".");
            System.out.println("  the fast one picks its " + fast.picked().size() + " and stands idle. waiting: "
                    + queue.waiting() + ". still held by the slow one: " + slow.holding() + ".");
            slow.release();
            Poll.until("the slow picker to finish", () -> slow.picked().size() == 10);
            fast.close();
            slow.close();
        }
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-prefetch-one")) {
            queue.sendOrders(1, 20);
            Picker slow = Picker.oneAtATime("slow", broker, queue.name(), new Stock()).stallingOnTheFirst().start();
            Poll.until("the slow picker to be handed one", () -> slow.busy() && queue.waiting() == 19);
            Picker fast = Picker.oneAtATime("fast", broker, queue.name(), new Stock()).start();
            Poll.until("the fast picker to pick the rest", () -> fast.picked().size() == 19 && queue.waiting() == 0);
            System.out.println("  the same 20, prefetch 1. the slow picker holds " + slow.holding()
                    + ". the fast one picks the other " + fast.picked().size() + ".");
            slow.release();
            Poll.until("the slow picker to finish", () -> slow.picked().size() == 1);
            fast.close();
            slow.close();
        }
    }

    /**
     * A picker holding five dies half-way through the third. Returns {orders, deliveries,
     * times ORD-3 was reserved} for the bill.
     */
    private static int[] four(Broker broker) {
        System.out.println("FOUR. A picker dies mid-work.");
        Stock stock = new Stock();
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-crash")) {
            queue.sendOrders(1, 5);
            Picker first = Picker.holdingUpTo(5, "A", broker, queue.name(), stock)
                    .stallingOn(order -> order.orderId().equals("ORD-3")).start();
            Poll.until("picker A to be half-way through ORD-3",
                    () -> first.handedOver() == 5 && first.picked().size() == 2 && "ORD-3".equals(first.inHand()));
            System.out.println("  prefetch 5. picker A is handed " + first.handedOver() + ", picks "
                    + String.join(" and ", first.picked()) + ", reserves the stock for " + first.inHand()
                    + ", and crashes before saying it is done.");
            first.crash();
            Poll.until("the broker to notice picker A has gone", () -> queue.pickersListening() == 0);
            Poll.until("the broker to put back what A was holding", () -> queue.waiting() == 3);
            System.out.println("  the broker puts back every order it handed to A and was not told was done. waiting again: "
                    + queue.waiting() + ".");

            try (Picker second = Picker.holdingUpTo(5, "B", broker, queue.name(), stock).start()) {
                Poll.until("picker B to pick the three", () -> second.picked().size() == 3 && queue.waiting() == 0);
                System.out.println("  picker B is handed " + second.handedOrders() + ", marked as seen before: "
                        + second.markedSeenBefore() + " of " + second.handedOver() + ". only ORD-3 had been started.");
                int deliveries = first.handedOver() + second.handedOver();
                System.out.println("  deliveries: " + deliveries + " for 5 orders. stock reserved for ORD-3: "
                        + stock.timesReserved("ORD-3") + " times. for ORD-4: " + stock.timesReserved("ORD-4") + ".");
                return new int[]{5, deliveries, stock.timesReserved("ORD-3")};
            }
        }
    }

    /** The same crash, with a picker that told the broker not to wait for done. */
    private static void five(Broker broker) {
        System.out.println("FIVE. No saying done.");
        Stock stock = new Stock();
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-auto")) {
            queue.sendOrders(1, 5);
            Picker careless = Picker.forgettingOnHandover("A", broker, queue.name(), stock)
                    .stallingOn(order -> order.orderId().equals("ORD-3")).start();
            Poll.until("picker A to be half-way through ORD-3",
                    () -> careless.handedOver() == 5 && careless.picked().size() == 2 && "ORD-3".equals(careless.inHand()));
            System.out.println("  picker A tells the broker to count each order as done on handover. handed: "
                    + careless.handedOver() + ". waiting: " + queue.waiting() + ".");
            careless.crash();
            Poll.until("the broker to notice picker A has gone", () -> queue.pickersListening() == 0);
            int picked = careless.picked().size();
            int lost = careless.handedOver() - picked;
            System.out.println("  the same crash on ORD-3. picked: " + picked + ". waiting again: " + queue.waiting()
                    + ". lost: " + lost + ". nobody will be handed ORD-3, ORD-4 or ORD-5 again.");
        }
    }

    /** What sharing a queue between pickers costs, with one more thing the broker cannot know. */
    private static void six(Broker broker, int hoarded, int[] crash) {
        System.out.println("SIX. The bill.");
        try (OrderQueue queue = new OrderQueue(broker, "pick-orders-poison")) {
            queue.send(PickOrder.of(13));
            int deliveries = 0;
            int seenBefore = 0;
            for (String name : new String[]{"A", "B", "C"}) {
                Picker picker = Picker.oneAtATime(name, broker, queue.name(), new Stock()).stallingOnTheFirst().start();
                Poll.until("picker " + name + " to take ORD-13", picker::busy);
                deliveries += picker.handedOver();
                seenBefore += picker.markedSeenBefore();
                picker.crash();
                Poll.until("the broker to notice picker " + name + " has gone", () -> queue.pickersListening() == 0);
                Poll.until("ORD-13 to be put back", () -> queue.waiting() == 1);
            }
            System.out.println("  ORD-13 crashes every picker that takes it. 3 pickers, delivered " + deliveries
                    + " times, marked seen before on " + seenBefore + ", picked 0 times. waiting again: " + queue.waiting() + ".");
            System.out.println("  the broker cannot tell a poison order from a slow one. it will hand it out for ever unless told a limit.");
        }
        System.out.println("  and every picker must be safe to run twice: act four made " + crash[1] + " deliveries for "
                + crash[0] + " orders, and reserved the stock for ORD-3 " + crash[2] + " times.");
        System.out.println("  and prefetch is a number somebody has to choose. left unset, one picker took " + hoarded
                + " of 12 while another stood idle.");
    }

    private static List<Picker> startPickers(Broker broker, String queue, int count, boolean stalling) {
        String[] names = {"A", "B", "C"};
        List<Picker> pickers = new java.util.ArrayList<>();
        for (int i = 0; i < count; i++) {
            Picker p = Picker.oneAtATime(names[i], broker, queue, new Stock());
            if (stalling) {
                p.stallingOnTheFirst();
            }
            pickers.add(p.start());
        }
        return pickers;
    }

    private static int totalPicked(List<Picker> pickers) {
        return pickers.stream().mapToInt(p -> p.picked().size()).sum();
    }

    private static int distinctPicked(List<Picker> pickers) {
        Set<String> all = new HashSet<>();
        pickers.forEach(p -> all.addAll(p.picked()));
        return all.size();
    }
}
