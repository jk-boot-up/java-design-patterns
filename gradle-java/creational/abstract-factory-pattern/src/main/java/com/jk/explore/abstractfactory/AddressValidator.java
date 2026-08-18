package com.jk.explore.abstractfactory;

/**
 * One member of the product family: what this market calls the postal part
 * of an address, and what a valid one looks like.
 */
public interface AddressValidator {

    String postcodeLabel();

    boolean isValid(String postcode);
}
