package com.jk.explore.repositoryspringdata.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.FetchType;
import jakarta.persistence.Id;
import jakarta.persistence.OneToMany;

import java.util.ArrayList;
import java.util.List;

/** The partner's customer: a name, a city, and the orders they have placed. */
@Entity
public class Customer {

    @Id
    private int id;
    private String name;
    private String city;

    @OneToMany(mappedBy = "customer", fetch = FetchType.LAZY)
    private List<CustomerOrder> orders = new ArrayList<>();

    protected Customer() {
    }

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

    public void moveTo(String newCity) {
        this.city = newCity;
    }

    public List<CustomerOrder> orders() {
        return orders;
    }
}
