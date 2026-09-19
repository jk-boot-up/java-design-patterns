package com.jk.explore.unitofworkspring.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Product {

    @Id
    private int id;
    private String name;
    private int stock;

    protected Product() {
    }

    public Product(int id, String name, int stock) {
        this.id = id;
        this.name = name;
        this.stock = stock;
    }

    public int id() {
        return id;
    }

    public int stock() {
        return stock;
    }

    public void take(int quantity) {
        this.stock -= quantity;
    }
}
