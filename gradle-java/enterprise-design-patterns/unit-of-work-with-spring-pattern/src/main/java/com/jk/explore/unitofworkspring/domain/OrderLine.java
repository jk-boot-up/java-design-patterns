package com.jk.explore.unitofworkspring.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class OrderLine {

    @Id
    private int id;
    private int orderId;
    private int productId;
    private int quantity;

    protected OrderLine() {
    }

    public OrderLine(int id, int orderId, int productId, int quantity) {
        this.id = id;
        this.orderId = orderId;
        this.productId = productId;
        this.quantity = quantity;
    }

    public int id() {
        return id;
    }
}
