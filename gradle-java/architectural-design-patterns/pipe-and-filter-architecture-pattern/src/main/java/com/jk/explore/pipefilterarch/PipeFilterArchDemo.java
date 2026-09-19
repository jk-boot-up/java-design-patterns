package com.jk.explore.pipefilterarch;

public class PipeFilterArchDemo {

    static final int TICKS = 30;

    static Line pipeline(int priceWorkers, int limit) {
        return new Line(new Stage("parse", 1, 1, limit), new Stage("price", 3, priceWorkers, limit), new Stage("pack", 1, 1, limit));
    }

    static String queues(Line line) {
        StringBuilder b = new StringBuilder();
        for (Stage s : line.stages()) {
            b.append(s.name()).append(' ').append(s.queued()).append(", ");
        }
        return b.substring(0, b.length() - 2);
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
        System.out.println("ONE. One big step.");
        Line big = new Line(new Stage("everything", 5, 1, Integer.MAX_VALUE));
        big.run(TICKS);
        System.out.println("  parse 1 tick, price 3, pack 1: 5 ticks for each order, one at a time. an order arrives every tick.");
        System.out.println("  after " + TICKS + " ticks, orders done: " + big.out() + ".");
    }

    private static void two() {
        System.out.println("TWO. Stages joined by waiting lines.");
        Line line = pipeline(1, Integer.MAX_VALUE);
        line.run(TICKS);
        System.out.println("  the same work in three stages, each working while the others do. after " + TICKS + " ticks, orders done: " + line.out() + ".");
        System.out.println("  the parse stage takes a new order while price is still on the last one.");
    }

    private static void three() {
        System.out.println("THREE. The slowest stage sets the pace.");
        Line line = pipeline(1, Integer.MAX_VALUE);
        line.run(TICKS);
        System.out.println("  waiting in front of each stage: " + queues(line) + ".");
        System.out.println("  price takes 3 ticks, so one order leaves every 3 ticks however fast parse and pack are. orders pile up in front of it.");
    }

    private static void four() {
        System.out.println("FOUR. Widen only the slow stage.");
        Line line = pipeline(3, Integer.MAX_VALUE);
        line.run(TICKS);
        System.out.println("  three price workers. after " + TICKS + " ticks, orders done: " + line.out() + ". waiting: " + queues(line) + ".");
        System.out.println("  parse and pack were not touched. now they take one order a tick, and that is the new limit.");
    }

    private static void five() {
        System.out.println("FIVE. A limit on each waiting line.");
        Line open = pipeline(1, Integer.MAX_VALUE);
        Line limited = pipeline(1, 3);
        open.run(TICKS);
        limited.run(TICKS);
        System.out.println("  no limit: most orders waiting in one line " + open.stage("price").peakQueue() + ", refused at the door " + open.refused() + ".");
        System.out.println("  limit of 3: most orders waiting in one line " + limited.stage("price").peakQueue() + ", refused at the door " + limited.refused() + ". orders done: " + limited.out() + ", the same as without a limit.");
        System.out.println("  a full line makes the stage before it hold its order, and so on back to the door. that push-back is called backpressure.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Line line = pipeline(1, Integer.MAX_VALUE);
        line.run(TICKS);
        int lost = line.stage("price").crash();
        System.out.println("  the price stage crashes. orders it was holding, waiting or working on: " + lost + ". they were accepted from customers and are gone, unless the lines are kept somewhere that survives.");
        System.out.println("  and an order now passes through 3 stages and 2 waiting lines, so a single order takes longer than the 5 ticks of work, whenever it has to wait.");
    }
}
