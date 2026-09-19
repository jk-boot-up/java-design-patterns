package com.jk.explore.serverlessls;

import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.atomic.AtomicReferenceArray;

public class ServerlessLsDemo {

    static final String FN = "send-receipt";

    public static void main(String[] args) throws Exception {
        if (!Platform.toolsAvailable()) {
            System.out.println("This demo needs Docker running, and the LocalStack and Lambda images. Start Docker, and run it again.");
            return;
        }
        System.setProperty("org.slf4j.simpleLogger.defaultLogLevel", "error");
        try (Platform platform = new Platform()) {
            platform.start();
            platform.deploy(FN, 3);
            one();
            two(platform);
            three(platform);
            four(platform);
            five(platform);
            six(platform);
        }
    }

    static void waitForZero(Platform platform) {
        Platform.waitUntil(() -> platform.copies() == 0, 90);
    }

    private static void one() {
        System.out.println("ONE. A machine that is always on.");
        System.out.println("  in the earlier project's price units, a server costs 2 a tick. 100 ticks with 3 orders: " + 2 * 100 + ". paid for 100 ticks, used for 3 orders.");
    }

    private static void two(Platform platform) {
        System.out.println("TWO. A function per event.");
        int ok = 0;
        for (String id : new String[]{"ORD-1", "ORD-2", "ORD-3"}) {
            Platform.Call c = platform.invoke(FN, "{\"orderId\":\"" + id + "\"}");
            if (!c.failed() && c.body().contains("sent for " + id)) {
                ok++;
            }
        }
        System.out.println("  the function was uploaded to a real Lambda API, and run for each of 3 orders. receipts sent: " + ok + ". the bill at 1 per call: " + ok + ".");
        System.out.println("  between orders nothing has to be running, and nothing is paid for.");
    }

    private static void three(Platform platform) throws Exception {
        System.out.println("THREE. Scale out, and back to zero.");
        waitForZero(platform);
        System.out.println("  before any order, copies running: " + platform.copies() + ".");
        Thread[] threads = new Thread[5];
        AtomicReferenceArray<String> ids = new AtomicReferenceArray<>(5);
        for (int i = 0; i < 5; i++) {
            int n = i;
            threads[i] = new Thread(() -> ids.set(n, platform.invoke(FN, "{\"orderId\":\"C" + n + "\",\"hold\":2}").field("instance")));
            threads[i].start();
        }
        for (Thread t : threads) {
            t.join();
        }
        Set<String> distinct = new HashSet<>();
        for (int i = 0; i < 5; i++) {
            distinct.add(ids.get(i));
        }
        System.out.println("  5 orders at the same moment: distinct copies that answered " + distinct.size() + ", copies running " + platform.copies() + ".");
        waitForZero(platform);
        System.out.println("  " + Platform.IDLE_SECONDS + " quiet seconds later, with no orders: copies running " + platform.copies() + ".");
    }

    private static void four(Platform platform) {
        System.out.println("FOUR. The cold start.");
        Platform.Call cold = platform.invoke(FN, "{\"orderId\":\"ORD-4\"}");
        Platform.Call warm = platform.invoke(FN, "{\"orderId\":\"ORD-5\"}");
        System.out.println("  the first call after a quiet time took " + cold.millis() + " ms, and the call right after it " + warm.millis() + " ms. the cold call was slower: " + (cold.millis() > warm.millis()) + ".");
        System.out.println("  the first call had to start a container for the function, and the second found it running.");
    }

    private static void five(Platform platform) {
        System.out.println("FIVE. No memory between calls.");
        Platform.Call before = platform.invoke(FN, "{\"orderId\":\"ORD-6\"}");
        System.out.println("  a call to the copy that is running: it has handled " + before.field("callsOnThisInstance") + " calls, in copy " + before.field("instance") + ".");
        waitForZero(platform);
        Platform.Call after = platform.invoke(FN, "{\"orderId\":\"ORD-7\"}");
        System.out.println("  after the quiet time: it has handled " + after.field("callsOnThisInstance") + " calls. a different copy answered: " + !before.field("instance").equals(after.field("instance")) + ".");
        System.out.println("  what the first copy kept in its variables went with it. anything that must last goes in a store outside.");
    }

    private static void six(Platform platform) {
        System.out.println("SIX. The bill.");
        System.out.println("  in price units, 100 ticks. quiet, 3 calls: functions " + 3 + ", server " + 200 + ". busy, 300 calls: functions " + 300 + ", server " + 200 + ".");
        System.out.println("  paying per call is cheap when quiet and dear when busy all the time.");
        Platform.Call slow = platform.invoke(FN, "{\"orderId\":\"ORD-8\",\"sleep\":6}");
        System.out.println("  a job that needs 6 seconds, with a limit of 3: failed " + slow.failed() + ", and the platform said: " + (slow.body().contains("Task timed out after 3.00 seconds") ? "Task timed out after 3.00 seconds" : slow.body()) + ".");
    }
}
