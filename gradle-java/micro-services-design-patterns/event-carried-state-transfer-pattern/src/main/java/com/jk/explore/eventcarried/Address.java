package com.jk.explore.eventcarried;

/**
 * A customer's delivery address.
 */
public record Address(String street, String city) {

    @Override
    public String toString() {
        return street + ", " + city;
    }
}
