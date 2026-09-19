package com.jk.explore.repository.domain;

import java.util.ArrayList;
import java.util.List;

/** A customer, and the orders they have placed. */
public class Customer {

    private final int id;
    private final String name;
    private final String city;
    private final List<Order> orders = new ArrayList<>();

    public Customer(int id, String name, String city) {
        this.id = id;
        this.name = name;
        this.city = city;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public String city() {
        return city;
    }

    public List<Order> orders() {
        return orders;
    }

    public boolean hasOrderAfter(int day) {
        return orders.stream().anyMatch(o -> o.day() > day);
    }
}
