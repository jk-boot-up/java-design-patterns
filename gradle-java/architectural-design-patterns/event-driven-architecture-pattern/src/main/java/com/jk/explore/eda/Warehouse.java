package com.jk.explore.eda;

public class Warehouse {

    private int stock;

    public Warehouse(int stock) {
        this.stock = stock;
    }

    public void reserve(Event e) {
        if (e.type().equals("OrderPlaced")) {
            stock--;
        }
    }

    public int stock() {
        return stock;
    }
}
