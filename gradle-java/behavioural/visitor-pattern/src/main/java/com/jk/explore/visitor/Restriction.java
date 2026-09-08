package com.jk.explore.visitor;

/**
 * Why an item cannot simply be put in a box and posted.
 *
 * <p>A field on the product rather than a subclass, deliberately. Adding a
 * node type to a Visitor design is expensive (see {@link CatalogVisitor});
 * adding a value to an enum is not. When the difference between two things
 * is data, keep it data.
 */
public enum Restriction {

    /** Nothing special — most of the catalog. */
    NONE("", ""),

    /** Air freight needs a dangerous-goods declaration for these. */
    LITHIUM_BATTERY("lithium cell", "UN3481 declaration required for air freight"),

    /** Age check at the door, so it cannot go to a parcel locker. */
    AGE_18("age 18+", "signature and ID on delivery, no locker drop"),

    /** Flammable contents — road only, and never by air. */
    FLAMMABLE("flammable", "road freight only, no air");

    private final String label;
    private final String obligation;

    Restriction(String label, String obligation) {
        this.label = label;
        this.obligation = obligation;
    }

    /** Whether this item has to appear on the compliance report at all. */
    public boolean isRestricted() {
        return this != NONE;
    }

    /** Short form, for the CSV column and the audit line. */
    public String label() {
        return label;
    }

    /** What the warehouse actually has to do about it. */
    public String obligation() {
        return obligation;
    }
}
