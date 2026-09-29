package com.jk.explore.leaderfollowers;

import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.LinkedBlockingQueue;

/**
 * The five acts: a dispatcher that hands off, leader and followers, leadership passed on, every thread working, and the bill.
 */
public final class LeaderFollowersDemo {

    static final int MESSAGES = 20;

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static BlockingQueue<Message> messages() {
        BlockingQueue<Message> q = new LinkedBlockingQueue<>();
        for (int i = 1; i <= MESSAGES; i++) {
            q.add(new Message("ORD-" + i, 10));
        }
        q.add(Message.STOP);
        return q;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();

        out.add("ONE. A dispatcher receives every message and hands it to a worker.");
        DispatcherWorkers dw = new DispatcherWorkers(messages(), 4);
        dw.runUntilStopped();
        out.add("  " + dw.threadCount() + " threads: 1 dispatcher + 4 workers; " + dw.record().entries().size() + " orders handled");
        out.add("  hand-offs between threads: " + dw.handOffs() + "; handled by the thread that received it: "
                + dw.record().sameThread());
        out.add("  the dispatcher handled 0 orders itself");

        out.add("");
        out.add("TWO. Leader and followers: the pool takes turns.");
        LeaderFollowers lf = new LeaderFollowers(messages(), 4);
        lf.runUntilStopped();
        out.add("  " + lf.threadCount() + " threads, no dispatcher; " + lf.record().entries().size() + " orders handled");
        out.add("  threads ever waiting for a message at the same moment: " + lf.mostWaitingAtOnce());

        out.add("");
        out.add("THREE. Receive, promote a follower, then handle.");
        out.add("  leadership passed on " + lf.promotions() + " times, once per order");
        out.add("  handled by the thread that received it: " + lf.record().sameThread() + " of " + MESSAGES
                + "; hand-offs between threads: 0");

        out.add("");
        out.add("FOUR. Every thread in the pool does real work.");
        long workers = lf.record().entries().stream().map(Record.Entry::handledBy).distinct().count();
        out.add("  orders handled by pool threads: " + lf.record().entries().size() + ", by " + (workers >= 2 ? "several" : workers)
                + " different threads; none sat as a pure dispatcher");

        out.add("");
        out.add("FIVE. The bill: order is not kept.");
        BlockingQueue<Message> two = new LinkedBlockingQueue<>(List.of(
                new Message("ORD-1 place order", 80), new Message("ORD-1 cancel order", 5), Message.STOP));
        LeaderFollowers lf2 = new LeaderFollowers(two, 2);
        lf2.runUntilStopped();
        out.add("  \"place\" then \"cancel\" for the same order, received in that order");
        out.add("  finished in the order: " + lf2.record().finished());
        out.add("  messages that must stay in order need to go to the same thread");
        return out;
    }

    private LeaderFollowersDemo() {
    }
}
