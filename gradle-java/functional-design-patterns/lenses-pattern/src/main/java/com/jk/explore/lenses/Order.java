package com.jk.explore.lenses;

import java.util.List;

/**
 * An order: three levels deep, all immutable.
 */
public record Order(String id, Customer customer, List<String> lines) {
}
