package com.jk.explore.markerinterface;

/**
 * The pattern: empty interfaces that say something about a type. They have no methods; the name is the message.
 */
public final class Markers {

    /** Must travel cold. */
    public interface Perishable {
    }

    /** Must be wrapped against knocks. */
    public interface Fragile {
    }

    private Markers() {
    }
}
