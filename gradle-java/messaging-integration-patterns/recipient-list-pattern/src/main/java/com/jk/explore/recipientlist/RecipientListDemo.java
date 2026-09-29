package com.jk.explore.recipientlist;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * The five acts: send everything everywhere, a recipient list, rules that add recipients, a changed table, and the bill.
 */
public final class RecipientListDemo {

    static final List<Order> ORDERS = List.of(
            new Order("ORD-1", List.of("kitchen", "furniture"), 42000, false),
            new Order("ORD-2", List.of("kitchen"), 3000, true),
            new Order("ORD-3", List.of("chilled"), 1200, false),
            new Order("ORD-4", List.of("furniture", "chilled"), 65000, false),
            new Order("ORD-5", List.of("kitchen", "chilled"), 2500, false));

    static final List<String> WAREHOUSES = List.of("north", "south", "big-items", "cold-store");

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static RecipientList standard() {
        return new RecipientList()
                .stocks("kitchen", "north").stocks("furniture", "big-items").stocks("chilled", "cold-store");
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Every order sent to every warehouse.");
        Inboxes everywhere = new Inboxes();
        int useful = 0;
        for (Order o : ORDERS) {
            for (String w : WAREHOUSES) {
                everywhere.deliver(w, o);
            }
            useful += standard().recipientsFor(o).size();
        }
        out.add("  " + ORDERS.size() + " orders x " + WAREHOUSES.size() + " warehouses = " + everywhere.total()
                + " deliveries; " + useful + " of them needed");
        out.add("  every warehouse sorts through orders it has nothing to do with");

        out.add("");
        out.add("TWO. A recipient list: each order goes where its items are.");
        RecipientList list = standard();
        Inboxes inboxes = new Inboxes();
        for (Order o : ORDERS) {
            list.send(o, inboxes);
            out.add("  " + o.id() + " " + o.categories() + " -> " + list.recipientsFor(o));
        }
        out.add("  deliveries: " + inboxes.total());

        out.add("");
        out.add("THREE. Rules add recipients: fraud review over £500, gift wrap for gifts.");
        list.rule(o -> o.pence() > 50000 ? Optional.of("fraud-review") : Optional.empty())
                .rule(o -> o.gift() ? Optional.of("gift-wrap") : Optional.empty());
        out.add("  ORD-4 (£650.00) -> " + list.recipientsFor(ORDERS.get(3)));
        out.add("  ORD-2 (a gift)  -> " + list.recipientsFor(ORDERS.get(1)));

        out.add("");
        out.add("FOUR. The table changes while the shop runs.");
        list.stocks("kitchen", "south");
        out.add("  north closes for stocktake; kitchen items now come from south");
        out.add("  ORD-5 -> " + list.recipientsFor(ORDERS.get(4)) + "; checkout was not changed");

        out.add("");
        out.add("FIVE. The bill: the list knows everyone, and a send can half-fail.");
        Inboxes partly = new Inboxes();
        partly.takeDown("big-items");
        List<String> failed = list.send(ORDERS.get(0), partly);
        out.add("  big-items is unreachable; ORD-1 reached " + partly.all().keySet() + ", failed " + failed);
        out.add("  half an order is out; the list must retry or undo, and it must know every destination's job");
        return out;
    }

    private RecipientListDemo() {
    }
}
