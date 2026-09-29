package com.jk.explore.remotefacade;

import java.util.List;
import java.util.Set;

/**
 * The domain object: fine-grained, with a small method for each fact and each change. Cheap to call in-process.
 */
public final class Order {

    static final Set<String> SLOTS = Set.of("Mon 9-12", "Mon 12-3", "Tue 9-12");

    private final String id = "ORD-1";
    private final String customer = "Priya";
    private final List<String> items = List.of("kettle", "2 x mug");
    private final long totalPence = 4600;
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

    public long totalPence() {
        return totalPence;
    }

    public String address() {
        return address;
    }

    public String slot() {
        return slot;
    }

    public void changeAddress(String newAddress) {
        address = newAddress;
    }

    /** Both changes, or neither: the slot is checked before anything is changed. */
    public void changeDelivery(String newAddress, String newSlot) {
        if (!SLOTS.contains(newSlot)) {
            throw new IllegalArgumentException("no delivery slot " + newSlot + "; nothing changed");
        }
        address = newAddress;
        slot = newSlot;
    }

    public void bookSlot(String newSlot) {
        if (!SLOTS.contains(newSlot)) {
            throw new IllegalArgumentException("no delivery slot " + newSlot);
        }
        slot = newSlot;
    }
}
