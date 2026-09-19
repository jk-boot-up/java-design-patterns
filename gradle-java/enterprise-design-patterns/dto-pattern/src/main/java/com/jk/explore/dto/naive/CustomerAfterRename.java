package com.jk.explore.dto.naive;

/**
 * The same customer after a developer tidies a private field's name from
 * {@code name} to {@code fullName}. Nothing in the compiler objects, and
 * no test of the domain object fails.
 */
public class CustomerAfterRename {

    private final int id = 7;
    private final String fullName = "Ada Lovelace";
    private final String city = "London";
}
