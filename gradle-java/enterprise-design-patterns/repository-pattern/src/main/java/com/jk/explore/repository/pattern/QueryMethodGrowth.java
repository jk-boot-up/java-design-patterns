package com.jk.explore.repository.pattern;

import com.jk.explore.repository.domain.Customer;

import java.util.List;

/**
 * <strong>The bill: a repository grows a method per question.</strong> Each
 * new business question adds one, until the interface is a query language with
 * worse ergonomics. This is the interface after three more questions arrived.
 */
public interface QueryMethodGrowth {

    List<Customer> findByCity(String city);

    List<Customer> findByCityAndOrderedAfter(String city, int day);

    List<Customer> findByCityAndOrderDateAfterAndStatusIn(String city, int day, List<String> statuses);

    List<Customer> findByCityAndOrderDateAfterAndStatusInOrderByNameAsc(String city, int day, List<String> statuses);
}
