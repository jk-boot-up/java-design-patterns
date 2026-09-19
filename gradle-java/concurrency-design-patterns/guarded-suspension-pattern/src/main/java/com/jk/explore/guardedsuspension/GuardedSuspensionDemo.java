package com.jk.explore.guardedsuspension;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class GuardedSuspensionDemo {

    static void until(java.util.function.BooleanSupplier condition) {
        long deadline = System.nanoTime() + 10_000_000_000L;
        while (!condition.getAsBoolean() && System.nanoTime() < deadline) {
            Thread.onSpinWait();
        }
    }

    static Thread startTaker(Inbox inbox, List<String> got) {
        Thread t = new Thread(() -> {
            try {
                got.add(String.valueOf(inbox.take()));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        t.start();
        return t;
    }

    public static void main(String[] args) throws Exception {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() throws Exception {
        System.out.println("ONE. Waiting by asking.");
        SpinningInbox inbox = new SpinningInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread picker = startTaker(inbox, got);
        until(() -> inbox.checks() >= 1_000_000);
        int whileEmpty = inbox.checks();
        inbox.put("ORD-1");
        picker.join();
        System.out.println("  the picker asks whether an order has come, over and over. no order has come, and it has already asked more than a million times: " + (whileEmpty >= 1_000_000) + ".");
        System.out.println("  it took " + got + " when it arrived. the whole time it kept a processor busy doing nothing.");
    }

    private static void two() throws Exception {
        System.out.println("TWO. Waiting by sleeping.");
        WaitingInbox inbox = new WaitingInbox();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread picker = startTaker(inbox, got);
        until(() -> picker.getState() == Thread.State.WAITING);
        System.out.println("  the picker's thread is: " + picker.getState() + ". it is using no processor, and has asked nothing.");
        inbox.put("ORD-1");
        picker.join();
        System.out.println("  an order arrives, the picker is woken, and takes " + got + ".");
    }

    private static void three() throws Exception {
        System.out.println("THREE. Ask again after waking.");
        for (Inbox inbox : new Inbox[]{new IfGuardInbox(), new WaitingInbox()}) {
            List<String> got = Collections.synchronizedList(new ArrayList<>());
            Thread a = startTaker(inbox, got);
            Thread b = startTaker(inbox, got);
            until(() -> a.getState() == Thread.State.WAITING && b.getState() == Thread.State.WAITING);
            inbox.put("ORD-1");
            until(() -> got.size() >= 1 && (inbox.wakeups() >= 2 || inbox instanceof IfGuardInbox == false));
            long deadline = System.nanoTime() + 300_000_000L;
            until(() -> got.size() == 2 || System.nanoTime() > deadline);
            System.out.println("  two pickers wait and one order arrives, with the guard checked with "
                    + (inbox instanceof IfGuardInbox ? "if" : "while") + ": they took " + got + ".");
            if (inbox instanceof WaitingInbox) {
                System.out.println("  the second picker woke, looked, found nothing, and went back to waiting: " + (a.getState() == Thread.State.WAITING || b.getState() == Thread.State.WAITING) + ".");
            }
            inbox.put("ORD-2");
            a.join();
            b.join();
        }
    }

    private static void four() throws Exception {
        System.out.println("FOUR. The order came first.");
        NoCheckInbox blind = new NoCheckInbox();
        blind.put("ORD-1");
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        Thread late = startTaker(blind, got);
        until(() -> late.getState() == Thread.State.WAITING);
        System.out.println("  the order was already there, and its notification has come and gone. a picker that waits without looking first: " + late.getState() + ", holding nothing.");
        blind.put("ORD-2");
        late.join();
        WaitingInbox careful = new WaitingInbox();
        careful.put("ORD-1");
        List<String> got2 = Collections.synchronizedList(new ArrayList<>());
        startTaker(careful, got2).join();
        System.out.println("  a picker that looks at the guard first takes it at once: " + got2 + ".");
    }

    private static void five() throws Exception {
        System.out.println("FIVE. Wait, but not for ever.");
        WaitingInbox inbox = new WaitingInbox();
        System.out.println("  no order comes. after 100 milliseconds the picker gives up: " + inbox.take(100) + ".");
        inbox.put("ORD-1");
        System.out.println("  with an order there: " + inbox.take(100) + ".");
        System.out.println("  a limit turns 'wait until it is true' into 'wait a while, and tell me if it was not'.");
    }

    private static void six() throws Exception {
        System.out.println("SIX. The bill.");
        WaitingInbox inbox = new WaitingInbox();
        List<Thread> pickers = new ArrayList<>();
        List<String> got = Collections.synchronizedList(new ArrayList<>());
        for (int i = 0; i < 20; i++) {
            pickers.add(startTaker(inbox, got));
        }
        until(() -> pickers.stream().allMatch(t -> t.getState() == Thread.State.WAITING));
        inbox.put("ORD-1");
        until(() -> got.size() == 1);
        until(() -> inbox.wakeups() >= 20);
        System.out.println("  20 pickers waiting, 1 order arrives, and notifyAll: " + inbox.wakeups() + " threads woke, 1 took it, " + (inbox.wakeups() - 1) + " went back to sleep.");
        for (int i = 2; i <= 20; i++) {
            inbox.put("ORD-" + i);
        }
        for (Thread t : pickers) {
            t.join();
        }
        System.out.println("  and a thread waiting for something nobody will ever send waits for ever. every wait needs a plan for how it ends.");
    }
}
