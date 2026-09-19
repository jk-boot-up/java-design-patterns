package com.jk.explore.identitymap.pattern;

import com.jk.explore.identitymap.domain.Customer;
import com.jk.explore.identitymap.domain.Order;
import com.jk.explore.identitymap.naive.PlainCustomerMapper;
import com.jk.explore.identitymap.toydb.Database;
import com.jk.explore.identitymap.toydb.Row;

/**
 * <strong>One session, one identity map.</strong> Ask for customer 7 twice
 * and get the same object both times. The second ask costs no database
 * operation at all.
 *
 * <p>The scope is the session: a new session is a new map, so it sees the
 * database afresh, and this session does not see changes made elsewhere.
 */
public class CustomerSession {

    private final PlainCustomerMapper mapper;
    private final Database database;
    private final IdentityMap<Customer> customers = new IdentityMap<>();

    public CustomerSession(Database database) {
        this.database = database;
        this.mapper = new PlainCustomerMapper(database);
    }

    public Customer find(int id) {
        Customer already = customers.get(id);
        if (already != null) {
            return already;
        }
        Customer loaded = mapper.find(id);
        if (loaded != null) {
            customers.put(id, loaded);
        }
        return loaded;
    }

    public Order findOrder(int orderId) {
        Row row = database.table("orders").select(orderId);
        return new Order(orderId, find(row.number("customer_id")));
    }

    public void save(Customer customer) {
        mapper.save(customer);
    }

    /** How many objects this session is holding on to. */
    public int loadedCount() {
        return customers.size();
    }
}
