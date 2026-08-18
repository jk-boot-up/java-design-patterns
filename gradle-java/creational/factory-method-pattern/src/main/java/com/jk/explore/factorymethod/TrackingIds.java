package com.jk.explore.factorymethod;

import java.util.UUID;

final class TrackingIds {

    private TrackingIds() {
    }

    static String withPrefix(String prefix) {
        return prefix + "-" + UUID.randomUUID().toString().substring(0, 8).toUpperCase();
    }
}
