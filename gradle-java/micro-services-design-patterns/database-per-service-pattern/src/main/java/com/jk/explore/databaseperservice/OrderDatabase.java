package com.jk.explore.databaseperservice;

import java.util.ArrayList;
import java.util.List;

/**
 * The Orders service's own database. Nobody else may read it.
 *
 * Every method takes the name of whoever is asking and refuses anybody but the owner.
 * That check is standing in for database credentials — see {@link NotYourDataException}
 * — and it is the entire pattern. There is nothing else to it.
 */
public final class OrderDatabase {

    private static final String OWNER = "Orders";

    private final List<Order> orders = new ArrayList<>();
    private final CallLog log;
    private int queries;

    public OrderDatabase(CallLog log) {
        this.log = log;
    }

    public void insert(Order order) {
        orders.add(order);
    }

    /**
     * Every order a customer has placed.
     *
     * @param requester the service asking
     * @throws NotYourDataException if that is anybody but Orders
     */
    public List<Order> ordersFor(String requester, String customerId) {
        refuseStrangers(requester);
        queries++;
        List<Order> found = orders.stream()
                .filter(o -> o.customerId().equals(customerId))
                .toList();
        log.note("OrderDb", "QUERY", found.size() + " order(s) for " + customerId);
        return found;
    }

    private void refuseStrangers(String requester) {
        if (!OWNER.equals(requester)) {
            log.note("OrderDb", "REFUSED", requester + " tried to read Orders' tables");
            throw new NotYourDataException(requester, OWNER);
        }
    }

    public int queries() {
        return queries;
    }
}
