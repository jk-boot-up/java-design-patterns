package com.jk.explore.typeobject;

import java.util.HashMap;
import java.util.Map;

public class TypeRegistry {

    private final Map<String, ProductType> types = new HashMap<>();

    public ProductType define(String name, int taxPercent, int returnDays, int shippingCents) {
        ProductType t = new ProductType(name, null, taxPercent, returnDays, shippingCents);
        types.put(name, t);
        return t;
    }

    /** A type that takes whatever it does not state from its parent. */
    public ProductType derive(String name, String parent, Integer taxPercent, Integer returnDays, Integer shippingCents) {
        ProductType t = new ProductType(name, of(parent), taxPercent, returnDays, shippingCents);
        types.put(name, t);
        return t;
    }

    public ProductType of(String name) {
        ProductType t = types.get(name);
        if (t == null) {
            throw new IllegalArgumentException("no type named " + name);
        }
        return t;
    }

    public int count() {
        return types.size();
    }
}
