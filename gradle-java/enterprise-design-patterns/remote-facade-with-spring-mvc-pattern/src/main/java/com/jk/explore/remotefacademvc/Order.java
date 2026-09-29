package com.jk.explore.remotefacademvc;

import java.util.List;
import java.util.Set;

/**
 * The order, fine-grained inside the server: small methods, and the business rule about valid slots.
 */
public final class Order {

    static final Set<String> SLOTS = Set.of("Mon 9-12", "Tue 9-12", "Wed 13-17");

    private final String id = "ORD-1";
    private final String customer = "Priya";
    private final List<String> items = List.of("kettle", "2 x mug");
    private final int pence = 4600;
    private String address = "4 Mill Lane, Leeds";
    private String slot = "Mon 9-12";

    public String id() {
        return id;
    }

    public String customer() {
        return customer;
    }

    public List<String> items() {
        return items;
    }

    public int pence() {
        return pence;
    }

    public String address() {
        return address;
    }

    public String slot() {
        return slot;
    }

    public void changeAddress(String address) {
        this.address = address;
    }

    public void changeSlot(String slot) {
        if (!SLOTS.contains(slot)) {
            throw new IllegalArgumentException("no delivery slot " + slot);
        }
        this.slot = slot;
    }

    /** Both, or neither: the slot is checked before anything changes. */
    public void changeDelivery(String address, String slot) {
        if (!SLOTS.contains(slot)) {
            throw new IllegalArgumentException("no delivery slot " + slot);
        }
        this.address = address;
        this.slot = slot;
    }
}
