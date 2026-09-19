package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;

/**
 * <strong>A query as an object.</strong> Specifications combine, so the
 * repository does not need a new method for every combination, and the price
 * is one more concept to learn.
 */
public interface Specification<T> {

    boolean isSatisfiedBy(T candidate);

    default Specification<T> and(Specification<T> other) {
        return c -> isSatisfiedBy(c) && other.isSatisfiedBy(c);
    }

    static Specification<Customer> inCity(String city) {
        return c -> c.city().equals(city);
    }

    static Specification<Customer> orderedAfter(int day) {
        return c -> c.hasOrderAfter(day);
    }

    static Specification<Customer> hasOrderWithStatus(String status) {
        return c -> c.orders().stream().anyMatch(o -> o.status().equals(status));
    }
}
