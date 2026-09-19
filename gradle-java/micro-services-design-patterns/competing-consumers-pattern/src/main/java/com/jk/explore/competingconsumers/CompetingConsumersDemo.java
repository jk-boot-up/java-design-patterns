package com.jk.explore.competingconsumers;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.Semaphore;
import java.util.concurrent.atomic.AtomicInteger;

public class CompetingConsumersDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    /** Publishes six jobs, each of which holds its consumer until the gate opens, and reports what is in flight. */
    static int[] heldJobs(int consumers) {
        Broker broker = new Broker();
        Gate gate = new Gate();
        for (int i = 1; i <= 6; i++) {
            broker.publish(i, "order-" + i);
        }
        try (ConsumerPool pool = new ConsumerPool(broker, consumers, (who, d) -> gate.await())) {
            ConsumerPool.until(() -> broker.inFlight() == Math.min(consumers, 6));
            int[] answer = {broker.inFlight(), broker.waiting()};
            gate.open();
            ConsumerPool.until(() -> broker.acknowledged() == 6);
            return answer;
        }
    }

    private static void one() {
        System.out.println("ONE. One consumer, then three.");
        int[] one = heldJobs(1);
        int[] three = heldJobs(3);
        System.out.println("  six slow jobs, one consumer: " + one[0] + " in progress, " + one[1] + " waiting.");
        System.out.println("  six slow jobs, three consumers: " + three[0] + " in progress, " + three[1] + " waiting.");
        System.out.println("  the consumers do not talk to each other. they take from the same queue.");
    }

    private static void two() {
        System.out.println("TWO. Each message is handled once.");
        Broker broker = new Broker();
        Set<Integer> seen = ConcurrentHashMap.newKeySet();
        AtomicInteger total = new AtomicInteger();
        for (int i = 1; i <= 1000; i++) {
            broker.publish(i, "order-" + i);
        }
        try (ConsumerPool pool = new ConsumerPool(broker, 4, (who, d) -> {
            seen.add(d.id());
            total.incrementAndGet();
        })) {
            ConsumerPool.until(() -> broker.acknowledged() == 1000);
        }
        System.out.println("  1000 orders, 4 consumers: handled " + total.get() + " times in all, " + seen.size() + " different orders.");
        System.out.println("  none twice, none missed. which consumer got which order is not defined, and does not matter.");
    }

    private static void three() {
        System.out.println("THREE. The order is not kept.");
        Broker broker = new Broker();
        Gate first = new Gate();
        List<Integer> finished = Collections.synchronizedList(new ArrayList<>());
        for (int i = 1; i <= 3; i++) {
            broker.publish(i, "order-" + i);
        }
        try (ConsumerPool pool = new ConsumerPool(broker, 2, (who, d) -> {
            if (d.id() == 1) {
                first.await();
            }
            finished.add(d.id());
        })) {
            ConsumerPool.until(() -> finished.size() == 2);
            first.open();
            ConsumerPool.until(() -> broker.acknowledged() == 3);
        }
        System.out.println("  orders 1, 2 and 3 published in that order. order 1's consumer is slow. they finished: " + finished + ".");
        System.out.println("  if order 2 depends on order 1, this is a bug. competing consumers give up ordering.");
    }

    private static void four() {
        System.out.println("FOUR. A consumer fails, another takes over.");
        Broker broker = new Broker();
        List<String> log = Collections.synchronizedList(new ArrayList<>());
        broker.publish(1, "order-1");
        try (ConsumerPool pool = new ConsumerPool(broker, 2, (who, d) -> {
            if (d.attempt() == 1) {
                log.add("attempt 1 fails");
                throw new IllegalStateException("consumer crashed");
            }
            log.add("attempt " + d.attempt() + " succeeds");
        })) {
            ConsumerPool.until(() -> broker.acknowledged() == 1);
        }
        System.out.println("  " + log + ".");
        System.out.println("  the message was given back and handled again. it was not lost.");
    }

    private static void five() {
        System.out.println("FIVE. At least once, so a duplicate.");
        List<String> charges = Collections.synchronizedList(new ArrayList<>());
        Broker broker = new Broker();
        broker.publish(1, "charge order-1");
        try (ConsumerPool pool = new ConsumerPool(broker, 2, (who, d) -> {
            charges.add(d.body());
            if (d.attempt() == 1) {
                throw new IllegalStateException("crashed after charging, before saying so");
            }
        })) {
            ConsumerPool.until(() -> broker.acknowledged() == 1);
        }
        System.out.println("  a consumer charges the card and then crashes before it can say it finished. charges made: " + charges.size() + ".");
        List<String> safeCharges = Collections.synchronizedList(new ArrayList<>());
        Set<Integer> done = ConcurrentHashMap.newKeySet();
        Broker broker2 = new Broker();
        broker2.publish(1, "charge order-1");
        try (ConsumerPool pool = new ConsumerPool(broker2, 2, (who, d) -> {
            if (done.add(d.id())) {
                safeCharges.add(d.body());
            }
            if (d.attempt() == 1) {
                throw new IllegalStateException("crashed after charging, before saying so");
            }
        })) {
            ConsumerPool.until(() -> broker2.acknowledged() == 1);
        }
        System.out.println("  the same crash, with a consumer that remembers what it has done: charges made: " + safeCharges.size() + ".");
    }

    /** Six consumers, six jobs, and a database that lets only two in at once. Returns {inside, waiting for a permit}. */
    static int[] sharedDatabase() {
        Semaphore database = new Semaphore(2);
        Gate gate = new Gate();
        Broker broker = new Broker();
        for (int i = 1; i <= 6; i++) {
            broker.publish(i, "order-" + i);
        }
        try (ConsumerPool pool = new ConsumerPool(broker, 6, (who, d) -> {
            try {
                database.acquire();
                try {
                    gate.await();
                } finally {
                    database.release();
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        })) {
            ConsumerPool.until(() -> database.availablePermits() == 0 && database.getQueueLength() == 4);
            int[] answer = {2 - database.availablePermits(), database.getQueueLength()};
            gate.open();
            ConsumerPool.until(() -> broker.acknowledged() == 6);
            return answer;
        }
    }

    private static void six() {
        System.out.println("SIX. The bill: more consumers, the same downstream.");
        int[] state = sharedDatabase();
        System.out.println("  6 consumers share a database that lets 2 in at a time. inside it: " + state[0] + ". waiting for a place: " + state[1] + ".");
        System.out.println("  four of the six are doing nothing useful. adding consumers only helps while the shared thing has room.");
    }
}
