package com.jk.explore.templatemethod;

/**
 * Mints the download key for a digital order.
 *
 * <p>Deliberately deterministic — the same order always produces the same
 * key — so that the demo output and the tests can quote it. A real one would
 * be random and stored.
 */
public final class LicenceKeys {

    private LicenceKeys() {
    }

    public static String mint(Order order) {
        String sku = order.lines().isEmpty() ? "NONE" : order.lines().get(0).sku();
        return "KEY-" + order.id() + "-" + sku;
    }
}
