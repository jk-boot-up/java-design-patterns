package com.jk.explore.processmanager;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The five acts: services chained together, a process manager, a branch to a partner, a failure path, and the bill.
 */
public final class ProcessManagerDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Each step hands on to the next.");
        Services.Warehouse w1 = new Services.Warehouse("main", Map.of("KETTLE-1", 3));
        Chained chain = new Chained(w1, new Services.Payments(Set.of("CARD-BAD")), new Services.Shipping());
        out.add("  ORD-1: " + chain.fulfil(new Order("ORD-1", "KETTLE-1", "CARD-OK")));
        out.add("  ORD-3, card declined: " + chain.fulfil(new Order("ORD-3", "KETTLE-1", "CARD-BAD")));
        out.add("  kettles in stock: " + w1.stock("KETTLE-1") + " of 3, though only one was shipped");
        out.add("  the warehouse never heard about the decline; and where is ORD-3 now? nobody knows");

        out.add("");
        out.add("TWO. A process manager runs each order's journey.");
        Services.Warehouse main = new Services.Warehouse("main", Map.of("KETTLE-1", 3, "SOFA-1", 0));
        Services.Warehouse partner = new Services.Warehouse("partner", Map.of("SOFA-1", 2));
        Services.Emails emails = new Services.Emails();
        ProcessManager pm = new ProcessManager(main, partner, new Services.Payments(Set.of("CARD-BAD")),
                new Services.Shipping(), emails);
        pm.start(new Order("ORD-1", "KETTLE-1", "CARD-OK"));
        out.add("  ORD-1 replies: " + pm.history("ORD-1") + " -> " + pm.state("ORD-1"));

        out.add("");
        out.add("THREE. The manager decides the next step: a branch.");
        pm.start(new Order("ORD-2", "SOFA-1", "CARD-OK"));
        out.add("  ORD-2 replies: " + pm.history("ORD-2") + " -> " + pm.state("ORD-2"));
        out.add("  main was out of stock, so the manager asked the partner warehouse");

        out.add("");
        out.add("FOUR. The unhappy path is part of the process.");
        pm.start(new Order("ORD-3", "KETTLE-1", "CARD-BAD"));
        out.add("  ORD-3 replies: " + pm.history("ORD-3"));
        out.add("  -> " + pm.state("ORD-3") + "; kettles in stock: " + main.stock("KETTLE-1") + " of 3");
        out.add("  email: " + emails.sent().get(emails.sent().size() - 1));

        out.add("");
        out.add("FIVE. The bill: one brain for every order.");
        out.add("  where is every order? " + pm.allStates());
        out.add("  every route and every branch lives in one class, which grows with each new step");
        out.add("  and its state is in memory: a restart would forget every order in progress");
        return out;
    }

    private ProcessManagerDemo() {
    }
}
