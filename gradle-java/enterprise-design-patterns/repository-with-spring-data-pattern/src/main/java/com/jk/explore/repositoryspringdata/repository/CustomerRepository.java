package com.jk.explore.repositoryspringdata.repository;

import com.jk.explore.repositoryspringdata.domain.Customer;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;

import java.util.List;

/**
 * <strong>An interface with no implementation.</strong> There is no class in
 * this project that implements it. Spring Data generates one at start-up, and
 * writes the query for each method from the method's own name.
 */
public interface CustomerRepository extends JpaRepository<Customer, Integer> {

    /** The query the partner project wrote by hand, generated from this name. */
    List<Customer> findDistinctByCityAndOrdersDayGreaterThan(String city, int day);

    /** The partner's finder, so the calling code can stay exactly as it was. */
    default List<Customer> findByCityAndOrderedAfter(String city, int day) {
        return findDistinctByCityAndOrdersDayGreaterThan(city, day);
    }

    /** The bill: the name a real question ends up with. */
    List<Customer> findDistinctByCityAndOrdersDayGreaterThanAndOrdersStatusIn(String city, int day, List<String> statuses);

    /** The interface can say "join" here, at the price of a persistence hint on the caller-facing type. */
    @EntityGraph(attributePaths = "orders")
    @Query("select c from Customer c")
    List<Customer> findAllWithOrders();
}
