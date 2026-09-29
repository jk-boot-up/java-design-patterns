package com.jk.explore.healthcheck;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: an open port, liveness, readiness, a liveness check that is too deep, and the bill.
 */
public final class HealthEndpointDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Three checkout instances: each has its own database; all share payments and recommendations. */
    static final class Shop {
        final Dependency payments = new Dependency("payments", true);
        final Dependency recommendations = new Dependency("recommendations", false);
        final List<Instance> instances = new ArrayList<>();

        Shop() {
            for (String n : List.of("A", "B", "C")) {
                instances.add(new Instance(n, List.of(new Dependency("database", true), payments, recommendations)));
            }
        }

        Instance get(String name) {
            return instances.stream().filter(i -> i.name().equals(name)).findFirst().orElseThrow();
        }

        Dependency database(String name) {
            return get(name).dependencies().get(0);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. An open port is not a healthy service.");
        Shop s1 = new Shop();
        s1.get("B").setStuck(true);
        LoadBalancer byPort = new LoadBalancer(s1.instances, Instance::portOpen);
        out.add("  instance B is stuck, but its port is open");
        out.add("  load balancer checks the port: in rotation " + byPort.inRotation());
        out.add("  9 orders sent: " + byPort.send(9) + " failed");

        out.add("");
        out.add("TWO. A liveness endpoint: is the process working?");
        s1.instances.forEach(i -> out.add("  GET " + i.name() + "/health/live: " + HealthEndpoint.live(i)));
        LoadBalancer byHealth = new LoadBalancer(s1.instances, i -> HealthEndpoint.ready(i).code() == 200);
        out.add("  in rotation " + byHealth.inRotation() + "; 9 orders sent: " + byHealth.send(9) + " failed");
        Restarter restarter = new Restarter(HealthEndpoint::live);
        for (int round = 0; round < 3; round++) {
            restarter.checkAll(s1.instances);
        }
        out.add("  after 3 failed checks, B is restarted: now " + HealthEndpoint.live(s1.get("B"))
                + ", back in rotation " + byHealth.inRotation());

        out.add("");
        out.add("THREE. A readiness endpoint: can it take orders right now?");
        Shop s2 = new Shop();
        s2.database("C").setUp(false);
        s2.recommendations.setUp(false);
        s2.instances.forEach(i -> out.add("  GET " + i.name() + "/health/ready: " + HealthEndpoint.ready(i)));
        out.add("  C/health/live: " + HealthEndpoint.live(s2.get("C")) + ", so C is not restarted");
        LoadBalancer ready = new LoadBalancer(s2.instances, i -> HealthEndpoint.ready(i).code() == 200);
        out.add("  in rotation " + ready.inRotation() + "; 9 orders sent: " + ready.send(9)
                + " failed, without recommendations");

        out.add("");
        out.add("FOUR. The payment provider is down for 30 seconds.");
        Shop shallow = new Shop();
        Shop deep = new Shop();
        shallow.payments.setUp(false);
        deep.payments.setUp(false);
        Restarter r1 = new Restarter(HealthEndpoint::live);
        Restarter r2 = new Restarter(HealthEndpoint::deepLive);
        for (int round = 0; round < 3; round++) {
            r1.checkAll(shallow.instances);
            r2.checkAll(deep.instances);
        }
        out.add("  liveness that checks payments too: " + restarts(deep) + " of 3 instances restarted");
        out.add("  liveness that checks only the process: " + restarts(shallow) + " restarted");
        out.add("  restarting checkout cannot fix the payment provider");

        out.add("");
        out.add("FIVE. The bill: checks cost calls, and say too much.");
        Shop s3 = new Shop();
        LoadBalancer lb = new LoadBalancer(s3.instances, i -> HealthEndpoint.ready(i).code() == 200);
        for (int round = 0; round < 6; round++) {
            lb.inRotation();
        }
        int calls = s3.instances.stream().flatMap(i -> i.dependencies().stream()).distinct()
                .mapToInt(Dependency::checks).sum();
        out.add("  readiness every 10 s on 3 instances: " + calls + " dependency calls a minute, before any order");
        out.add("  and \"database down\" tells an attacker what to aim at: keep details off the public address");
        return out;
    }

    private static long restarts(Shop shop) {
        return shop.instances.stream().filter(i -> i.restarts() > 0).count();
    }

    private HealthEndpointDemo() {
    }
}
