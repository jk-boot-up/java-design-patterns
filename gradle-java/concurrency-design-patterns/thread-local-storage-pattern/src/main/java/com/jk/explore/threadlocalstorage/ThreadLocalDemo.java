package com.jk.explore.threadlocalstorage;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class ThreadLocalDemo {

    // The four layers of a request, each of which has to be handed the customer just so the last can log it.
    static void checkoutExplicit(Audit a, String customer) {
        priceExplicit(a, customer);
    }

    static void priceExplicit(Audit a, String customer) {
        stockExplicit(a, customer);
    }

    static void stockExplicit(Audit a, String customer) {
        a.recordExplicit(customer, "reserved stock");
    }

    static void checkout(Audit a) {
        price(a);
    }

    static void price(Audit a) {
        stock(a);
    }

    static void stock(Audit a) {
        a.record("reserved stock");
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Hand it down.");
        Audit audit = new Audit();
        checkoutExplicit(audit, "ada");
        System.out.println("  three methods each take a customer parameter that they never use, so that the last can log it: " + audit.lines() + ".");
        System.out.println("  every new layer, and every new caller, has to pass it on.");
    }

    private static void two() {
        System.out.println("TWO. A value that belongs to the thread.");
        Audit audit = new Audit();
        RequestContext.with("ada", () -> {
            checkout(audit);
            return null;
        });
        System.out.println("  the customer is set once, at the door. checkout, price and stock take no customer: " + audit.lines() + ".");
        System.out.println("  after the request the context is cleared: " + RequestContext.customer() + ".");
    }

    private static void three() throws Exception {
        System.out.println("THREE. Each thread has its own.");
        Audit audit = new Audit();
        CountDownLatch bothSet = new CountDownLatch(2);
        List<Thread> threads = new ArrayList<>();
        for (String who : List.of("ada", "ben")) {
            Thread t = new Thread(() -> RequestContext.with(who, () -> {
                bothSet.countDown();
                try {
                    bothSet.await();
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                }
                checkout(audit);
                return null;
            }));
            threads.add(t);
            t.start();
        }
        for (Thread t : threads) {
            t.join();
        }
        List<String> lines = audit.lines();
        Collections.sort(lines);
        System.out.println("  two customers at the same moment, both contexts set before either reads: " + lines + ".");
        System.out.println("  neither saw the other's, though both used the same code and the same static field.");
    }

    /** Runs two requests one after another on the same pool thread. The second sets no customer. */
    static List<String> reusedThread(boolean clearAfterwards) throws Exception {
        ExecutorService pool = Executors.newSingleThreadExecutor();
        Audit audit = new Audit();
        try {
            pool.submit(() -> {
                RequestContext.set("ada");
                checkout(audit);
                if (clearAfterwards) {
                    RequestContext.clear();
                }
            }).get();
            pool.submit(() -> checkout(audit)).get();
        } finally {
            pool.shutdown();
        }
        return audit.lines();
    }

    private static void four() throws Exception {
        System.out.println("FOUR. A thread that is reused.");
        System.out.println("  request A sets its customer and forgets to clear it. request B, an anonymous visitor, runs next on the same pool thread: " + reusedThread(false) + ".");
        System.out.println("  request B was logged as ada. a pool reuses its threads, so what a request leaves behind, the next one finds.");
        System.out.println("  with the clear in a finally block: " + reusedThread(true) + ".");
    }

    private static void five() throws Exception {
        System.out.println("FIVE. A new thread starts empty.");
        Audit audit = new Audit();
        ExecutorService other = Executors.newSingleThreadExecutor();
        try {
            RequestContext.with("ada", () -> {
                try {
                    other.submit(() -> checkout(audit)).get();
                } catch (Exception e) {
                    throw new IllegalStateException(e);
                }
                return null;
            });
        } finally {
            other.shutdown();
        }
        System.out.println("  ada's request hands the work to another thread: " + audit.lines() + ".");
        InheritedContext.set("ada");
        String[] seen = new String[1];
        Thread child = new Thread(() -> seen[0] = InheritedContext.customer());
        child.start();
        child.join();
        InheritedContext.clear();
        System.out.println("  a thread created by ada's thread inherits a copy: " + seen[0] + ". but a pool thread is created once and reused, so it holds whatever was there when it was created, not the current request's.");
        System.out.println("  handing work on means handing the context on, on purpose.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Audit audit = new Audit();
        audit.record("reserved stock");
        System.out.println("  a method that reads the context has a dependency its signature does not show. called with none set: " + audit.lines() + ".");
        System.out.println("  every test of the code below the door has to remember to set the context first, and to clear it after.");
        System.out.println("  and a long-lived pool thread keeps whatever is left in it for as long as the thread lives.");
    }
}
