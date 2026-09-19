package com.jk.explore.deadletter;

import java.util.HashMap;
import java.util.Map;
import java.util.function.Consumer;

public class DeadLetterDemo {

    /** A handler that cannot cope with a body it cannot read. */
    static Consumer<Message> fussy() {
        return m -> {
            if (m.body().contains("###")) {
                throw new IllegalArgumentException("cannot read the body of " + m.id());
            }
        };
    }

    static Worker loaded(Consumer<Message> handler, int maxAttempts) {
        Worker w = new Worker(handler, maxAttempts);
        w.send(new Message("ORD-1", "2 x MUG-BLUE"));
        w.send(new Message("ORD-2", "### garbled ###"));
        w.send(new Message("ORD-3", "1 x ESP-001"));
        w.send(new Message("ORD-4", "5 x TEA-050"));
        return w;
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A message that can never succeed.");
        Worker w = loaded(fussy(), 10);
        w.runAll(false);
        System.out.println("  four orders, one garbled. handled: " + w.handled() + ". still waiting: " + w.waiting() + ". attempts made: " + w.totalAttempts() + ".");
        System.out.println("  the garbled order is at the head of the line and will never succeed. orders 3 and 4 are stuck behind it.");
    }

    private static void two() {
        System.out.println("TWO. A dead letter channel.");
        Worker w = loaded(fussy(), 3);
        w.runAll(true);
        System.out.println("  after 3 attempts the garbled order is moved aside. handled: " + w.handled() + ". waiting: " + w.waiting() + ". dead letters: " + w.deadLetters().size() + ".");
        System.out.println("  orders 3 and 4 went through.");
    }

    private static void three() {
        System.out.println("THREE. It says why.");
        Worker w = loaded(fussy(), 3);
        w.runAll(true);
        DeadLetter d = w.deadLetters().get(0);
        System.out.println("  " + d.message().id() + ": " + d.attempts() + " attempts, last error '" + d.lastError() + "', from channel " + d.fromChannel() + ".");
        System.out.println("  the original message is kept exactly, so it can be looked at, and put back.");
    }

    private static void four() {
        System.out.println("FOUR. A slow day is not a dead letter.");
        Map<String, Integer> seen = new HashMap<>();
        Consumer<Message> flaky = m -> {
            int n = seen.merge(m.id(), 1, Integer::sum);
            if (m.body().contains("###")) {
                throw new IllegalArgumentException("cannot read the body of " + m.id());
            }
            if (m.id().equals("ORD-3") && n < 2) {
                throw new IllegalStateException("the warehouse system timed out");
            }
        };
        Worker w = loaded(flaky, 3);
        w.runAll(true);
        System.out.println("  ORD-3 failed once, on a timeout, and succeeded on the second attempt. handled: " + w.handled() + ".");
        System.out.println("  only ORD-2, which fails every time, is a dead letter: " + w.deadLetters().stream().map(x -> x.message().id()).toList() + ".");
        System.out.println("  retrying is for the first kind of failure, and the dead letter channel is for the second.");
    }

    private static void five() {
        System.out.println("FIVE. Fix it, and replay.");
        boolean[] fixed = {false};
        Consumer<Message> handler = m -> {
            if (!fixed[0] && m.body().contains("###")) {
                throw new IllegalArgumentException("cannot read the body of " + m.id());
            }
        };
        Worker w = loaded(handler, 3);
        w.runAll(true);
        System.out.println("  before the fix: handled " + w.handled() + ", dead " + w.deadLetters().size() + ".");
        fixed[0] = true;
        int replayed = w.replayDeadLetters();
        w.runAll(true);
        System.out.println("  the parser is fixed and " + replayed + " dead letter is replayed. handled: " + w.handled() + ", dead " + w.deadLetters().size() + ".");
        System.out.println("  note the order: ORD-2 was handled after ORD-3 and ORD-4. replay does not restore the order.");
    }

    private static void six() {
        System.out.println("SIX. The bill: nobody is looking.");
        Worker w = new Worker(fussy(), 3);
        for (int i = 1; i <= 40; i++) {
            w.send(new Message("ORD-" + i, i % 2 == 0 ? "### garbled ###" : "1 x MUG-BLUE"));
        }
        w.runAll(true);
        System.out.println("  40 orders, half of them garbled: " + w.deadLetters().size() + " dead letters, and every one of those orders was accepted from a customer.");
        System.out.println("  the main channel looks perfectly healthy: " + w.waiting() + " waiting. the dead letter channel is where the loss is, and nothing tells anyone to look.");
        System.out.println("  a dead letter channel needs an alert on its depth, an owner, and a limit on how long a message may stay. each keeps a copy of customer data.");
    }
}
