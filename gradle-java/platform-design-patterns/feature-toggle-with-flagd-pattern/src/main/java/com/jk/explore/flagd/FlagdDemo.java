package com.jk.explore.flagd;

import java.util.List;

public class FlagdDemo {

    public static void main(String[] args) throws Exception {
        if (!Flagd.toolsAvailable()) {
            System.out.println("This demo needs Docker running, and the flagd image. Start Docker, and run it again.");
            return;
        }
        try (Flagd flagd = new Flagd()) {
            one();
            flagd.define("gift-wrap", new Rule.Off());
            flagd.start();
            two(flagd);
            three(flagd);
            four(flagd);
            five(flagd);
            six();
        }
    }

    static int gotIt(Flagd flagd, int customers) {
        int n = 0;
        for (int i = 0; i < customers; i++) {
            if (Boolean.TRUE.equals(flagd.evaluate("gift-wrap", "c" + i))) {
                n++;
            }
        }
        return n;
    }

    static int failures(Checkout checkout, int customers) {
        int failed = 0;
        for (int i = 0; i < customers; i++) {
            if (checkout.total("c" + i, 5000) < 0) {
                failed++;
            }
        }
        return failed;
    }

    private static void one() {
        System.out.println("ONE. Deploying is releasing.");
        System.out.println("  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.");
        System.out.println("  each deploy ships every other change waiting in the branch too.");
    }

    private static void two(Flagd flagd) throws Exception {
        System.out.println("TWO. Deploy dark, switch later.");
        Checkout checkout = new Checkout(flagd, false);
        System.out.println("  gift wrap is in the deployed code, and flagd has it off. an order of 5000 costs: " + checkout.total("c1", 5000) + ".");
        flagd.change("gift-wrap", new Rule.On());
        System.out.println("  the flags file was edited, and flagd noticed by itself. no deploy, no restart. the same order costs: " + checkout.total("c1", 5000) + ".");
    }

    private static void three(Flagd flagd) throws Exception {
        System.out.println("THREE. Switch on for some.");
        flagd.change("gift-wrap", new Rule.Percent(10));
        int tenth = gotIt(flagd, 100);
        System.out.println("  a 10 percent rollout, decided by flagd's own hash of the customer. of 100 customers, got it: " + (tenth >= 3 && tenth <= 20 ? "about a tenth" : "an unexpected number") + ".");
        flagd.change("gift-wrap", new Rule.Only(List.of("c1", "c2")));
        System.out.println("  only two named testers. of 100 customers, got it: " + gotIt(flagd, 100) + ".");
    }

    private static void four(Flagd flagd) throws Exception {
        System.out.println("FOUR. The kill switch.");
        flagd.change("gift-wrap", new Rule.Percent(20));
        Checkout checkout = new Checkout(flagd, true);
        int failed = failures(checkout, 100);
        System.out.println("  gift wrap has a bug. with 20 percent on, some of 100 orders failed: " + (failed > 0 ? "yes" : "no") + ", " + (failed >= 5 && failed <= 40 ? "about a fifth" : "an unexpected number") + ".");
        flagd.change("gift-wrap", new Rule.Off());
        System.out.println("  one edit to the file turned it off. of 100 orders, failed: " + failures(checkout, 100) + ". no deploy.");
    }

    private static void five(Flagd flagd) throws Exception {
        System.out.println("FIVE. When flagd cannot be reached.");
        flagd.change("gift-wrap", new Rule.On());
        Checkout checkout = new Checkout(flagd, false);
        System.out.println("  flagd is up. an order of 5000: " + checkout.total("c1", 5000) + ".");
        flagd.stop();
        System.out.println("  flagd is stopped. an order of 5000: " + checkout.total("c1", 5000) + ". the order still works, and every feature falls back to off.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        int toggles = 5;
        System.out.println("  this file has one real flag. a shop with " + toggles + " flags like it would have " + (1 << toggles) + " possible combinations. the tests usually run one.");
        System.out.println("  flagd is another process to run and keep up, and every flag check is a network call: this demo made hundreds.");
        System.out.println("  and a flag that is settled and still in the file is an if that nobody needs. flagd does not remove it for you.");
    }
}
