package com.jk.explore.prototype;

import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.NoSuchElementException;
import java.util.Objects;
import java.util.Set;

/**
 * A prototype registry: a named shelf of pre-built {@link ProductListing}
 * templates that callers clone by key instead of assembling from scratch.
 *
 * <p>This is the Gang of Four's own variant of Prototype — the book
 * describes a registry exactly like this one for cases where the set of
 * "kinds of thing to copy" is decided at runtime (loaded from a database,
 * configured by an admin) rather than known and named in the caller's code.
 * A caller here only ever needs a key, such as {@code "earbuds-template"};
 * it never needs to know how that template was originally assembled.
 */
public final class ListingRegistry {

    private final Map<String, ProductListing> templates = new LinkedHashMap<>();

    public void register(String key, ProductListing template) {
        templates.put(Objects.requireNonNull(key, "key"), Objects.requireNonNull(template, "template"));
    }

    /** Returns a fresh, independent copy of the template registered under {@code key}. */
    public ProductListing create(String key) {
        ProductListing template = templates.get(key);
        if (template == null) {
            throw new NoSuchElementException("no listing template registered under: " + key);
        }
        return template.copy();
    }

    public Set<String> keys() {
        return Collections.unmodifiableSet(templates.keySet());
    }
}
