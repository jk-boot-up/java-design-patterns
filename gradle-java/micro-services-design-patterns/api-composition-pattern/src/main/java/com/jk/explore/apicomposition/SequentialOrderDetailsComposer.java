package com.jk.explore.apicomposition;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The way everybody writes it first: three calls, one after the other.
 *
 * It is worth being clear that this class is not wrong. It returns exactly the same page
 * as {@link OrderDetailsComposer} whenever all three services are up, and every test in
 * {@code SequentialOrderDetailsComposerTest} passes. That is the trouble with it. Read
 * the code and it looks like three lines of ordinary Java; there is no bug to find, no
 * exception to catch, and nothing a code review would flag.
 *
 * <p>Its two costs only show up in the timeline and in an outage. The page takes the sum
 * of the three latencies rather than the largest, because each call waits for the last
 * one to come back before it starts — and nothing about the second call actually needed
 * the third call's answer. And when the last service fails, the method throws, throwing
 * away the order and the product names that had already arrived. The shopper is shown an
 * error page built out of two perfectly good answers.
 */
public final class SequentialOrderDetailsComposer {

    private final OrderService orders;
    private final CatalogService catalog;
    private final ShippingService shipping;

    public SequentialOrderDetailsComposer(OrderService orders, CatalogService catalog,
                                          ShippingService shipping) {
        this.orders = orders;
        this.catalog = catalog;
        this.shipping = shipping;
    }

    /** The same page, at the sum of three latencies, and all-or-nothing. */
    public OrderDetailsPage pageFor(String orderId) {
        Order order = orders.fetch(orderId);
        Map<String, String> names = catalog.namesFor(order.skus());
        DeliveryStatus delivery = shipping.statusFor(orderId);

        List<OrderDetailsPage.PageLine> lines = new ArrayList<>();
        for (Order.Line line : order.lines()) {
            lines.add(new OrderDetailsPage.PageLine(line.sku(), names.get(line.sku()),
                    line.quantity(), line.lineTotal()));
        }
        return new OrderDetailsPage(order.orderId(), lines, order.total(), delivery,
                List.of());
    }
}
