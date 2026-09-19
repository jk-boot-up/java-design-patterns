package com.jk.explore.repositoryspringdata.service;

import com.jk.explore.repositoryspringdata.domain.Customer;
import com.jk.explore.repositoryspringdata.repository.CustomerRepository;
import org.springframework.stereotype.Service;

import java.util.List;

/** The partner's caller. It knows the interface and nothing else, and its body is what it was. */
@Service
public class MarketingService {

    public static final int LAST_MONTH_STARTS = 70;

    private final CustomerRepository customers;

    public MarketingService(CustomerRepository customers) {
        this.customers = customers;
    }

    public List<String> londonCustomersWhoOrderedLastMonth() {
        return customers.findByCityAndOrderedAfter("London", LAST_MONTH_STARTS).stream()
                .map(Customer::name).sorted().toList();
    }
}
