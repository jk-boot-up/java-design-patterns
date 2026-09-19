package com.jk.explore.contract;

import java.util.Map;

/** What one consumer needs from a response, and nothing more: the fields it reads, and their types. */
public record Contract(String consumer, Map<String, Type> expects) {
}
