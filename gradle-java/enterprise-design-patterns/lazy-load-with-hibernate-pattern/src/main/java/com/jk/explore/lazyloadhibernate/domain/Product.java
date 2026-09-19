package com.jk.explore.lazyloadhibernate.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.ManyToOne;

@Entity
public class Product {

    @Id
    private int id;
    private String name;

    @ManyToOne(fetch = FetchType.LAZY)
    private Category category;

    protected Product() {
    }

    public Product(int id, String name, Category category) {
        this.id = id;
        this.name = name;
        this.category = category;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public Category category() {
        return category;
    }
}
