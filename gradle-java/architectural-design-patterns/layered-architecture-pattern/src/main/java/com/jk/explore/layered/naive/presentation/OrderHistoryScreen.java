package com.jk.explore.layered.naive.presentation;

import com.jk.explore.layered.domain.Order;
import com.jk.explore.layered.infrastructure.InMemoryOrderTable;

/**
 * The second naive version, and the one that matters — because this is what most
 * codebases calling themselves "layered" actually are.
 *
 * <p>The layers all exist. There are four packages with the right names and a
 * diagram on a wall somewhere. And then somebody needed a screen listing a
 * customer's past orders, and the application layer did not have a method for
 * it, and adding one would have meant a request object, a result object and a
 * service method — three files to return some rows that were <em>right
 * there</em>. So the screen took the storage class directly. It was ten minutes
 * instead of an afternoon, it worked, the tests passed, and it shipped.
 *
 * <p><strong>Nothing in the build objected.</strong> That sentence is the whole
 * lesson of this project. This class compiles. It is not a hack, it has no
 * warning suppressed, and a reviewer skimming a diff would see a small, tidy,
 * readable screen. Layering as it is usually practised is a convention, and a
 * convention that nothing checks is a convention that decays — not all at once,
 * but one reasonable Tuesday at a time.
 *
 * <p>And then it costs. Look at the second import: not the {@code OrderTable}
 * interface, but {@code InMemoryOrderTable}, the concrete class, because that
 * was what was in the variable being copied. When this project replaces its
 * storage layer — the forced change, further down — every class that went
 * through the application layer needs nothing done to it, and <em>this one will
 * not compile</em>. It cannot be handed the new store. The bill for the ten
 * minutes arrives, with interest, on a day nobody remembers the ten minutes.
 *
 * <p>This class is left here on purpose, and the architecture test is deliberately
 * scoped so it passes while this exists. The companion test then runs the same
 * rule over this package and shows it going red, naming this class by name.
 */
public class OrderHistoryScreen {

    private final InMemoryOrderTable orders;

    public OrderHistoryScreen(InMemoryOrderTable orders) {
        this.orders = orders;
    }

    public String history(String customerId) {
        StringBuilder out = new StringBuilder();
        for (Order order : orders.all()) {
            if (order.customerId().equals(customerId)) {
                out.append(order.id()).append(" ").append(order.total()).append("\n");
            }
        }
        return out.isEmpty() ? "No orders yet.\n" : out.toString();
    }
}
