package com.jk.explore.servicemesh;

import java.util.Set;

public class ServiceMeshDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. Each service carries its own.");
        LibraryClient a = new LibraryClient("checkout", 3);
        LibraryClient b = new LibraryClient("refunds", 0);
        LibraryClient c = new LibraryClient("reports", 1);
        System.out.println("  the payment service refuses its first 2 calls. checkout retries 3 times: " + a.call(new Flaky(2)) + ". refunds never retries: " + b.call(new Flaky(2)) + ". reports retries once: " + c.call(new Flaky(2)) + ".");
        System.out.println("  three services, three copies of the retry code, three different behaviours.");
    }

    private static void two() {
        System.out.println("TWO. A proxy beside each service.");
        Mesh mesh = new Mesh();
        mesh.register("payments", new Flaky(2));
        mesh.setRetries(3);
        boolean ok = mesh.call("checkout", "payments");
        System.out.println("  the same bad day, the same policy for everyone: the call " + (ok ? "worked" : "failed") + ", attempts made by the proxy: " + mesh.report() + ".");
        System.out.println("  the checkout service has no retry code at all.");
    }

    private static void three() {
        System.out.println("THREE. Change the policy once.");
        Mesh before = new Mesh();
        before.register("payments", new Flaky(2));
        before.setRetries(3);
        Mesh after = new Mesh();
        after.register("payments", new Flaky(2));
        after.setRetries(0);
        System.out.println("  retries 3: " + before.call("checkout", "payments") + ". one setting changed to 0: " + after.call("checkout", "payments") + ".");
        System.out.println("  every service's calls changed. services redeployed: 0.");
    }

    private static void four() {
        System.out.println("FOUR. Who is calling.");
        Mesh mesh = new Mesh();
        Flaky payments = new Flaky(0);
        mesh.register("payments", payments);
        mesh.allowOnly("payments", Set.of("checkout", "refunds"));
        System.out.println("  checkout calls payments: " + mesh.call("checkout", "payments") + ". an unknown service calls payments: " + mesh.call("gift-cards", "payments") + ".");
        System.out.println("  the payment service received " + payments.received() + " call. the proxy turned the other one away before it got there. denied: " + mesh.denied() + ".");
    }

    private static void five() {
        System.out.println("FIVE. Numbers for free.");
        Mesh mesh = new Mesh();
        mesh.register("payments", new Flaky(2));
        mesh.setRetries(3);
        mesh.call("checkout", "payments");
        mesh.call("checkout", "payments");
        mesh.call("refunds", "payments");
        for (String line : mesh.report()) {
            System.out.println("  " + line + ".");
        }
        System.out.println("  no service counted anything. the proxies did.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Mesh mesh = new Mesh();
        Flaky payments = new Flaky(2);
        mesh.register("payments", payments);
        mesh.register("checkout", new Flaky(0));
        mesh.register("refunds", new Flaky(0));
        mesh.setRetries(3);
        mesh.call("checkout", "payments");
        System.out.println("  one call, with 2 refusals: the payment service received " + payments.received() + " calls. retrying multiplies the load on a service that is already struggling.");
        System.out.println("  one attempt takes " + Mesh.TICKS_THROUGH_PROXIES + " ticks through the proxies, and " + Mesh.TICKS_DIRECT + " directly. this call took " + mesh.ticks() + " ticks.");
        System.out.println("  and " + mesh.proxies() + " services means " + mesh.proxies() + " more processes to run, upgrade and understand.");
    }
}
