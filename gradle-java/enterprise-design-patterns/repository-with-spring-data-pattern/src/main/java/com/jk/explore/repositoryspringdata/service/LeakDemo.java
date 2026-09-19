package com.jk.explore.repositoryspringdata.service;

import com.jk.explore.repositoryspringdata.domain.Customer;
import com.jk.explore.repositoryspringdata.repository.CustomerRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

/**
 * <strong>The leak: an entity handed out by a repository is a managed object.</strong>
 * Inside a transaction, a change to it is written at commit with no
 * {@code save} call anywhere. Outside one, the same change is silently lost.
 */
@Service
public class LeakDemo {

    private final CustomerRepository customers;

    public LeakDemo(CustomerRepository customers) {
        this.customers = customers;
    }

    /** A caller that only meant to read, and changes an object on the way. Never calls save. */
    @Transactional
    public void moveFirstCustomerInsideATransaction() {
        List<Customer> all = customers.findAll();
        all.stream().filter(c -> c.id() == 1).findFirst().orElseThrow().moveTo("Manchester");
    }

    /** The same change, with no transaction around it. */
    public void moveFirstCustomerOutsideATransaction() {
        List<Customer> all = customers.findAll();
        all.stream().filter(c -> c.id() == 1).findFirst().orElseThrow().moveTo("Manchester");
    }

    /** N+1: the orders are lazy, so touching each customer's orders costs a statement each. */
    @Transactional(readOnly = true)
    public int countOrdersLazily() {
        return customers.findAll().stream().mapToInt(c -> c.orders().size()).sum();
    }

    @Transactional(readOnly = true)
    public int countOrdersWithAGraph() {
        return customers.findAllWithOrders().stream().mapToInt(c -> c.orders().size()).sum();
    }
}
