package com.jk.explore.actorpattern;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;

public class ActorDemo {

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() throws Exception {
        System.out.println("ONE. State that many threads can reach.");
        SharedStock shared = new SharedStock("MUG-BLUE", 10);
        CountDownLatch bothRead = new CountDownLatch(2);
        Runnable rendezvous = () -> {
            bothRead.countDown();
            try {
                bothRead.await();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        };
        Thread a = new Thread(() -> shared.reserve("MUG-BLUE", 3, rendezvous));
        Thread b = new Thread(() -> shared.reserve("MUG-BLUE", 4, rendezvous));
        a.start();
        b.start();
        a.join();
        b.join();
        System.out.println("  10 in stock. two orders, for 3 and for 4, read the stock at the same moment. it should be 3 left. it is 3 left: " + (shared.stockOf("MUG-BLUE") == 3) + ". one of the two reservations was lost.");
        System.out.println("  every method looked correct. the state was open to anyone.");
    }

    private static void two() throws Exception {
        System.out.println("TWO. State that one actor owns.");
        try (InventoryActor inventory = new InventoryActor(Map.of("MUG-BLUE", 4000))) {
            inventory.start();
            List<Thread> senders = new ArrayList<>();
            for (int i = 0; i < 4; i++) {
                Thread t = new Thread(() -> {
                    for (int n = 0; n < 1000; n++) {
                        inventory.tell(new Messages.Reserve("MUG-BLUE", 1));
                    }
                });
                senders.add(t);
                t.start();
            }
            for (Thread t : senders) {
                t.join();
            }
            long deadline = System.nanoTime() + 10_000_000_000L;
            while (inventory.handled() < 4000 && System.nanoTime() < deadline) {
                Thread.onSpinWait();
            }
            System.out.println("  4 threads each send 1000 reservations of 1 mug to an inventory of 4000. stock left: " + inventory.ask(new Messages.StockOf("MUG-BLUE")).get(5, TimeUnit.SECONDS) + ".");
            System.out.println("  no lock in the inventory. the actor handled one message at a time, so none was lost.");
        }
    }

    private static void three() throws Exception {
        System.out.println("THREE. Ask, and be answered by a message.");
        try (InventoryActor inventory = new InventoryActor(Map.of("MUG-BLUE", 5))) {
            inventory.start();
            System.out.println("  reserve 3: " + inventory.ask(new Messages.Reserve("MUG-BLUE", 3)).get(5, TimeUnit.SECONDS) + ".");
            System.out.println("  reserve 3 more: " + inventory.ask(new Messages.Reserve("MUG-BLUE", 3)).get(5, TimeUnit.SECONDS) + ".");
            System.out.println("  the answer is a message too, and it can be a refusal. no exception crossed between the two.");
        }
    }

    private static void four() throws Exception {
        System.out.println("FOUR. Nobody can reach in.");
        boolean hasGetter = false;
        for (var m : InventoryActor.class.getDeclaredMethods()) {
            if (java.lang.reflect.Modifier.isPublic(m.getModifiers()) && m.getName().toLowerCase().contains("stock")) {
                hasGetter = true;
            }
        }
        System.out.println("  the inventory actor has a public method that returns its stock: " + hasGetter + ".");
        try (InventoryActor inventory = new InventoryActor(Map.of("MUG-BLUE", 5))) {
            inventory.start();
            Object seen = inventory.ask(new Messages.StockOf("MUG-BLUE")).get(5, TimeUnit.SECONDS);
            System.out.println("  the only way to learn the stock is to ask, and the answer is a copy: " + seen + ".");
        }
    }

    private static void five() throws Exception {
        System.out.println("FIVE. Let it crash.");
        try (InventoryActor inventory = new InventoryActor(Map.of("MUG-BLUE", 5))) {
            inventory.start();
            inventory.ask(new Messages.Reserve("MUG-BLUE", 2)).get(5, TimeUnit.SECONDS);
            System.out.println("  after reserving 2, stock is: " + inventory.ask(new Messages.StockOf("MUG-BLUE")).get(5, TimeUnit.SECONDS) + ".");
            try {
                inventory.ask(new Messages.Poison()).get(5, TimeUnit.SECONDS);
            } catch (ExecutionException e) {
                System.out.println("  a message the actor cannot handle: the sender is told, '" + e.getCause().getMessage() + "'.");
            }
            System.out.println("  the actor was restarted: restarts " + inventory.restarts() + ". the next message is handled: " + inventory.ask(new Messages.Reserve("MUG-BLUE", 1)).get(5, TimeUnit.SECONDS) + ".");
            System.out.println("  one bad message did not stop the actor, or the others.");
            System.out.println("  the stock after the restart: " + inventory.ask(new Messages.StockOf("MUG-BLUE")).get(5, TimeUnit.SECONDS) + " (it started at 5, and was back to 5 before that last reservation).");
        }
    }

    /** Two actors that each ask the other and wait for the answer before replying to anything. */
    static String cycle() throws Exception {
        class Waiter extends Actor {
            volatile Waiter other;
            final Gate started = new Gate();

            Waiter(String name) {
                super(name);
            }

            @Override
            protected Object receive(Object message) {
                try {
                    return other.ask("hello").get();
                } catch (InterruptedException | ExecutionException e) {
                    Thread.currentThread().interrupt();
                    return null;
                }
            }

            @Override
            protected void restart() {
            }
        }
        Waiter a = new Waiter("a");
        Waiter b = new Waiter("b");
        a.other = b;
        b.other = a;
        try {
            a.start();
            b.start();
            var fa = a.ask("go");
            var fb = b.ask("go");
            try {
                fa.get(300, TimeUnit.MILLISECONDS);
                fb.get(300, TimeUnit.MILLISECONDS);
                return "answered";
            } catch (TimeoutException e) {
                return "no answer";
            }
        } finally {
            a.close();
            b.close();
        }
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill.");
        System.out.println("  two actors each ask the other, and wait for the answer before doing anything else: " + cycle() + ".");
        System.out.println("  no locks, and still a deadlock: each is waiting for a message the other can never send.");
        System.out.println("  and a restart forgets: an actor's state is gone unless it was written somewhere else. messages are copied, mailboxes can grow, and finding where a message went takes tools.");
    }
}
