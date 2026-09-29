package com.jk.explore.contextmap.kernel;

/**
 * Shared kernel: the one address both sales and shipping use. Changed only when both teams agree.
 */
public record Address(String flat, String street, String city) {

    public String label() {
        return (flat == null ? "" : flat + ", ") + street + ", " + city;
    }
}
