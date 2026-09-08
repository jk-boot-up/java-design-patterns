package com.jk.explore.chain;

import java.util.List;
import java.util.Optional;
import java.util.Set;

/**
 * Is this somewhere the couriers actually go?
 *
 * <p>The cheapest link in the chain — no network call, just two lookups — which
 * is why the standard chain puts it first. Where a link sits is a cost decision
 * as much as a correctness one.
 */
public final class AddressCheck extends ScreeningHandler {

    private static final Set<String> SERVED_COUNTRIES = Set.of("GB", "IE");
    private static final List<String> EXCLUDED_POSTCODES = List.of("JE", "GY", "IM");

    @Override
    public String name() {
        return "address";
    }

    @Override
    protected Optional<Decision> check(CheckoutRequest request) {
        if (!SERVED_COUNTRIES.contains(request.country())) {
            return Optional.of(Decision.rejected(name(),
                    "we do not ship to " + request.country()));
        }
        for (String prefix : EXCLUDED_POSTCODES) {
            if (request.postcode().startsWith(prefix)) {
                return Optional.of(Decision.rejected(name(),
                        "no courier covers " + request.postcode()));
            }
        }
        return Optional.empty();   // nothing to say — ask the next link
    }
}
