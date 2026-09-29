package com.jk.explore.servicestub;

import java.util.Optional;

/**
 * The shop's one door to the postcode service: a postcode in, an address out, or nothing if unknown.
 */
public interface AddressGateway {

    /** The first line and town for a postcode; empty if the postcode is unknown; throws if the service cannot be reached. */
    Optional<String> lookup(String postcode);
}
