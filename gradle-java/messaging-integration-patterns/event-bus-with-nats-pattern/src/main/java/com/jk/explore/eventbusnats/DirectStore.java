package com.jk.explore.eventbusnats;

/**
 * The store before there is a bus: every service is wired to every other one by hand.
 *
 * <p>Each wire is a network address one service has to be told about, and each one can be wrong, or point
 * at a service that is not running. The count is the cost.
 */
public class DirectStore {

    private final int services;

    public DirectStore(int services) {
        this.services = services;
    }

    /** Every service tells every other service directly, so each pair needs a wire in each direction. */
    public int wires() {
        return services * (services - 1);
    }

    /** What adding one more service costs: it must be told about all the others, and they about it. */
    public int wiresForOneMoreService() {
        return 2 * services;
    }

    /** With a bus, each service knows one address: the bus. */
    public int wiresThroughABus() {
        return services;
    }
}
