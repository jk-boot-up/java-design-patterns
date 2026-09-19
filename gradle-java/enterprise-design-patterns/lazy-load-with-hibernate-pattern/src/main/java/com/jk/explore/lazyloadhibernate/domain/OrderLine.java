package com.jk.explore.lazyloadhibernate.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class OrderLine {

    @Id
    private int id;
    private int quantity;

    @ManyToOne(fetch = FetchType.LAZY)
    private CustomerOrder order;

    @ManyToOne(fetch = FetchType.LAZY)
    private Product product;

    protected OrderLine() {
    }

    public OrderLine(int id, CustomerOrder order, Product product, int quantity) {
        this.id = id;
        this.order = order;
        this.product = product;
        this.quantity = quantity;
    }

    public int id() {
        return id;
    }

    public Product product() {
        return product;
    }
}
