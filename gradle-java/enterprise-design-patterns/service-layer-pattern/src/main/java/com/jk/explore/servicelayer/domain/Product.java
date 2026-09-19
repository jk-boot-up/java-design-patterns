package com.jk.explore.servicelayer.domain;

/** A product, and the rule that stock cannot go below zero. The rule lives here, in the domain. */
public class Product {

    private final int id;
    private final String name;
    private final int pricePence;
    private int stock;

    public Product(int id, String name, int pricePence, int stock) {
        this.id = id;
        this.name = name;
        this.pricePence = pricePence;
        this.stock = stock;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public int pricePence() {
        return pricePence;
    }

    public int stock() {
        return stock;
    }

    public void reserve(int quantity) {
        if (quantity > stock) {
            throw new OrderRejectedException("only " + stock + " " + name + " in stock, " + quantity + " wanted");
        }
        stock -= quantity;
    }
}
