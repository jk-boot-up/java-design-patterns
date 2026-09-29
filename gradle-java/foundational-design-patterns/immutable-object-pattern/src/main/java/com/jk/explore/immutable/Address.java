package com.jk.explore.immutable;

/**
 * The pattern: an address that can never change. A "change" makes a new Address and leaves this one alone.
 */
public record Address(String street, String city) {

    public Address withStreet(String newStreet) {
        return new Address(newStreet, city);
    }

    public Address withCity(String newCity) {
        return new Address(street, newCity);
    }

    @Override
    public String toString() {
        return street + ", " + city;
    }
}
