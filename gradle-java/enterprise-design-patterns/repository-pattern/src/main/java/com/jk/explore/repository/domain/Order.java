package com.jk.explore.repository.domain;

/** An order, placed on a numbered day, with a status. */
public record Order(int id, int day, String status) {
}
