package com.jk.explore.unitofwork.domain;

import java.util.ArrayList;
import java.util.List;

public class Order {

    private final int id;
    private final int customerId;
    private final List<OrderLine> lines = new ArrayList<>();

    public Order(int id, int customerId) {
        this.id = id;
        this.customerId = customerId;
    }

    public int id() {
        return id;
    }

    public int customerId() {
        return customerId;
    }

    public List<OrderLine> lines() {
        return lines;
    }

    public void addLine(int productId, int quantity) {
        lines.add(new OrderLine(id * 10 + lines.size() + 1, id, productId, quantity));
    }
}
