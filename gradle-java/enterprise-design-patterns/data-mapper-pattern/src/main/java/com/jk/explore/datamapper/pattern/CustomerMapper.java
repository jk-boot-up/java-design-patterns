package com.jk.explore.datamapper.pattern;

import com.jk.explore.datamapper.domain.Address;
import com.jk.explore.datamapper.domain.Customer;
import com.jk.explore.datamapper.domain.CustomerSummary;
import com.jk.explore.datamapper.toydb.Database;
import com.jk.explore.datamapper.toydb.Row;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The data mapper: it moves data between a {@link Customer} and its
 * rows, and is the only class that knows both.</strong>
 *
 * <p>One customer here is spread across two tables, {@code customers} and
 * {@code addresses}. The same {@code customers} table also feeds a second
 * object, {@link CustomerSummary}. Active Record has no answer for either
 * shape.
 */
public class CustomerMapper {

    static final String CUSTOMERS = "customers";
    static final String ADDRESSES = "addresses";

    private final Database database;

    public CustomerMapper(Database database) {
        this.database = database;
    }

    public void insert(Customer customer) {
        database.table(CUSTOMERS).insert(customer.id(), customerRow(customer));
        database.table(ADDRESSES).insert(customer.id(), addressRow(customer.address()));
    }

    public void update(Customer customer) {
        database.table(CUSTOMERS).update(customer.id(), customerRow(customer));
        database.table(ADDRESSES).update(customer.id(), addressRow(customer.address()));
    }

    public Customer find(int id) {
        Row customer = database.table(CUSTOMERS).select(id);
        if (customer == null) {
            return null;
        }
        Row address = database.table(ADDRESSES).select(id);
        return new Customer(id, customer.text("name"), customer.text("email"),
                new Address(address.text("street"), address.text("city"), address.text("postcode")),
                customer.number("loyalty_points"));
    }

    public List<CustomerSummary> summaries() {
        List<CustomerSummary> summaries = new ArrayList<>();
        for (Row row : database.table(CUSTOMERS).selectAll()) {
            summaries.add(new CustomerSummary(row.number("id"), row.text("name")));
        }
        return summaries;
    }

    protected Row customerRow(Customer customer) {
        return Row.of("id", customer.id(), "name", customer.name(), "email", customer.email(),
                "loyalty_points", customer.loyaltyPoints());
    }

    protected Row addressRow(Address address) {
        return Row.of("street", address.street(), "city", address.city(), "postcode", address.postcode());
    }
}
