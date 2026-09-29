package com.jk.explore.extensionobject;

import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

/**
 * The pattern: a small core product that can carry extra roles, looked up by type, added by anyone.
 *
 * <p>The product knows nothing about warranties or downloads. Other code
 * attaches them with {@link #with}, and asks for them with {@link #extension},
 * which answers "not supported" as an empty Optional.
 */
public final class Product {

    private final String sku;
    private final String name;
    private final long pricePence;
    private final Map<Class<?>, Object> extensions = new LinkedHashMap<>();

    public Product(String sku, String name, long pricePence) {
        this.sku = sku;
        this.name = name;
        this.pricePence = pricePence;
    }

    public <T> Product with(Class<T> type, T extension) {
        extensions.put(type, extension);
        return this;
    }

    public <T> Optional<T> extension(Class<T> type) {
        return Optional.ofNullable(type.cast(extensions.get(type)));
    }

    public Set<String> extensionNames() {
        return extensions.keySet().stream().map(Class::getSimpleName).collect(Collectors.toCollection(java.util.LinkedHashSet::new));
    }

    public String sku() {
        return sku;
    }

    public String name() {
        return name;
    }

    public long pricePence() {
        return pricePence;
    }
}
