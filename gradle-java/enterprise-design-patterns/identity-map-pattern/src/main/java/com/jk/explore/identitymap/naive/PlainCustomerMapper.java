package com.jk.explore.identitymap.naive;

import com.jk.explore.identitymap.domain.Customer;
import com.jk.explore.identitymap.domain.Order;
import com.jk.explore.identitymap.toydb.Database;
import com.jk.explore.identitymap.toydb.Row;

/**
 * <strong>Loads a new object every time it is asked.</strong> Correct for a
 * single caller. With two callers holding "customer 7", there are two
 * objects, and each is free to disagree with the other.
 */
public class PlainCustomerMapper {

    static final String CUSTOMERS = "customers";
    static final String ORDERS = "orders";

    protected final Database database;

    public PlainCustomerMapper(Database database) {
        this.database = database;
    }

    public void insert(Customer customer) {
        database.table(CUSTOMERS).insert(customer.id(), row(customer));
    }

    public void insertOrder(int orderId, int customerId) {
        database.table(ORDERS).insert(orderId, Row.of("customer_id", customerId));
    }

    public Customer find(int id) {
        Row row = database.table(CUSTOMERS).select(id);
        return row == null ? null : new Customer(id, row.text("name"), row.text("email"), row.text("address"));
    }

    public Order findOrder(int orderId) {
        Row row = database.table(ORDERS).select(orderId);
        return new Order(orderId, find(row.number("customer_id")));
    }

    /** Writes the whole row, every column, from whatever this object currently holds. */
    public void save(Customer customer) {
        database.table(CUSTOMERS).update(customer.id(), row(customer));
    }

    protected Row row(Customer customer) {
        return Row.of("name", customer.name(), "email", customer.email(), "address", customer.address());
    }
}
