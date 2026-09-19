package com.jk.explore.leaderelection;

import java.util.List;

public class LeaderElectionDemo {

    static final long TTL = 30;

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static List<Node> nodes(LeaseStore store, ReportSink sink) {
        return List.of(new Node("A", store, sink, TTL), new Node("B", store, sink, TTL), new Node("C", store, sink, TTL));
    }

    private static void one() {
        System.out.println("ONE. Three copies, nobody in charge.");
        ReportSink sink = new ReportSink(false);
        for (Node n : nodes(new LeaseStore(new Clock()), sink)) {
            n.sendReportAlways();
        }
        System.out.println("  the nightly sales report is sent by every copy: " + sink.written() + ".");
        System.out.println("  the manager receives it three times.");
    }

    private static void two() {
        System.out.println("TWO. One holds the lease.");
        LeaseStore store = new LeaseStore(new Clock());
        ReportSink sink = new ReportSink(false);
        List<Node> nodes = nodes(store, sink);
        for (Node n : nodes) {
            n.tryToLead();
        }
        for (Node n : nodes) {
            n.sendReportIfLeader();
        }
        System.out.println("  all three ask for the lease. the leader is " + store.leader().orElse("nobody") + ". the report was sent by: " + sink.written() + ".");
    }

    private static void three() {
        System.out.println("THREE. The leader dies.");
        Clock clock = new Clock();
        LeaseStore store = new LeaseStore(clock);
        ReportSink sink = new ReportSink(false);
        List<Node> nodes = nodes(store, sink);
        for (Node n : nodes) {
            n.tryToLead();
        }
        nodes.get(0).die();
        System.out.println("  A, the leader, dies. leader now: " + store.leader().orElse("nobody") + ", and its lease has " + TTL + " seconds to run.");
        clock.advance(10);
        nodes.get(1).tryToLead();
        System.out.println("  after 10 seconds B asks: leader is still " + store.leader().orElse("nobody") + ".");
        clock.advance(TTL - 10);
        nodes.get(1).tryToLead();
        nodes.get(2).tryToLead();
        System.out.println("  after " + TTL + " seconds the lease has expired. B asks first and becomes leader: " + store.leader().orElse("nobody") + ".");
        System.out.println("  for those " + TTL + " seconds nobody was leading. that is the cost of not being sure A was dead.");
    }

    private static void four() {
        System.out.println("FOUR. Two who think they lead.");
        Clock clock = new Clock();
        LeaseStore store = new LeaseStore(clock);
        ReportSink sink = new ReportSink(false);
        Node a = new Node("A", store, sink, TTL);
        Node b = new Node("B", store, sink, TTL);
        a.tryToLead();
        clock.advance(TTL + 5);
        b.tryToLead();
        System.out.println("  A paused for " + (TTL + 5) + " seconds, say for a long garbage collection. its lease expired and B took it. the store says the leader is " + store.leader().orElse("nobody") + ".");
        a.sendReportIfLeader();
        b.sendReportIfLeader();
        System.out.println("  A wakes up, still believing it leads, and sends. so does B. the report was sent by: " + sink.written() + ".");
    }

    private static void five() {
        System.out.println("FIVE. Fencing.");
        Clock clock = new Clock();
        LeaseStore store = new LeaseStore(clock);
        ReportSink sink = new ReportSink(true);
        Node a = new Node("A", store, sink, TTL);
        Node b = new Node("B", store, sink, TTL);
        a.tryToLead();
        clock.advance(TTL + 5);
        b.tryToLead();
        b.sendReportIfLeader();
        try {
            a.sendReportIfLeader();
        } catch (ReportSink.StaleToken e) {
            System.out.println("  A wakes up and tries to send: refused, " + e.getMessage() + ".");
        }
        System.out.println("  the report was sent by: " + sink.written() + ". each lease carries a token that only goes up, and the thing being written to checks it.");
    }

    /** A healthy leader that renews every {@code renewEvery} seconds against a lease of {@code ttl}. Returns the second it lost the lease, or -1. */
    static int secondLeadershipWasLost(long ttl, int renewEvery) {
        Clock clock = new Clock();
        LeaseStore store = new LeaseStore(clock);
        Node a = new Node("A", store, new ReportSink(true), ttl);
        Node b = new Node("B", store, new ReportSink(true), ttl);
        a.tryToLead();
        for (int second = 1; second <= 60; second++) {
            clock.advance(1);
            if (second % renewEvery == 0) {
                a.tryToLead();
            }
            b.tryToLead();
            if (!store.leader().orElse("nobody").equals("A")) {
                return second;
            }
        }
        return -1;
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        System.out.println("  a leader that is perfectly healthy, renewing every 7 seconds against a lease of 5: it loses leadership at second " + secondLeadershipWasLost(5, 7) + ".");
        System.out.println("  the same leader against a lease of 30: " + (secondLeadershipWasLost(30, 7) < 0 ? "never loses it" : "loses it") + ".");
        System.out.println("  the lease must be longer than the renewal interval, with room for a slow moment. too long, and a dead leader goes unnoticed for that long.");
        System.out.println("  and everything now depends on one shared record. if it is down, nobody can lead.");
    }
}
