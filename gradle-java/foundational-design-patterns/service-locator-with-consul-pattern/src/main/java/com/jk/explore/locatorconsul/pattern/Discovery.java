package com.jk.explore.locatorconsul.pattern;

import com.jk.explore.locatorconsul.consul.Address;

/**
 * <strong>The static way in: how a class reaches the locator.</strong> Every class
 * that needs a remote service calls this, so every class depends on it, and none
 * says so in its signature.
 */
public final class Discovery {

    private static Locator locator;

    private Discovery() {
    }

    public static void use(Locator configured) {
        locator = configured;
    }

    public static Address find(String serviceName) {
        if (locator == null) {
            throw new IllegalStateException("no locator is configured");
        }
        return locator.find(serviceName);
    }
}
