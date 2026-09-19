package com.jk.explore.lazyloadhibernate.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.OneToMany;
import jakarta.persistence.Table;

import java.util.ArrayList;
import java.util.List;

/**
 * The partner's order: a customer and four lines. Both are declared lazy, and
 * that one word, {@code FetchType.LAZY}, is what this whole project is about.
 */
@Entity
@Table(name = "orders")
public class CustomerOrder {

    @Id
    private int id;

    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;

    @OneToMany(mappedBy = "order", fetch = FetchType.LAZY)
    private List<OrderLine> lines = new ArrayList<>();

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

    public List<OrderLine> lines() {
        return lines;
    }
}
