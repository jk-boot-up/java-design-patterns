package com.jk.explore.messagechannel;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

public class MessageChannelDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Checkout calls the warehouse.");
        Warehouse warehouse = new Warehouse();
        warehouse.goDown();
        int failed = 0;
        for (int i = 1; i <= 3; i++) {
            try {
                warehouse.pick("ORD-" + i);
            } catch (IllegalStateException e) {
                failed++;
            }
        }
        System.out.println("  the warehouse system is down for maintenance. orders placed: 3. checkouts that failed: " + failed + ".");
        System.out.println("  the shop cannot sell while another system is away, though selling does not need it to answer yet.");
    }

    private static void two() {
        System.out.println("TWO. A channel between them.");
        Channel<String> pick = new Channel<>("pick-orders", "PickOrder", 100);
        for (int i = 1; i <= 3; i++) {
            pick.send(Message.of("m" + i, "PickOrder", "ORD-" + i));
        }
        System.out.println("  checkout sends 3 messages and carries on. waiting in the channel: " + pick.waiting() + ".");
        List<String> got = new ArrayList<>();
        for (Message<String> m = pick.receive(); m != null; m = pick.receive()) {
            got.add(m.body());
        }
        System.out.println("  the warehouse takes them, each once: " + got + ".");
    }

    private static void three() {
        System.out.println("THREE. The receiver is away.");
        Channel<String> pick = new Channel<>("pick-orders", "PickOrder", 100);
        Warehouse warehouse = new Warehouse();
        warehouse.goDown();
        for (int i = 1; i <= 3; i++) {
            pick.send(Message.of("m" + i, "PickOrder", "ORD-" + i));
        }
        System.out.println("  the warehouse is down. checkout sends 3, and none fail. waiting: " + pick.waiting() + ".");
        warehouse.comeBack();
        for (Message<String> m = pick.receive(); m != null; m = pick.receive()) {
            warehouse.pick(m.body());
        }
        System.out.println("  the warehouse comes back and works through them, in order: " + warehouse.told() + ".");
    }

    private static void four() {
        System.out.println("FOUR. An envelope.");
        Message<String> m = new Message<>("m1", "PickOrder", Map.of("priority", "express", "correlation", "ORD-1"), "2 x MUG-BLUE");
        System.out.println("  headers, readable without opening the body: " + new java.util.TreeMap<>(m.headers()) + ". type: " + m.type() + ".");
        System.out.println("  body: " + m.body() + ".");
        System.out.println("  a router or a receiver can decide what to do from the envelope alone.");
    }

    private static void five() {
        System.out.println("FIVE. One channel, one kind of message.");
        Channel<String> pick = new Channel<>("pick-orders", "PickOrder", 100);
        try {
            pick.send(Message.of("m1", "RefundRequest", "ORD-1"));
        } catch (WrongType e) {
            System.out.println("  " + e.getMessage() + ".");
        }
        System.out.println("  a receiver of pick orders never has to ask what it was given.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Channel<String> pick = new Channel<>("pick-orders", "PickOrder", 5);
        int accepted = 0;
        int refused = 0;
        for (int i = 1; i <= 8; i++) {
            try {
                pick.send(Message.of("m" + i, "PickOrder", "ORD-" + i));
                accepted++;
            } catch (ChannelFull e) {
                refused++;
            }
        }
        System.out.println("  the warehouse stays down and a channel of 5 fills: " + accepted + " accepted, " + refused + " refused. a channel must have a limit, and somebody must decide what to do at it.");
        System.out.println("  and the sender no longer learns whether the warehouse picked the order. it learns only that the message was accepted.");
        System.out.println("  sent " + pick.sent() + ", received " + pick.received() + ": the difference is work nobody has done yet.");
    }
}
