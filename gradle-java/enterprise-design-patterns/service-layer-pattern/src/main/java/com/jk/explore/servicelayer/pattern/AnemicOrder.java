package com.jk.explore.servicelayer.pattern;

import java.util.List;

/**
 * <strong>The bill: an anemic domain object.</strong> Fields, getters and
 * setters, and no behaviour at all. Every rule about orders lives somewhere
 * else, in the service.
 */
public class AnemicOrder {

    private int id;
    private int customerId;
    private List<Integer> quantities;
    private int totalPence;

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getCustomerId() {
        return customerId;
    }

    public void setCustomerId(int customerId) {
        this.customerId = customerId;
    }

    public List<Integer> getQuantities() {
        return quantities;
    }

    public void setQuantities(List<Integer> quantities) {
        this.quantities = quantities;
    }

    public int getTotalPence() {
        return totalPence;
    }

    public void setTotalPence(int totalPence) {
        this.totalPence = totalPence;
    }
}
