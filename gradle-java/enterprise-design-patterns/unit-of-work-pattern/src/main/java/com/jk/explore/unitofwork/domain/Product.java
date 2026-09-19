package com.jk.explore.unitofwork.domain;

public class Product {

    private final int id;
    private final String name;
    private int stock;

    public Product(int id, String name, int stock) {
        this.id = id;
        this.name = name;
        this.stock = stock;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public int stock() {
        return stock;
    }

    public void take(int quantity) {
        this.stock -= quantity;
    }
}
