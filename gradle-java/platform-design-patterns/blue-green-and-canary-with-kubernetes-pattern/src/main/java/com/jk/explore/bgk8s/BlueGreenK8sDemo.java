package com.jk.explore.bgk8s;

public class BlueGreenK8sDemo {

    static final int PORT = 30080;
    static final int PREVIEW = 30081;

    public static void main(String[] args) throws Exception {
        if (!Cluster.toolsAvailable()) {
            System.out.println("This demo needs Docker running, and kind and kubectl on the PATH. Install them, and run it again.");
            return;
        }
        Cluster cluster = new Cluster();
        cluster.create();
        try {
            Traffic live = new Traffic(PORT);
            Traffic.waitUntil(() -> "v1".equals(live.get("/")));
            one(cluster, live);
            two(cluster, live);
            three(cluster, live);
            four(cluster, live);
            five(cluster, live);
            six(cluster);
        } finally {
            if (System.getenv("KEEP_CLUSTER") == null) {
                cluster.delete();
            }
        }
    }

    private static void one(Cluster cluster, Traffic live) {
        System.out.println("ONE. Replace it where it stands.");
        cluster.scale("checkout-v1", 0);
        Traffic.Outcome gap = live.send("/", 20);
        System.out.println("  v1 stopped to make room for v2. 20 requests while nothing is running: failed " + gap.failed() + " of 20.");
        cluster.scale("checkout-v1", 2);
        Traffic.waitUntil(() -> "v1".equals(live.get("/")));
    }

    private static void two(Cluster cluster, Traffic live) {
        System.out.println("TWO. Blue and green.");
        Traffic preview = new Traffic(PREVIEW);
        System.out.println("  v2 is running beside v1, and only a test port reaches it. test request to v2: " + preview.get("/") + ".");
        Traffic.Outcome before = live.send("/", 20);
        cluster.selectVersion("v2");
        Traffic.waitUntil(() -> "v2".equals(live.get("/")));
        Traffic.Outcome after = live.send("/", 20);
        System.out.println("  20 requests before the switch: " + before.answers() + ". the switch is one patch to the service. 20 after: " + after.answers() + ", failed " + (before.failed() + after.failed()) + ".");
        cluster.selectVersion("v1");
        Traffic.waitUntil(() -> "v1".equals(live.get("/")));
    }

    private static void three(Cluster cluster, Traffic live) {
        System.out.println("THREE. Going back.");
        cluster.selectVersion("v2");
        Traffic.waitUntil(() -> "v2".equals(live.get("/")));
        Traffic.Outcome onV2 = live.send("/big", 20);
        System.out.println("  v2 has a bug with big orders. 20 big orders on v2, failed: " + onV2.failed() + ".");
        cluster.selectVersion("v1");
        Traffic.waitUntil(() -> "v1".equals(live.get("/")));
        Traffic.Outcome back = live.send("/big", 20);
        System.out.println("  one patch sent the service back to v1, whose pods had never stopped. 20 big orders, failed: " + back.failed() + ".");
    }

    private static void four(Cluster cluster, Traffic live) {
        System.out.println("FOUR. A canary.");
        cluster.scale("checkout-v1", 9);
        cluster.scale("checkout-v2", 1);
        cluster.selectBoth();
        Traffic.waitUntil(() -> "v2".equals(live.get("/")));
        Traffic.Outcome mix = live.send("/big", 300);
        int share = mix.failed() * 100 / 300;
        System.out.println("  9 pods of v1 and 1 of v2, behind one service. 300 big orders: failed " + mix.failed() + ", which is " + (share >= 2 && share <= 20 ? "a small share, as a canary should be" : "not the small share expected") + ".");
        System.out.println("  the spread is chosen by the cluster's own rules, so the exact count changes from run to run.");
        System.out.println("  had all 300 gone to v2, all 300 would have failed. a few customers found the bug, not everyone.");
    }

    private static void five(Cluster cluster, Traffic live) {
        System.out.println("FIVE. Promote in steps, with a gate.");
        int[][] steps = {{9, 1}, {5, 5}, {0, 10}};
        boolean halted = false;
        int stepsDone = 0;
        for (int[] step : steps) {
            cluster.scale("checkout-v2", step[1]);
            cluster.scale("checkout-v1", step[0]);
            Traffic.waitUntil(() -> "v2".equals(live.get("/")));
            Traffic.Outcome o = live.send("/big", 100);
            stepsDone++;
            if (o.failed() > 5) {
                cluster.scale("checkout-v1", 10);
                cluster.scale("checkout-v2", 0);
                halted = true;
                break;
            }
        }
        System.out.println((stepsDone == 1 ? "  the gate caught it at the first step." : "  the first step was a small sample and missed it. the gate caught it at step " + stepsDone + ", with more traffic."));
        System.out.println("  steps of 1, 5 and 10 pods of v2, and a gate at 5 failures in 100. buggy v2: halted " + halted + ", and every pod is v1 again.");
        Traffic.waitUntil(() -> "v1".equals(live.get("/")) && "v1".equals(live.get("/")));
    }

    private static void six(Cluster cluster) {
        System.out.println("SIX. The bill.");
        cluster.scale("checkout-v1", 2);
        cluster.scale("checkout-v2", 2);
        System.out.println("  during a blue-green switch both releases are fully running: " + cluster.runningPods() + " pods, where one release needs 2.");
        System.out.println("  both releases share one database, so a release that changes the data cannot be switched back safely.");
        System.out.println("  and a cluster is a lot to run for a checkout: a control plane, a node, an image, a service and two deployments.");
    }
}
