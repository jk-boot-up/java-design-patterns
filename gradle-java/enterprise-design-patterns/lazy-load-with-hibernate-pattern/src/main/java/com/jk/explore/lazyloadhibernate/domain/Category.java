package com.jk.explore.lazyloadhibernate.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

@Entity
public class Category {

    @Id
    private int id;
    private String name;

    protected Category() {
    }

    public Category(int id, String name) {
        this.id = id;
        this.name = name;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }
}
