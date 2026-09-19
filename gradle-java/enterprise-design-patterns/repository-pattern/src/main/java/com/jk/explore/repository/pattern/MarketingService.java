package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;
import com.jk.explore.repository.domain.Shop;

import java.util.List;

/**
 * <strong>The caller.</strong> It knows the interface and nothing else: no
 * database, no table, no column. The same class runs, unchanged, against
 * either store.
 */
public class MarketingService {

    private final CustomerRepository customers;

    public MarketingService(CustomerRepository customers) {
        this.customers = customers;
    }

    public List<String> londonCustomersWhoOrderedLastMonth() {
        return customers.findByCityAndOrderedAfter("London", Shop.LAST_MONTH_STARTS).stream()
                .map(Customer::name).toList();
    }
}
