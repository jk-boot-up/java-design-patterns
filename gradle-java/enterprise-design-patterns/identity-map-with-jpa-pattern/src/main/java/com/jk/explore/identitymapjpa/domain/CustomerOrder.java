package com.jk.explore.identitymapjpa.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/** The same order as Identity Map's: an id, and the customer it belongs to. */
@Entity
@Table(name = "orders")
public class CustomerOrder {

    @Id
    private int id;

    @ManyToOne
    private Customer customer;

    protected CustomerOrder() {
    }

    public CustomerOrder(int id, Customer customer) {
        this.id = id;
        this.customer = customer;
    }

    public int id() {
        return id;
    }

    public Customer customer() {
        return customer;
    }
}
