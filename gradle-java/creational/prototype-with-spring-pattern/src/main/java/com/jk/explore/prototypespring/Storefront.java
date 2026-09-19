package com.jk.explore.prototypespring;

import jakarta.annotation.PreDestroy;
import org.springframework.beans.factory.ObjectProvider;
import org.springframework.stereotype.Component;

import java.util.concurrent.atomic.AtomicInteger;

/**
 * A singleton that needs listings. The constructor receives a Listing once, at startup;
 * the provider can build a new one on every call.
 */
@Component
public class Storefront {

    static final AtomicInteger DESTROYED = new AtomicInteger();

    private final Listing injectedOnce;
    private final ObjectProvider<Listing> listings;

    public Storefront(Listing injectedOnce, ObjectProvider<Listing> listings) {
        this.injectedOnce = injectedOnce;
        this.listings = listings;
    }

    /** The trap: the same object on every call, for the life of the container. */
    public Listing draftInjectedOnce() {
        return injectedOnce;
    }

    /** The fix: a new listing on every call. */
    public Listing freshDraft() {
        return listings.getObject();
    }

    @PreDestroy
    void close() {
        DESTROYED.incrementAndGet();
    }
}
