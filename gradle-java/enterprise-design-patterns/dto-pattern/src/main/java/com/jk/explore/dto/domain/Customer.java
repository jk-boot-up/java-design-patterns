package com.jk.explore.dto.domain;

/**
 * <strong>The domain object.</strong> It has private fields nobody should
 * see, a lazily loaded order history, and behaviour: a rule about email.
 * That behaviour is what makes it a domain object and not a DTO.
 */
public class Customer {

    private final int id;
    private String name;
    private String email;
    private final String passwordHash;
    private final String city;
    private int loyaltyPoints;
    private final LazyOrders orders = new LazyOrders();

    public Customer(int id, String name, String email, String passwordHash, String city, int loyaltyPoints) {
        this.id = id;
        this.name = name;
        this.email = email;
        this.passwordHash = passwordHash;
        this.city = city;
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

    public String city() {
        return city;
    }

    public int loyaltyPoints() {
        return loyaltyPoints;
    }

    public LazyOrders orders() {
        return orders;
    }

    public void changeEmail(String newEmail) {
        if (!newEmail.contains("@")) {
            throw new IllegalArgumentException("not an email address: " + newEmail);
        }
        this.email = newEmail;
    }

    public void earnPoints(int points) {
        this.loyaltyPoints += points;
    }

    public void rename(String newName) {
        this.name = newName;
    }

    public static Customer ada() {
        return new Customer(7, "Ada Lovelace", "ada@example.com",
                "$2a$10$N9qo8uLOickgx2ZMRZoMyeIjZAgcfl7p92ldGxad68LJZdL17lhWy", "London", 120);
    }
}
