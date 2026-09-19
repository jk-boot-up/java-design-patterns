package com.jk.explore.featuretoggle;

import java.util.Set;

public class FeatureToggleDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
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

    static int gotIt(Toggles toggles, int customers) {
        int n = 0;
        for (int i = 0; i < customers; i++) {
            if (toggles.isOn("gift-wrap", "c" + i)) {
                n++;
            }
        }
        return n;
    }

    private static void one() {
        System.out.println("ONE. Deploying is releasing.");
        System.out.println("  gift wrap goes live by deploying it: 1 deploy. it has a bug, so taking it away is another: 2 deploys.");
        System.out.println("  each deploy ships every other change waiting in the branch too, so the wish to switch one thing carries everything else with it.");
    }

    private static void two() {
        System.out.println("TWO. Deploy dark, switch later.");
        Toggles toggles = new Toggles();
        toggles.define("gift-wrap", new Rule.Off(), 10);
        Checkout checkout = new Checkout(toggles, false);
        System.out.println("  gift wrap is in the deployed code, switched off. an order of 5000 costs: " + checkout.total("c1", 5000) + ".");
        toggles.set("gift-wrap", new Rule.On());
        System.out.println("  the switch is turned on in the table. no deploy. the same order costs: " + checkout.total("c1", 5000) + ".");
    }

    private static void three() {
        System.out.println("THREE. Switch on for some.");
        Toggles toggles = new Toggles();
        toggles.define("gift-wrap", new Rule.Percent(10), 10);
        System.out.println("  10 percent rollout. of 100 customers, got it: " + gotIt(toggles, 100) + ".");
        toggles.set("gift-wrap", new Rule.Only(Set.of("c1", "c2")));
        System.out.println("  only two named testers. of 100 customers, got it: " + gotIt(toggles, 100) + ".");
    }

    private static void four() {
        System.out.println("FOUR. The kill switch.");
        Toggles toggles = new Toggles();
        toggles.define("gift-wrap", new Rule.Percent(20), 10);
        Checkout checkout = new Checkout(toggles, true);
        System.out.println("  gift wrap has a bug. with 20 percent on, of 100 orders, failed: " + failures(checkout, 100) + ".");
        toggles.set("gift-wrap", new Rule.Off());
        System.out.println("  one change in the table turned it off. of 100 orders, failed: " + failures(checkout, 100) + ". no deploy.");
    }

    private static void five() {
        System.out.println("FIVE. When the table cannot be read.");
        Toggles toggles = new Toggles();
        toggles.define("gift-wrap", new Rule.On(), 10);
        Checkout checkout = new Checkout(toggles, false);
        System.out.println("  the table is up. an order of 5000: " + checkout.total("c1", 5000) + ".");
        toggles.storeDown();
        System.out.println("  the table is down. an order of 5000: " + checkout.total("c1", 5000) + ". the order still works, and every feature falls back to off.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Toggles toggles = new Toggles();
        toggles.define("gift-wrap", new Rule.On(), 10);
        toggles.define("new-search", new Rule.On(), 20);
        toggles.define("loyalty-points", new Rule.Percent(30), 150);
        toggles.define("express-shipping", new Rule.Off(), 40);
        toggles.define("dark-mode", new Rule.Percent(50), 190);
        System.out.println("  " + toggles.count() + " toggles make " + (1 << toggles.count()) + " possible combinations. the tests usually run one.");
        System.out.println("  on day 200, settled for over 90 days and still in the code: " + toggles.stale(200, 90) + ". every one is an if that nobody needs.");
    }
}
