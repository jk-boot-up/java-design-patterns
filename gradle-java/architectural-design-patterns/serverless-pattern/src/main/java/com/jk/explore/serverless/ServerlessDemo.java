package com.jk.explore.serverless;

public class ServerlessDemo {

    static final int COLD = 5;
    static final int IDLE = 10;
    static final int MAX = 15;

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. A machine that is always on.");
        AlwaysOnServer server = new AlwaysOnServer(2);
        System.out.println("  100 ticks, 3 orders. the bill: " + server.bill(100) + ". paid for 100 ticks, used for 3 orders.");
    }

    private static void two() {
        System.out.println("TWO. A function per event.");
        Platform p = new Platform(COLD, IDLE, MAX);
        p.invoke(1);
        p.advance(30);
        p.invoke(1);
        p.advance(30);
        p.invoke(1);
        System.out.println("  the same 3 orders, each one runs a send-receipt function. invocations: " + p.invocations() + ". the bill at 1 per invocation: " + p.bill(1) + ".");
        System.out.println("  between orders nothing runs, and nothing is paid for.");
    }

    private static void three() {
        System.out.println("THREE. Scale out, and back to zero.");
        Platform p = new Platform(COLD, IDLE, MAX);
        System.out.println("  before any order, instances: " + p.instances() + ".");
        p.invoke(5);
        System.out.println("  5 orders at the same moment: instances " + p.instances() + ", cold starts " + p.coldStarts() + ".");
        p.advance(IDLE);
        System.out.println("  " + IDLE + " ticks later, with no orders: instances " + p.instances() + ".");
    }

    private static void four() {
        System.out.println("FOUR. The cold start.");
        Platform p = new Platform(COLD, IDLE, MAX);
        p.invoke(1);
        int first = p.latency();
        p.advance(2);
        p.invoke(1);
        int second = p.latency() - first;
        p.advance(IDLE);
        p.invoke(1);
        int third = p.latency() - first - second;
        System.out.println("  extra wait: first call " + first + " ticks, a call soon after " + second + ", a call after a long quiet " + third + ".");
        System.out.println("  the first call after a quiet time is slow, because an instance must be started for it.");
    }

    private static void five() {
        System.out.println("FIVE. No memory between calls.");
        Platform p = new Platform(COLD, IDLE, MAX);
        p.invoke(1);
        p.advance(2);
        p.invoke(1);
        System.out.println("  two calls in a row: the instance remembers " + p.lastInstanceUses() + ", the outside store " + p.sharedCount() + ".");
        p.advance(IDLE);
        p.invoke(1);
        System.out.println("  after the quiet time: the instance remembers " + p.lastInstanceUses() + ", the outside store " + p.sharedCount() + ".");
        System.out.println("  what is kept in the function is gone. anything that must last goes in a store outside.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        AlwaysOnServer server = new AlwaysOnServer(2);
        Platform quiet = new Platform(COLD, IDLE, MAX);
        quiet.invoke(3);
        Platform busy = new Platform(COLD, IDLE, MAX);
        for (int i = 0; i < 300; i++) {
            busy.invoke(1);
        }
        System.out.println("  100 ticks. quiet, 3 calls: functions " + quiet.bill(1) + ", server " + server.bill(100) + ". busy, 300 calls: functions " + busy.bill(1) + ", server " + server.bill(100) + ".");
        System.out.println("  paying per call is cheap when quiet and dear when busy all the time.");
        System.out.println("  and a job of 20 ticks against a limit of " + MAX + ": finished " + new Platform(COLD, IDLE, MAX).runWork(20) + ". long work does not fit.");
    }
}
