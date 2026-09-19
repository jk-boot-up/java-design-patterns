package com.jk.explore.pactcdc;

/** The releases of the catalog's price service. Each answers in its own shape. */
public enum Release {

    /** sku, priceCents in pence, currency. */
    V1("{\"sku\":\"%s\",\"priceCents\":1600,\"currency\":\"GBP\"}"),
    /** priceCents has been renamed to price. */
    RENAMED("{\"sku\":\"%s\",\"price\":1600,\"currency\":\"GBP\"}"),
    /** A stock field has been added; nothing has been taken away. */
    EXTRA_FIELD("{\"sku\":\"%s\",\"priceCents\":1600,\"currency\":\"GBP\",\"stock\":40}"),
    /** Same field, same type, but now in pounds and not pence. */
    POUNDS("{\"sku\":\"%s\",\"priceCents\":16,\"currency\":\"GBP\"}");

    private final String template;

    Release(String template) {
        this.template = template;
    }

    public String body(String sku) {
        return template.formatted(sku);
    }
}
