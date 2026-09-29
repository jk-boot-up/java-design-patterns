package com.jk.explore.recipientlist;

import java.util.List;

/**
 * An order: its lines, each with a product category, its total, and whether it is a gift.
 */
public record Order(String id, List<String> categories, long pence, boolean gift) {
}
