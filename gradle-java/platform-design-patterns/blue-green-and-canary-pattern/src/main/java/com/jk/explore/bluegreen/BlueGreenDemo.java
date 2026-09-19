package com.jk.explore.bluegreen;

import java.util.List;

public class BlueGreenDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Replace it where it stands.");
        int failed = new InPlaceUpgrade(10).run(100);
        System.out.println("  stop v1, install v2, start v2: 10 requests arrive while it is down. of 100 requests, failed: " + failed + ".");
    }

    private static void two() {
        System.out.println("TWO. Blue and green.");
        Router router = new Router(Version.good("v1"), Version.good("v2"));
        for (int seq = 0; seq < 50; seq++) {
            router.route(seq, Router.orderCents(seq));
        }
        router.green().handle(2000);
        System.out.println("  v2 was started beside v1 and tried with a test order: ok. v1 served " + router.blue().served() + " requests meanwhile.");
        router.setGreenPercent(100);
        for (int seq = 50; seq < 100; seq++) {
            router.route(seq, Router.orderCents(seq));
        }
        System.out.println("  the switch was one setting. after it v2 served " + (router.green().served() - 1) + ". of 100 requests, failed: " + router.failures() + ".");
    }

    private static void three() {
        System.out.println("THREE. Going back.");
        Router router = new Router(Version.good("v1"), Version.buggy("v2"));
        router.setGreenPercent(100);
        for (int seq = 0; seq < 50; seq++) {
            router.route(seq, Router.orderCents(seq));
        }
        int failedOnV2 = router.failures();
        router.setGreenPercent(0);
        for (int seq = 50; seq < 100; seq++) {
            router.route(seq, Router.orderCents(seq));
        }
        System.out.println("  v2 has a bug with big orders. 50 requests on v2, failed: " + failedOnV2 + ".");
        System.out.println("  one setting sent traffic back to v1, which had never been stopped. the next 50 requests, failed: " + (router.failures() - failedOnV2) + ".");
    }

    private static void four() {
        System.out.println("FOUR. A canary.");
        Router router = new Router(Version.good("v1"), Version.buggy("v2"));
        router.setGreenPercent(5);
        for (int seq = 0; seq < 200; seq++) {
            router.route(seq, Router.orderCents(seq));
        }
        System.out.println("  5% of traffic to the buggy v2. of 200 requests, v2 got " + router.green().served() + " and failed " + router.failures() + ".");
        System.out.println("  had all 200 gone to v2, " + 200 / 10 + " would have failed. a few customers found the bug, not everyone.");
    }

    private static void five() {
        System.out.println("FIVE. Promote in steps, with a gate.");
        Router bad = new Router(Version.good("v1"), Version.buggy("v2"));
        CanaryRollout stopped = new CanaryRollout(bad, 5);
        stopped.run(List.of(5, 25, 50, 100), 100);
        System.out.println("  buggy v2: halted " + stopped.halted() + " after " + stopped.stepsDone() + " step, failure rate on v2 " + stopped.lastFailurePercent() + "%, traffic back to " + (100 - bad.greenPercent()) + "% v1.");
        Router fine = new Router(Version.good("v1"), Version.good("v2"));
        CanaryRollout through = new CanaryRollout(fine, 5);
        through.run(List.of(5, 25, 50, 100), 100);
        System.out.println("  good v2: halted " + through.halted() + ", steps " + through.stepsDone() + ", now at " + fine.greenPercent() + "% v2.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        System.out.println("  two full copies run during the switch: capacity " + (10 + 10) + " instead of 10.");
        int writtenByV2 = 5;
        Version v1 = Version.good("v1");
        Version v2 = Version.good("v2");
        int unreadable = v1.format().equals(v2.format()) ? 0 : writtenByV2;
        System.out.println("  v2 wrote " + writtenByV2 + " orders in a new format before we went back. v1 can read: " + (writtenByV2 - unreadable) + ".");
        System.out.println("  both releases share one database, so a release that changes the data cannot be switched back safely.");
    }
}
