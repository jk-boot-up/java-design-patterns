package com.jk.explore.cqrs;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The order history page composed from scratch, on every single view.
 *
 * This is the previous project's answer, and it is a good answer — for a page that is
 * looked at occasionally. Here it is being used for a page a customer refreshes while
 * waiting for a parcel, and the arithmetic turns against it: every view pays for a call to
 * Orders and a call to Catalog, and every view produces a page identical to the last one.
 *
 * <p>It is also always up to the second, which is the one thing a read model cannot
 * promise. That is not a small point in its favour.
 */
public final class ComposingOrderHistory {

    private final OrdersQueryApi orders;
    private final CatalogService catalog;

    public ComposingOrderHistory(OrdersQueryApi orders, CatalogService catalog) {
        this.orders = orders;
        this.catalog = catalog;
    }

    /** The page, assembled again from two services. */
    public List<OrderHistoryRow> historyFor(String customerId) {
        List<Order> theirOrders = orders.ordersFor(customerId);
        if (theirOrders.isEmpty()) {
            return List.of();
        }

        List<String> skus = theirOrders.stream()
                .flatMap(order -> order.skus().stream()).distinct().toList();
        Map<String, String> names = catalog.namesFor(skus);

        List<OrderHistoryRow> rows = new ArrayList<>();
        for (Order order : theirOrders) {
            for (Order.Line line : order.lines()) {
                rows.add(new OrderHistoryRow(order.orderId(), line.sku(),
                        names.get(line.sku()), line.quantity(), line.lineTotal(),
                        order.placedAtMillis()));
            }
        }
        return rows;
    }
}
