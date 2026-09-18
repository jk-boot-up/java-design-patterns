package com.jk.explore.sidecarjavaproxy;

import java.util.List;

/**
 * Whatever is listening on the port beside the service.
 *
 * <p>This interface is the entire reason the swap in this project is possible, and it is
 * worth noticing how little it asks for. A proxy has to take a payment and either come
 * back with a receipt or throw. It does not have to be written in any particular
 * language, be built by the same team, ship on the same day, or know anything at all
 * about the shop.
 *
 * <p>In the deployed version there is no interface, because there is no shared program.
 * The contract there is the network: something accepts a request on {@code
 * localhost:8081} and answers it. That is a far weaker promise than a Java interface and
 * it is exactly as sufficient — which is the point the project is making. Here it is
 * typed only because everything in Tier 1 runs in one JVM and Java wants a type.
 *
 * <p>The three description methods exist for the demo rather than for the pattern.
 * {@link #cannotExpress()} is the honest one: a proxy that admits what its configuration
 * language has no words for is a proxy you can make an informed decision about.
 */
public interface Proxy {

    /** The name the demo and the provider know this proxy by. */
    String name();

    /** What it is written in. The point of the project is that this may be anything. */
    String language();

    /** Roughly how much of it there is — the line count a maintainer inherits. */
    int lines();

    /**
     * Parts of the agreed policy this proxy's configuration language cannot state.
     *
     * <p>Empty for a proxy that can say everything the policy says. Not empty is not a
     * verdict; it is a fact to weigh against everything else the proxy brings.
     */
    List<String> cannotExpress();

    /** Takes the payment on behalf of the service next door, or throws. */
    Receipt forward(Payment payment);
}
