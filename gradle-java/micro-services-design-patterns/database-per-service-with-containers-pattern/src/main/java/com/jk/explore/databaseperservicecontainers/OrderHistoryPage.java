package com.jk.explore.databaseperservicecontainers;

import com.mongodb.MongoException;
import java.util.ArrayList;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;

/**
 * The join, now written in Java. Ask Orders what the customer bought; collect the skus;
 * ask Catalog for their names in one call; put the two answers side by side.
 *
 * <p>It also has to decide what to show when a name is missing — because the product was
 * deleted, or because the Catalog cannot be reached at all. A SQL join never had to decide
 * either thing.
 */
public class OrderHistoryPage {

    public static final String DELETED = "(no longer in the catalogue)";
    public static final String UNREACHABLE = "(catalog unreachable)";

    private final OrderService orders;
    private final CatalogService catalog;

    public OrderHistoryPage(OrderService orders, CatalogService catalog) {
        this.orders = orders;
        this.catalog = catalog;
    }

    public List<OrderHistoryRow> forCustomer(String customerId) {
        List<Order> bought = orders.ordersFor(customerId);
        Set<String> skus = new LinkedHashSet<>();
        for (Order o : bought) {
            skus.add(o.sku());
        }
        Map<String, String> names;
        boolean reached = true;
        try {
            names = catalog.namesFor(skus);
        } catch (MongoException unreachable) {
            names = Map.of();
            reached = false;
        }
        List<OrderHistoryRow> rows = new ArrayList<>();
        for (Order o : bought) {
            String name = names.get(o.sku());
            if (name == null) {
                name = reached ? DELETED : UNREACHABLE;
            }
            rows.add(new OrderHistoryRow(o.orderId(), o.sku(), name, o.quantity()));
        }
        return rows;
    }
}
