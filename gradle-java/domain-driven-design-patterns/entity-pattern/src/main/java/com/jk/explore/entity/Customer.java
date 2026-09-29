package com.jk.explore.entity;

import java.util.ArrayList;
import java.util.List;
import java.util.Objects;

/**
 * The pattern: a customer is defined by its identity, not by its current details.
 *
 * <p>Its name, email and points can all change over its life; it stays the
 * same customer because its ID does not. Equality and hashing use the ID only.
 */
public final class Customer {

    private final CustomerId id;
    private final String name;
    private String email;
    private long points;
    private final List<String> history = new ArrayList<>();

    public Customer(CustomerId id, String name, String email) {
        this.id = Objects.requireNonNull(id);
        this.name = name;
        this.email = email;
        history.add("opened with " + email);
    }

    public void changeEmail(String newEmail) {
        history.add("email " + email + " -> " + newEmail);
        email = newEmail;
    }

    public void earn(long points) {
        this.points += points;
    }

    public CustomerId id() {
        return id;
    }

    public String name() {
        return name;
    }

    public String email() {
        return email;
    }

    public long points() {
        return points;
    }

    public List<String> history() {
        return List.copyOf(history);
    }

    /** A detached copy, as a cache or another screen might hold. */
    public Customer copy() {
        Customer c = new Customer(id, name, email);
        c.points = points;
        return c;
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof Customer other && other.id.equals(id);
    }

    @Override
    public int hashCode() {
        return id.hashCode();
    }

    @Override
    public String toString() {
        return id + " " + name + " <" + email + ">";
    }
}
