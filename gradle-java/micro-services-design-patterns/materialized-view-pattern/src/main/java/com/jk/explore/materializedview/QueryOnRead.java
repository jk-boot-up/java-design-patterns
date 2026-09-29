package com.jk.explore.materializedview;

import java.util.ArrayList;
import java.util.List;

/**
 * The page without the pattern: asks all three services every time someone opens it.
 */
public final class QueryOnRead {

    private final Services services;

    public QueryOnRead(Services services) {
        this.services = services;
    }

    public List<HistoryRow> myOrders(String customerId) {
        List<HistoryRow> rows = new ArrayList<>();
        for (Event.OrderPlaced o : services.ordersOf(customerId)) {
            String status = services.isShipped(o.orderId()) ? "shipped" : "placed";
            rows.add(new HistoryRow(o.orderId(), services.productName(o.productId()), o.quantity(), status));
        }
        return rows;
    }
}
