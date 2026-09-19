package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;
import com.jk.explore.repository.domain.Order;
import com.jk.explore.repository.toydb.Database;
import com.jk.explore.repository.toydb.Row;

import java.util.ArrayList;
import java.util.List;

/**
 * A repository backed by the toy database. The caller cannot say "join" or
 * "fetch the orders with the customers", so to hand back customers with their
 * orders this class loads each customer's orders one query at a time. That is
 * the leak: the abstraction hides the database, and performance needs it.
 */
public class ToyDatabaseCustomerRepository implements CustomerRepository {

    private final Database db;

    public ToyDatabaseCustomerRepository(Database db) {
        this.db = db;
    }

    @Override
    public void add(Customer customer) {
        db.table("customers").insert(customer.id(), Row.of("id", customer.id(), "name", customer.name(), "city", customer.city()));
        for (Order o : customer.orders()) {
            db.table("orders").insert(o.id(), Row.of("id", o.id(), "customer_id", customer.id(), "day", o.day(), "status", o.status()));
        }
    }

    @Override
    public Customer findById(int id) {
        Row row = db.table("customers").select(id);
        return row == null ? null : hydrate(row);
    }

    @Override
    public List<Customer> findByCityAndOrderedAfter(String city, int day) {
        return matching(Specification.inCity(city).and(Specification.orderedAfter(day)));
    }

    @Override
    public List<Customer> matching(Specification<Customer> specification) {
        List<Customer> found = new ArrayList<>();
        for (Row row : db.table("customers").selectAll()) {
            Customer customer = hydrate(row);
            if (specification.isSatisfiedBy(customer)) {
                found.add(customer);
            }
        }
        return found;
    }

    private Customer hydrate(Row row) {
        Customer customer = new Customer(row.number("id"), row.text("name"), row.text("city"));
        for (Row order : db.table("orders").selectWhere("customer_id", customer.id())) {
            customer.orders().add(new Order(order.number("id"), order.number("day"), order.text("status")));
        }
        return customer;
    }
}
