package com.jk.explore.datamapper.domain;

/**
 * <strong>A customer, and nothing else.</strong> No table name, no column
 * name, no SQL, no database. The demo prints this class's members to prove
 * it, and the domain tests construct one with no database anywhere.
 */
public class Customer {

    private final int id;
    private String name;
    private String email;
    private Address address;
    private int loyaltyPoints;

    public Customer(int id, String name, String email, Address address, int loyaltyPoints) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.address = address;
        this.loyaltyPoints = loyaltyPoints;
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

    public Address address() {
        return address;
    }

    public int loyaltyPoints() {
        return loyaltyPoints;
    }

    public void changeEmail(String newEmail) {
        if (!newEmail.contains("@")) {
            throw new IllegalArgumentException("not an email address: " + newEmail);
        }
        this.email = newEmail;
    }

    public void moveTo(Address newAddress) {
        this.address = newAddress;
    }

    public void earnPoints(int points) {
        this.loyaltyPoints += points;
    }
}
