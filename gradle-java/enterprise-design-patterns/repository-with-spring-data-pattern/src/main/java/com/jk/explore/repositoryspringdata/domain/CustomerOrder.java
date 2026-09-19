package com.jk.explore.repositoryspringdata.domain;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;
import jakarta.persistence.Table;

/** The partner's order: placed on a numbered day, with a status. */
@Entity
@Table(name = "orders")
public class CustomerOrder {

    @Id
    private int id;
    @Column(name = "order_day")
    private int day;
    private String status;

    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;

    protected CustomerOrder() {
    }

    public CustomerOrder(int id, int day, String status, Customer customer) {
        this.id = id;
        this.day = day;
        this.status = status;
        this.customer = customer;
    }

    public int id() {
        return id;
    }

    public int day() {
        return day;
    }

    public String status() {
        return status;
    }
}
