package com.jk.explore.activerecord;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * An active record: an order that is also one row of the orders table. It finds itself, saves itself, and
 * carries the rules about itself. One class, and the table's columns are its fields.
 */
public class Order {

    static final Table TABLE = new Table();

    private Integer id;
    private final int customerId;
    private long totalPence;
    private String status = "DRAFT";

    public Order(int customerId) {
        this.customerId = customerId;
    }

    public Integer id() {
        return id;
    }

    public int customerId() {
        return customerId;
    }

    public long totalPence() {
        return totalPence;
    }

    public String status() {
        return status;
    }

    /** A rule about the order, written on the order. */
    public void addLine(long unitPence, int quantity) {
        if (!isEditable()) {
            throw new IllegalStateException("a " + status + " order cannot change");
        }
        totalPence += unitPence * quantity;
    }

    public boolean isEditable() {
        return status.equals("DRAFT");
    }

    /** A rule that needs a record: loads the customer to decide. Convenient, and it touches the table. */
    public boolean qualifiesForFreeDelivery(long thresholdPence) {
        return totalPence >= thresholdPence && Customer.find(customerId).name().length() > 0;
    }

    public void place() {
        if (totalPence <= 0) {
            throw new IllegalStateException("an empty order cannot be placed");
        }
        status = "PLACED";
    }

    public Order save() {
        Map<String, Object> row = new HashMap<>();
        row.put("customer_id", customerId);
        row.put("total_pence", totalPence);
        row.put("status", status);
        if (id == null) {
            id = TABLE.insert(row);
        } else {
            TABLE.update(id, row);
        }
        return this;
    }

    public static Order find(int id) {
        Map<String, Object> row = TABLE.find(id);
        if (row == null) {
            throw new IllegalArgumentException("no order " + id);
        }
        return fromRow(id, row);
    }

    public static List<Order> forCustomer(int customerId) {
        return TABLE.whereEquals("customer_id", customerId).stream().map(Order::find).toList();
    }

    private static Order fromRow(int id, Map<String, Object> row) {
        for (String column : new String[]{"customer_id", "total_pence", "status"}) {
            if (!row.containsKey(column) || row.get(column) == null) {
                throw new IllegalStateException("the orders table has no column " + column);
            }
        }
        Order o = new Order((Integer) row.get("customer_id"));
        o.id = id;
        o.totalPence = (Long) row.get("total_pence");
        o.status = (String) row.get("status");
        return o;
    }
}
