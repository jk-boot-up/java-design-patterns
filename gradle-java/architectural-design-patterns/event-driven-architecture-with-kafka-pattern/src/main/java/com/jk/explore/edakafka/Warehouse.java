package com.jk.explore.edakafka;

public class Warehouse {

    private int stock;

    public Warehouse(int stock) {
        this.stock = stock;
    }

    public void reserve(String event) {
        if (event.startsWith("OrderPlaced")) {
            stock--;
        }
    }

    public int stock() {
        return stock;
    }
}
