package com.jk.explore.servicestub;

import java.util.HashMap;
import java.util.Map;
import java.util.Optional;

/**
 * The pattern: a free, instant, in-memory stand-in for the postcode service, used in development and tests.
 *
 * <p>It knows a handful of postcodes, and can be told to behave as if the
 * service were down, which the real one cannot be asked to do. It was written
 * to accept postcodes in any case, which the real service does not: a
 * difference only a contract check will notice.
 */
public final class PostcodeStub implements AddressGateway {

    private final Map<String, String> known = new HashMap<>(Map.of(
            "LS1 4AP", "4 Mill Lane, Leeds",
            "BA1 2QH", "9 Park Road, Bath"));
    private boolean down;
    private int lookups;

    @Override
    public Optional<String> lookup(String postcode) {
        lookups++;
        if (down) {
            throw new IllegalStateException("postcode service unreachable");
        }
        return Optional.ofNullable(known.get(postcode.toUpperCase()));
    }

    public PostcodeStub goDown() {
        down = true;
        return this;
    }

    public int lookups() {
        return lookups;
    }
}
