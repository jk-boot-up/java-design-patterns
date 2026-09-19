package com.jk.explore.identitymapjpa.domain;

import jakarta.persistence.Entity;
import jakarta.persistence.Id;

import java.util.Objects;

/**
 * The same customer as Identity Map's, with two annotations. {@code @Entity}
 * says it is stored; {@code @Id} says which field is its identity. Nothing
 * else about the class changed.
 */
@Entity
public class Customer {

    @Id
    private int id;
    private String name;
    private String email;
    private String address;

    protected Customer() {
    }

    public Customer(int id, String name, String email, String address) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.address = address;
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public String email() {
        return email;
    }

    public String address() {
        return address;
    }

    public void changeEmail(String email) {
        this.email = email;
    }

    public void moveTo(String address) {
        this.address = address;
    }

    @Override
    public boolean equals(Object other) {
        return other instanceof Customer c && c.id == id;
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }
}
