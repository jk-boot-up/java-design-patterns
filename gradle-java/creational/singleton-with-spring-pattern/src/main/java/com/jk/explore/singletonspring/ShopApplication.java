package com.jk.explore.singletonspring;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.CountDownLatch;
import java.util.concurrent.ConcurrentHashMap;

@SpringBootApplication
public class ShopApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(ShopApplication.class).web(WebApplicationType.NONE);
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static void one() {
        System.out.println("ONE. One bean, shared.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Checkout checkout = ctx.getBean(Checkout.class);
            AdminConsole admin = ctx.getBean(AdminConsole.class);
            RetryJob retry = ctx.getBean(RetryJob.class);
            System.out.println("  checkout, admin and retry hold the same generator: "
                    + (checkout.generator() == admin.generator() && admin.generator() == retry.generator()));
            System.out.println("  " + checkout.issue());
            System.out.println("  " + admin.issue());
            System.out.println("  " + retry.issue() + "  (three callers, one counter)");
        }
    }

    static void two() {
        System.out.println("TWO. Nothing stops new.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            OrderSequenceGenerator managed = ctx.getBean(OrderSequenceGenerator.class);
            OrderSequenceGenerator forged = new OrderSequenceGenerator();
            System.out.println("  managed says " + managed.nextOrderNumber() + ", a plain new says " + forged.nextOrderNumber());
            System.out.println("  same object: " + (managed == forged) + ". the constructor is public, so the compiler cannot help.");
        }
    }

    static void three() {
        System.out.println("THREE. One per container, not one per JVM.");
        try (ConfigurableApplicationContext a = builder().run();
             ConfigurableApplicationContext b = builder().run()) {
            String first = a.getBean(Checkout.class).issue();
            String second = b.getBean(Checkout.class).issue();
            System.out.println("  context A issues " + first + ", context B issues " + second);
            System.out.println("  the same order number went to two customers: " + first.equals(second));
        }
    }

    static void four() {
        System.out.println("FOUR. A scope change flips the answer.");
        try (ConfigurableApplicationContext ctx = builder()
                .initializers(c -> c.addBeanFactoryPostProcessor(
                        bf -> bf.getBeanDefinition("orderSequenceGenerator").setScope("prototype")))
                .run()) {
            String checkout = ctx.getBean(Checkout.class).issue();
            String admin = ctx.getBean(AdminConsole.class).issue();
            System.out.println("  with scope prototype: checkout issues " + checkout + ", admin issues " + admin);
            System.out.println("  one word changed, and the two callers no longer share a counter.");
        }
    }

    static void five() {
        System.out.println("FIVE. When is it built?");
        OrderSequenceGenerator.BUILT.set(0);
        try (ConfigurableApplicationContext ctx = builder().run()) {
            System.out.println("  eager: built " + OrderSequenceGenerator.BUILT.get() + " before any caller asked.");
        }
        OrderSequenceGenerator.BUILT.set(0);
        try (ConfigurableApplicationContext ctx = builder().lazyInitialization(true).run()) {
            System.out.println("  lazy: built " + OrderSequenceGenerator.BUILT.get() + " after startup.");
            ctx.getBean(OrderSequenceGenerator.class);
            System.out.println("  lazy: built " + OrderSequenceGenerator.BUILT.get() + " after the first caller.");
        }
    }

    static void six() throws Exception {
        System.out.println("SIX. Shared means shared by every thread.");
        UnsafeOrderSequence unsafe = new UnsafeOrderSequence();
        Gate gate = new Gate();
        CountDownLatch inside = new CountDownLatch(1);
        String[] slow = new String[1];
        Thread first = new Thread(() -> slow[0] = unsafe.nextOrderNumber(() -> {
            inside.countDown();
            gate.await();
        }), "customer-1");
        first.start();
        inside.await();
        String quick = unsafe.nextOrderNumber(() -> { });
        gate.open();
        first.join();
        System.out.println("  a plain long, held between read and write: " + slow[0] + " and " + quick);
        System.out.println("  duplicate order number: " + slow[0].equals(quick));

        OrderSequenceGenerator safe = new OrderSequenceGenerator();
        Set<String> seen = ConcurrentHashMap.newKeySet();
        Thread[] callers = new Thread[4];
        for (int i = 0; i < callers.length; i++) {
            callers[i] = new Thread(() -> {
                for (int n = 0; n < 2500; n++) {
                    seen.add(safe.nextOrderNumber());
                }
            });
            callers[i].start();
        }
        for (Thread t : callers) {
            t.join();
        }
        System.out.println("  an AtomicLong, 4 threads x 2500: " + seen.size() + " distinct numbers, none repeated.");
        System.out.println("  Spring shares the bean. Keeping its state safe is still your job.");
    }
}
