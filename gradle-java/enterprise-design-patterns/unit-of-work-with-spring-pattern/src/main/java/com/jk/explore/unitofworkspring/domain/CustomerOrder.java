package com.jk.explore.unitofworkspring.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

@Entity
@Table(name = "orders")
public class CustomerOrder {

    @Id
    private int id;
    private int customerId;

    protected CustomerOrder() {
    }

    public CustomerOrder(int id, int customerId) {
        this.id = id;
        this.customerId = customerId;
    }

    public int id() {
        return id;
    }
}
