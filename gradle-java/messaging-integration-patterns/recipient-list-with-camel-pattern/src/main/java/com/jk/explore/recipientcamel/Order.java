package com.jk.explore.recipientcamel;

import java.util.List;

/**
 * An order: which kinds of item it holds, its value in pence, and whether it is a gift.
 */
public record Order(String id, List<String> categories, long pence, boolean gift) {
}
