package com.jk.explore.databaseperservice;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * One database holding both services' tables. The way it usually starts.
 *
 * It is important to be fair to this arrangement, because it is genuinely good at
 * several things. The order history page is one query. The join is done by a database
 * engine that is extremely good at joins. A product referenced by an order is
 * guaranteed to exist, because a foreign key says so. Reports are easy. Nothing is
 * eventually consistent. If a shop can live here, it should.
 *
 * <p>What it cannot do is let the two teams move independently, and this class shows
 * exactly why. The product name is stored under a column name, the order history
 * query names that column, and the catalog team owns neither the query nor any
 * knowledge that it exists.
 */
public final class SharedSchema {

    /** The column the order history query asks for by name. */
    public static final String PRODUCT_NAME_COLUMN = "product_name";

    private final List<Order> orders = new ArrayList<>();
    /** sku -> (column name -> value), so that a column can be renamed. */
    private final Map<String, Map<String, String>> products = new LinkedHashMap<>();

    public void addOrder(Order order) {
        orders.add(order);
    }

    public void addProduct(String sku, String name) {
        products.put(sku, new LinkedHashMap<>(Map.of(PRODUCT_NAME_COLUMN, name)));
    }

    /**
     * What the catalog team does on a Tuesday, for perfectly good reasons of their
     * own: {@code product_name} becomes {@code title}.
     *
     * They have no way of knowing that the order history page reads this column. It is
     * not in their code, not in their tests, and not in their repository.
     */
    public void renameProductNameColumnTo(String newName) {
        for (Map<String, String> row : products.values()) {
            String value = row.remove(PRODUCT_NAME_COLUMN);
            if (value != null) {
                row.put(newName, value);
            }
        }
    }

    /**
     * The order history page, as one query with a join across both tables.
     *
     * One trip, no assembly, no missing names, and the rows come back in order. This
     * is the method the rest of the category spends its time replacing, so it is worth
     * appreciating first.
     *
     * @throws ColumnNotFoundException if somebody renamed a column this query names
     */
    public List<OrderHistoryRow> orderHistory(String customerId) {
        List<OrderHistoryRow> rows = new ArrayList<>();
        for (Order order : orders) {
            if (!order.customerId().equals(customerId)) {
                continue;
            }
            Map<String, String> product = products.get(order.sku());
            if (product == null) {
                // A foreign key makes this unreachable, which is precisely the point.
                throw new IllegalStateException("no product row for " + order.sku());
            }
            String name = product.get(PRODUCT_NAME_COLUMN);
            if (name == null) {
                throw new ColumnNotFoundException(PRODUCT_NAME_COLUMN, "products");
            }
            rows.add(new OrderHistoryRow(order.orderId(), order.sku(), name, order.quantity()));
        }
        return rows;
    }

    /** How many round trips to a database the page above needed. Always one. */
    public int queriesForOnePage() {
        return 1;
    }
}
