package com.jk.explore.builder;

/** A postal address. Nothing to decide, so a constructor is right. */
public record Address(String line1, String city, String postcode, String country) {

    @Override
    public String toString() {
        return line1 + ", " + city + " " + postcode + ", " + country;
    }
}
