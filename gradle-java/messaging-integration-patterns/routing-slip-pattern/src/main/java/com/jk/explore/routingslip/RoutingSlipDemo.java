package com.jk.explore.routingslip;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: one fixed pipeline, routing slips, steps that know nothing of each other, a new step, and the bill.
 */
public final class RoutingSlipDemo {

    static List<OrderMessage> orders() {
        return List.of(
                new OrderMessage("ORD-1", 3000, false, false, "UK"),
                new OrderMessage("ORD-2", 4500, true, false, "UK"),
                new OrderMessage("ORD-3", 2500, false, true, "UK"),
                new OrderMessage("ORD-4", 62000, false, false, "FR"));
    }

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. One fixed pipeline for every order.");
        FixedPipeline fixed = new FixedPipeline();
        orders().forEach(fixed::process);
        out.add("  " + orders().size() + " orders x " + FixedPipeline.EVERY_STEP.size() + " steps = " + fixed.visits()
                + " visits; " + fixed.useful() + " did any work");
        out.add("  every step starts with \"does this apply to me?\"");

        out.add("");
        out.add("TWO. A routing slip: each order carries its own route.");
        RoutingSlip router = new RoutingSlip();
        for (OrderMessage m : orders()) {
            out.add("  " + m.id() + " slip: " + router.slipFor(m));
        }

        out.add("");
        out.add("THREE. Each step does its job and passes to the next on the slip.");
        RoutingSlip router2 = new RoutingSlip();
        List<OrderMessage> run = orders();
        run.forEach(router2::route);
        out.add("  " + router2.visits() + " visits in all, every one doing work");
        out.add("  ORD-2 went: " + run.get(1).visitedSteps());
        out.add("  no step knows which step comes after it");

        out.add("");
        out.add("FOUR. A new step: fraud check for orders over £500.");
        router.addRule(m -> m.pence() > 50000 ? List.of("fraud-check") : List.of());
        out.add("  ORD-4 slip: " + router.slipFor(orders().get(3)));
        out.add("  ORD-1 slip: " + router.slipFor(orders().get(0)) + " (unchanged)");
        out.add("  one rule added where slips are written; no step changed");

        out.add("");
        out.add("FIVE. The bill: the route is fixed when the order sets off.");
        OrderMessage knife = new OrderMessage("ORD-5", 1800, false, true, "UK");
        knife.failAgeCheck();
        out.add("  ORD-5 fails its age check: " + new RoutingSlip().route(knife));
        out.add("  a slip can stop, but it cannot choose a new route from what happened on the way;");
        out.add("  that needs a process manager");
        return out;
    }

    private RoutingSlipDemo() {
    }
}
