package com.jk.explore.callback;

import java.util.ArrayList;
import java.util.List;

public class CallbackDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Ask, and keep asking.");
        WaitingGateway gateway = new WaitingGateway();
        WaitingGateway.Handle h = gateway.charge("ORD-1", 5);
        while (!h.isDone()) {
            // the caller can do nothing else while it waits
        }
        System.out.println("  the answer arrived on the 5th look. looks made: " + h.polls() + ", 4 of them found nothing.");
        System.out.println("  and the caller could do nothing else in that time.");
    }

    private static void two() {
        System.out.println("TWO. Say what to do, and go on.");
        Gateway gateway = new Gateway();
        List<String> log = new ArrayList<>();
        gateway.charge("ORD-1", r -> log.add("callback: " + r.orderId() + " " + r.message()));
        log.add("charge requested, and the caller goes on");
        log.add("caller does other work");
        gateway.complete("ORD-1", true);
        System.out.println("  " + log + ".");
    }

    private static void three() {
        System.out.println("THREE. What happened decides what to do.");
        Gateway gateway = new Gateway();
        List<String> log = new ArrayList<>();
        java.util.function.Consumer<Result> onResult = r -> log.add(r.paid() ? r.orderId() + ": ship it" : r.orderId() + ": ask for another card");
        gateway.charge("ORD-1", onResult);
        gateway.charge("ORD-2", onResult);
        gateway.complete("ORD-1", true);
        gateway.complete("ORD-2", false);
        System.out.println("  one callback, told the result: " + log + ".");
    }

    private static void four() {
        System.out.println("FOUR. When the callback itself fails.");
        Gateway gateway = new Gateway();
        List<String> log = new ArrayList<>();
        gateway.charge("ORD-1", r -> {
            throw new IllegalStateException("the mail server was down");
        });
        gateway.charge("ORD-2", r -> log.add(r.orderId() + " " + r.message()));
        gateway.complete("ORD-1", true);
        gateway.complete("ORD-2", true);
        System.out.println("  the first callback threw. the gateway went on: " + log + ". recorded: " + gateway.callbackErrors() + ".");
        System.out.println("  the one who asked never sees that exception, because it happened in someone else's call.");
    }

    private static void five() {
        System.out.println("FIVE. Answers in another order.");
        Gateway good = new Gateway();
        SharedFieldShop shop = new SharedFieldShop(good);
        shop.pay("ORD-1");
        shop.pay("ORD-2");
        good.complete("ORD-1", true);
        good.complete("ORD-2", true);
        System.out.println("  remembering the order in a field: " + shop.log() + ". both say ORD-2.");
        Gateway gateway = new Gateway();
        List<String> log = new ArrayList<>();
        for (String id : List.of("ORD-1", "ORD-2")) {
            gateway.charge(id, r -> log.add(id + " " + r.message()));
        }
        gateway.complete("ORD-2", true);
        gateway.complete("ORD-1", true);
        System.out.println("  each callback holding its own order id: " + log + ". the answers came in the other order, and each is right.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Gateway payments = new Gateway();
        Gateway stock = new Gateway();
        Gateway shipping = new Gateway();
        List<String> log = new ArrayList<>();
        payments.charge("ORD-1", paid -> {
            log.add("2. paid");
            stock.charge("ORD-1", reserved -> {
                log.add("4. reserved");
                shipping.charge("ORD-1", shipped -> log.add("6. shipped"));
            });
            log.add("3. stock asked");
        });
        log.add("1. all asked for, first step only");
        payments.complete("ORD-1", true);
        stock.complete("ORD-1", true);
        log.add("5. next step asked");
        shipping.complete("ORD-1", true);
        System.out.println("  pay, then reserve, then ship: three callbacks, each inside the one before, three levels deep.");
        System.out.println("  the order the lines run in: " + log + ". in the code, the line that asks stock is written below the block that ships, and it runs first. that is not the order they are written in.");
        System.out.println("  and every level needs its own handling for a failure, and each answer arrives with no stack that shows who asked.");
    }
}
