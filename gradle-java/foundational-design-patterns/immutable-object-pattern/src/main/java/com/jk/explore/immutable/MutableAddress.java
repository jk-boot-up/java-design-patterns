package com.jk.explore.immutable;

/**
 * Without the pattern: an address with setters, so anyone holding it can change it for everyone.
 */
public final class MutableAddress {

    private String street;
    private String city;

    public MutableAddress(String street, String city) {
        this.street = street;
        this.city = city;
    }

    public void setStreet(String street) {
        this.street = street;
    }

    public void setCity(String city) {
        this.city = city;
    }

    @Override
    public boolean equals(Object o) {
        return o instanceof MutableAddress a && a.street.equals(street) && a.city.equals(city);
    }

    @Override
    public int hashCode() {
        return (street + city).hashCode();
    }

    @Override
    public String toString() {
        return street + ", " + city;
    }
}
