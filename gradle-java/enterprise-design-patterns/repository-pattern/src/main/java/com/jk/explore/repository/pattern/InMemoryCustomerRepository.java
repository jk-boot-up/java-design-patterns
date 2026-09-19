package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;

import java.util.ArrayList;
import java.util.List;

/** A repository backed by a plain list. */
public class InMemoryCustomerRepository implements CustomerRepository {

    private final List<Customer> customers = new ArrayList<>();

    @Override
    public void add(Customer customer) {
        customers.add(customer);
    }

    @Override
    public Customer findById(int id) {
        return customers.stream().filter(c -> c.id() == id).findFirst().orElse(null);
    }

    @Override
    public List<Customer> findByCityAndOrderedAfter(String city, int day) {
        return matching(Specification.inCity(city).and(Specification.orderedAfter(day)));
    }

    @Override
    public List<Customer> matching(Specification<Customer> specification) {
        return customers.stream().filter(specification::isSatisfiedBy).toList();
    }
}
