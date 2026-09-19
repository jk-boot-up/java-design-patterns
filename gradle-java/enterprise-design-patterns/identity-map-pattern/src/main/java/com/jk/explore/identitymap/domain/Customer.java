package com.jk.explore.identitymap.domain;

import java.util.Objects;

/**
 * A customer. {@code equals} compares ids, which is the partial fix the
 * demo shows is not enough: two equal objects can still be changed
 * separately.
 */
public class Customer {

    private final int id;
    private String name;
    private String email;
    private String address;

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
