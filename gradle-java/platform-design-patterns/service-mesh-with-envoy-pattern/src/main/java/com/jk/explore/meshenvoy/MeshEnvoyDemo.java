package com.jk.explore.meshenvoy;

import java.util.List;

public class MeshEnvoyDemo {

    public static void main(String[] args) throws Exception {
        if (!Envoy.toolsAvailable()) {
            System.out.println("This demo needs Docker running, and the Envoy image. Start Docker, and run it again.");
            return;
        }
        try (Payments payments = new Payments(); Envoy envoy = new Envoy(payments.port())) {
            one(payments);
            envoy.start(3, List.of());
            two(payments, envoy);
            three(payments, envoy);
            four(payments, envoy);
            five(payments, envoy);
            six(payments, envoy);
        }
    }

    private static void one(Payments payments) {
        System.out.println("ONE. Each service carries its own.");
        String direct = "http://127.0.0.1:" + payments.port() + "/charge";
        Caller[] callers = {new Caller("checkout", 3), new Caller("refunds", 0), new Caller("reports", 1)};
        StringBuilder line = new StringBuilder();
        for (Caller c : callers) {
            payments.badDay(2);
            line.append(c.name()).append(" ").append(c.call(direct) ? "worked" : "failed").append(", ");
        }
        System.out.println("  the payment service refuses its first 2 calls, for each caller in turn. with retry code of 3, 0 and 1 tries: " + line.substring(0, line.length() - 2) + ".");
        System.out.println("  three services, three copies of the retry code, three different behaviours.");
    }

    private static void two(Payments payments, Envoy envoy) {
        System.out.println("TWO. A proxy beside the service.");
        payments.badDay(2);
        boolean ok = new Caller("checkout", 0).call(envoy.url());
        System.out.println("  Envoy is told to retry 5xx answers up to 3 times. the checkout has no retry code. the call " + (ok ? "worked" : "failed")
                + ". the payment service received " + payments.received() + " calls, and Envoy counts " + envoy.counter("cluster.payments.upstream_rq_retry") + " retries.");
    }

    private static void three(Payments payments, Envoy envoy) throws Exception {
        System.out.println("THREE. Change the policy once.");
        envoy.start(0, List.of());
        payments.badDay(2);
        boolean ok = new Caller("checkout", 0).call(envoy.url());
        System.out.println("  one setting in Envoy's configuration changed, from 3 retries to 0. the same call " + (ok ? "worked" : "failed") + ". services changed or redeployed: 0.");
    }

    private static void four(Payments payments, Envoy envoy) throws Exception {
        System.out.println("FOUR. Who is calling.");
        envoy.start(3, List.of("checkout", "refunds"));
        payments.badDay(0);
        int allowed = new Caller("checkout", 0).status(envoy.url());
        int denied = new Caller("gift-cards", 0).status(envoy.url());
        System.out.println("  only checkout and refunds are allowed. checkout: status " + allowed + ". gift-cards: status " + denied + ".");
        System.out.println("  the payment service received " + payments.received() + " call. the proxy turned the other one away before it got there.");
        System.out.println("  here the caller's name is a header. a real mesh checks a certificate instead, which a service cannot forge.");
    }

    private static void five(Payments payments, Envoy envoy) throws Exception {
        System.out.println("FIVE. Numbers for free.");
        envoy.start(3, List.of());
        payments.badDay(2);
        new Caller("checkout", 0).call(envoy.url());
        System.out.println("  read from Envoy, and not from any service: requests to payments " + envoy.counter("cluster.payments.upstream_rq_total")
                + ", retries " + envoy.counter("cluster.payments.upstream_rq_retry") + ", retries that ended in success " + envoy.counter("cluster.payments.upstream_rq_retry_success") + ".");
        System.out.println("  no service counted anything. the proxy did.");
    }

    private static void six(Payments payments, Envoy envoy) throws Exception {
        System.out.println("SIX. The bill.");
        envoy.start(3, List.of());
        payments.badDay(2);
        new Caller("checkout", 0).call(envoy.url());
        System.out.println("  one call, with 2 refusals: the payment service received " + payments.received() + " calls. retrying multiplies the load on a service that is already struggling.");
        System.out.println("  every call now crosses a proxy, which is a second process and a second network hop. this demo needed 1 more container for 1 service.");
        System.out.println("  and the policy is in a configuration file of about " + Envoy.configuration(payments.port(), 3, List.of("checkout")).lines().count() + " lines, that someone must read, and keep right.");
    }
}
