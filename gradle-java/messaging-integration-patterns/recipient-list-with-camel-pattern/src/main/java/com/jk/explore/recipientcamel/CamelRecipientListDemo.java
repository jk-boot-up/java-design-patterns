package com.jk.explore.recipientcamel;

import java.util.ArrayList;
import java.util.List;
import org.apache.camel.CamelContext;
import org.apache.camel.CamelExecutionException;
import org.apache.camel.ProducerTemplate;
import org.apache.camel.impl.DefaultCamelContext;

/**
 * The five acts, with Apache Camel's recipientList().
 */
public final class CamelRecipientListDemo {

    static final List<Order> ORDERS = List.of(
            new Order("ORD-1", List.of("kitchen", "furniture"), 42000, false),
            new Order("ORD-2", List.of("kitchen"), 3000, true),
            new Order("ORD-3", List.of("chilled"), 1200, false),
            new Order("ORD-4", List.of("furniture", "chilled"), 65000, false),
            new Order("ORD-5", List.of("kitchen", "chilled"), 2500, false));

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        Warehouses warehouses = new Warehouses();
        RoutingTable table = new RoutingTable();
        try (CamelContext camel = new DefaultCamelContext()) {
            camel.addRoutes(new ShopRoutes(warehouses, table));
            camel.start();
            ProducerTemplate send = camel.createProducerTemplate();

            out.add("ONE. multicast(): every order to every warehouse.");
            ORDERS.forEach(o -> send.sendBody("direct:everyone", o));
            out.add("  " + ORDERS.size() + " orders x 4 warehouses = " + warehouses.deliveries() + " deliveries");

            out.add("");
            out.add("TWO. recipientList(method(table, \"recipients\")): each order goes where its items are.");
            warehouses.clear();
            for (Order o : ORDERS) {
                out.add("  " + o.id() + " " + o.categories() + " -> " + table.recipients(o).replace("direct:", ""));
                send.sendBody("direct:orders", o);
            }
            out.add("  deliveries: " + warehouses.deliveries());

            out.add("");
            out.add("THREE. The same table adds recipients: fraud review over £500, gift wrap for gifts.");
            out.add("  ORD-4 (£650.00) reached " + warehouses.reached("ORD-4"));
            out.add("  ORD-2 (a gift)  reached " + warehouses.reached("ORD-2"));

            out.add("");
            out.add("FOUR. The table changes while the routes run.");
            table.assign("kitchen", "south");
            warehouses.clear();
            send.sendBody("direct:orders", ORDERS.get(4));
            out.add("  north closes for stocktake; kitchen now from south: ORD-5 reached " + warehouses.reached("ORD-5"));
            out.add("  no route was changed or restarted");

            out.add("");
            out.add("FIVE. The bill: one recipient fails.");
            warehouses.clear();
            warehouses.setDown("big-items");
            try {
                send.sendBody("direct:orders", ORDERS.get(0));
            } catch (CamelExecutionException e) {
                out.add("  Camel reports: " + rootMessage(e));
            }
            out.add("  ORD-1 still reached " + warehouses.reached("ORD-1") + ": half an order is out");
            out.add("  Camel tells you it failed; retrying or undoing the half that went out is still your job");
        }
        return out;
    }

    private static String rootMessage(Throwable e) {
        Throwable t = e;
        while (t.getCause() != null) {
            t = t.getCause();
        }
        return t.getMessage();
    }

    private CamelRecipientListDemo() {
    }
}
