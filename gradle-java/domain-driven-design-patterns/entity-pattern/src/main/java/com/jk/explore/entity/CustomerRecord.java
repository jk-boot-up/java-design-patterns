package com.jk.explore.entity;

/**
 * Without the pattern: a customer defined by its values. Two records with the same values are "equal"; change a value and it is someone else.
 */
public record CustomerRecord(String name, String email, long points) {
}
