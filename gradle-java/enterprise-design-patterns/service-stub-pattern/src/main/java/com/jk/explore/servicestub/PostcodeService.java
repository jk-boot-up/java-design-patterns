package com.jk.explore.servicestub;

import java.util.Map;
import java.util.Optional;

/**
 * The real, external postcode service: 5p and 400 ms a lookup, needs the network, and insists on capital letters.
 */
public final class PostcodeService implements AddressGateway {

    public static final int PENCE_PER_LOOKUP = 5;
    public static final int MS_PER_LOOKUP = 400;

    private static final Map<String, String> ADDRESSES = Map.of(
            "LS1 4AP", "4 Mill Lane, Leeds",
            "BA1 2QH", "9 Park Road, Bath",
            "YO1 7HH", "12 High Street, York");

    private boolean online = true;
    private long spentPence;
    private long waitedMs;

    @Override
    public Optional<String> lookup(String postcode) {
        if (!online) {
            throw new IllegalStateException("postcode service unreachable");
        }
        spentPence += PENCE_PER_LOOKUP;
        waitedMs += MS_PER_LOOKUP;
        if (!postcode.equals(postcode.toUpperCase())) {
            throw new IllegalArgumentException("invalid postcode format: " + postcode);
        }
        return Optional.ofNullable(ADDRESSES.get(postcode));
    }

    public void setOnline(boolean online) {
        this.online = online;
    }

    public long spentPence() {
        return spentPence;
    }

    public long waitedMs() {
        return waitedMs;
    }
}
