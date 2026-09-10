package com.jk.explore.interpreter;

/** Terminal expression: "country is UK". */
public record CountryIs(String country) implements Rule {

    @Override
    public boolean matches(Order order) {
        return country.equalsIgnoreCase(order.country());
    }

    @Override
    public String describe() {
        return "country is " + country;
    }
}
