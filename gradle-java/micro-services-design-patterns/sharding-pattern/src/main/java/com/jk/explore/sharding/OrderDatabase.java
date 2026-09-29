package com.jk.explore.sharding;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Predicate;

/**
 * One database server. It can take 1,000 new orders a minute; anything beyond that has to wait.
 */
public final class OrderDatabase {

    public static final int PER_MINUTE = 1000;

    private final String name;
    private final List<Order> orders = new ArrayList<>();
    private int queriesAnswered;

    public OrderDatabase(String name) {
        this.name = name;
    }

    public void insert(Order o) {
        orders.add(o);
    }

    public List<Order> find(Predicate<Order> test) {
        queriesAnswered++;
        return orders.stream().filter(test).toList();
    }

    public int size() {
        return orders.size();
    }

    public int queriesAnswered() {
        return queriesAnswered;
    }

    public String name() {
        return name;
    }
}
