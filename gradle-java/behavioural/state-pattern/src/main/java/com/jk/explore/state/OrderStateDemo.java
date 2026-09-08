package com.jk.explore.state;

import java.util.List;

/**
 * Runnable walkthrough of the State pattern.
 *
 * <p>Section 1 shows a status field and three chains of conditionals paying a
 * customer twice. Sections 2 to 4 show the same lifecycle as one class per
 * state. Section 5 says what that cost.
 */
public final class OrderStateDemo {

    private static final Money HEADPHONES = Money.pounds(89.99);
    private static final Money CABLE = Money.pounds(7.50);

    public static void main(String[] args) {
        theTrap();
        theHappyPath();
        theRefusals();
        theButtons();
        whatItCost();
    }

    // --- 1 -----------------------------------------------------------------

    private static void theTrap() {
        System.out.println("=== 1. The trap: one rule, written out in three chains ===");
        System.out.println();

        NaiveOrder shipped = new NaiveOrder("N-9001", Money.pounds(89.99));
        shipped.pay();
        shipped.pack();
        shipped.ship();

        System.out.println("  A SHIPPED order, and the screen the agent is looking at:");
        System.out.println("    status          : " + shipped.status());
        System.out.println("    buttons drawn   : " + shipped.allowedActions());

        shipped.cancel("customer changed their mind");
        System.out.println("    cancel() anyway : accepted — status is now " + shipped.status());
        System.out.println("    ledger          : " + shipped.ledger());
        System.out.println("  The parcel is on a van and the customer has their money back.");
        System.out.println();

        NaiveOrder twice = new NaiveOrder("N-9002", Money.pounds(97.49));
        twice.pay();
        twice.cancel("out of stock");
        System.out.println("  A CANCELLED order, already refunded once:");
        System.out.println("    ledger          : " + twice.ledger());
        twice.refund("support ticket 4471");
        System.out.println("    refund() anyway : accepted — status is now " + twice.status());
        System.out.println("    ledger          : " + twice.ledger());
        System.out.printf("    the shop is out : %s over %d refunds%n",
                twice.ledger().net(), twice.ledger().refundCount());
        System.out.println();
        System.out.println("  Both are one condition, in a chain that was copied and then edited.");
        System.out.println();
    }

    // --- 2 -----------------------------------------------------------------

    private static void theHappyPath() {
        System.out.println("=== 2. The pattern: one class per state ===");
        System.out.println();

        Order order = order("A-1001", "grace@example.com");
        System.out.println("  " + order);
        order.pay();
        order.pack();
        order.ship();
        order.deliver();

        System.out.println("  history:");
        order.history().forEach(e -> System.out.println("    " + e));
        System.out.println("    ledger   : " + order.ledger());
        System.out.println();
        System.out.println("  Order has no switch and no status checks. Every one of its");
        System.out.println("  methods is a single delegation, and the state decides.");
        System.out.println();
    }

    // --- 3 -----------------------------------------------------------------

    private static void theRefusals() {
        System.out.println("=== 3. The refusals, and where they come from ===");
        System.out.println();

        Order shipped = order("A-1002", "priya@example.com");
        shipped.pay();
        shipped.pack();
        shipped.ship();
        attempt(shipped, "cancel", () -> shipped.cancel("customer changed their mind"));
        System.out.println();

        Order cancelled = order("A-1003", "leo@example.com");
        cancelled.pay();
        cancelled.cancel("out of stock");
        System.out.println("  A-1003, paid and then cancelled:");
        System.out.println("    ledger after cancel : " + cancelled.ledger());
        attempt(cancelled, "refund", () -> cancelled.refund("support ticket 4471"));
        System.out.println("    ledger unchanged    : " + cancelled.ledger());
        System.out.println();

        System.out.println("  Neither refusal is written down anywhere as a rule.");
        System.out.println("  CancelledState simply does not override refund, and the");
        System.out.println("  default in the interface says no. The refusals are recorded:");
        cancelled.history().stream().filter(OrderEvent::wasRefused)
                .forEach(e -> System.out.println("    " + e));
        System.out.println();
    }

    private static void attempt(Order order, String action, Runnable request) {
        System.out.printf("  %s, asked to %s:%n", order.id() + " (" + order.status() + ")", action);
        try {
            request.run();
            System.out.println("    accepted — now " + order.status());
        } catch (IllegalTransitionException e) {
            System.out.println("    refused: " + e.getMessage());
        }
    }

    // --- 4 -----------------------------------------------------------------

    private static void theButtons() {
        System.out.println("=== 4. Which buttons to draw ===");
        System.out.println();

        Order order = order("A-1004", "sam@example.com");
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        order.pay();
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        order.pack();
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        order.ship();
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        order.deliver();
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        order.refund("faulty on arrival");
        System.out.printf("    %-10s %s%n", order.status(), order.allowedActions());
        System.out.println();
        System.out.println("  One call, no conditionals, and it cannot disagree with the");
        System.out.println("  methods — the answers and the buttons live in the same class.");
        System.out.println();

        // A state that does not exist in src/main. Order was compiled without
        // it and needs no change; nor does any other state.
        OrderState awaitingCollection = new OrderState() {
            @Override
            public String name() {
                return "AT-LOCKER";
            }

            @Override
            public List<String> allowedActions() {
                return List.of("deliver");
            }

            @Override
            public void deliver(Order order) {
                order.transitionTo(DeliveredState.INSTANCE, "deliver",
                        "collected from the Bristol locker");
            }
        };

        Order locker = order("A-1005", "mia@example.com");
        locker.pay();
        locker.pack();
        locker.transitionTo(awaitingCollection, "hand over", "left at the Bristol locker");
        System.out.printf("    %-10s %s%n", locker.status(), locker.allowedActions());
        attempt(locker, "cancel", () -> locker.cancel("changed their mind"));
        locker.deliver();
        System.out.println("    delivered  " + locker.history().get(locker.history().size() - 1));
        System.out.println();
        System.out.println("  An eighth state, declared in this demo file. Order did not change.");
        System.out.println("  Neither did any other state — except the one that has to point");
        System.out.println("  at it, and that is the honest cost, in section 5.");
        System.out.println();
    }

    // --- 5 -----------------------------------------------------------------

    private static void whatItCost() {
        System.out.println("=== 5. What it cost ===");
        System.out.println();
        System.out.println("  Seven classes where there was one enum, and the transition");
        System.out.println("  table no longer exists anywhere you can read it — it is");
        System.out.println("  distributed across the states, one arrow at a time. Adding");
        System.out.println("  AT-LOCKER above meant editing whichever state hands over to");
        System.out.println("  it. For a small, stable machine an enum and a map of");
        System.out.println("  permitted transitions is often clearer, and you should use it.");
        System.out.println();
        System.out.println("  Use this when the BEHAVIOUR varies by state, not just the");
        System.out.println("  permissions — when cancelling a PAID order and a PACKED one");
        System.out.println("  do genuinely different work, as they do here.");
    }

    private static Order order(String id, String email) {
        return new Order(id, email, List.of(
                new OrderLine("H-100", "Wireless headphones", HEADPHONES, 1),
                new OrderLine("C-220", "USB-C cable", CABLE, 1)));
    }

    private OrderStateDemo() {
    }
}
