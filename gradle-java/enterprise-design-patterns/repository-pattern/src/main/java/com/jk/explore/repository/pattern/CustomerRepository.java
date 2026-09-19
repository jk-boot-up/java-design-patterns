package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;

import java.util.List;

/**
 * <strong>An interface that looks like an in-memory collection of customers.</strong>
 * Callers ask for customers. They do not know a database exists.
 */
public interface CustomerRepository {

    void add(Customer customer);

    Customer findById(int id);

    /** London customers who ordered after {@code day}: the question, asked one way. */
    List<Customer> findByCityAndOrderedAfter(String city, int day);

    /** Any customers matching a specification. */
    List<Customer> matching(Specification<Customer> specification);
}
