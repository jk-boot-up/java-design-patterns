package com.jk.explore.statetable;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: rules scattered in ifs, the table, wrong moves refused, a new rule, and the bill.
 */
public final class StateTableDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. The rules, scattered across if statements.");
        IfElseOrder a = new IfElseOrder();
        a.pay();
        a.ship();
        a.deliver();
        out.add("  pay, ship, deliver: " + a.status());
        a.cancel();
        out.add("  cancel a delivered order: allowed, now " + a.status());
        IfElseOrder b = new IfElseOrder();
        b.pay();
        b.refund();
        b.refund();
        out.add("  refund, then refund again: allowed, " + b.refunds() + " refunds of £63.44 paid out");

        out.add("");
        out.add("TWO. The rules, in one table.");
        TransitionTable table = TransitionTable.orders();
        table.describe().forEach(row -> out.add("  " + row));
        Order o1 = new Order("ORD-1", table).apply(Action.PAY).apply(Action.SHIP).apply(Action.DELIVER);
        out.add("  ORD-1: " + o1.history());

        out.add("");
        out.add("THREE. A move that is not in the table is refused.");
        try {
            o1.apply(Action.CANCEL);
        } catch (IllegalStateException e) {
            out.add("  cancel ORD-1: refused, " + e.getMessage());
        }
        Order o2 = new Order("ORD-2", table).apply(Action.PAY).apply(Action.REFUND);
        try {
            o2.apply(Action.REFUND);
        } catch (IllegalStateException e) {
            out.add("  refund ORD-2 again: refused, " + e.getMessage());
        }
        out.add("  buttons to show for a PAID order: " + table.allowed(Status.PAID));

        out.add("");
        out.add("FOUR. A new rule: returns.");
        table.allow(Status.DELIVERED, Action.RETURN, Status.RETURNED)
                .allow(Status.RETURNED, Action.REFUND, Status.REFUNDED);
        out.add("  2 lines added to the table; nothing else changed");
        out.add("  buttons for a DELIVERED order: " + table.allowed(Status.DELIVERED));
        o1.apply(Action.RETURN).apply(Action.REFUND);
        out.add("  ORD-1: " + o1.history());

        out.add("");
        out.add("FIVE. The bill: the table says where, not what else.");
        int cells = Status.values().length * Action.values().length;
        out.add("  " + Status.values().length + " statuses x " + Action.values().length + " actions = " + cells
                + " cells; " + table.transitions() + " are allowed moves");
        out.add("  paying the refund and sending the email are still code, hung on each move");
        return out;
    }

    private StateTableDemo() {
    }
}
