package com.jk.explore.flyweight;

import java.util.Arrays;

/**
 * The flyweight. Everything here is intrinsic state: it depends only on the
 * badge type, never on which listing wears the badge, so one instance per
 * {@link BadgeType} is enough for the whole catalog.
 *
 * <p>{@code artwork} stands in for the rasterised icon a real badge would
 * carry — a sprite, an SVG render, whatever a design system hands over. It
 * is the field that makes sharing worth doing: {@link #ARTWORK_BYTES} of
 * pixels, repeated once per badge type instead of once per listing.
 */
public final class BadgeStyle {

    static final int ARTWORK_BYTES = 64 * 1024;

    private final BadgeType type;
    private final String icon;
    private final String backgroundColor;
    private final String textColor;
    private final boolean bold;
    private final byte[] artwork;

    BadgeStyle(BadgeType type, String icon, String backgroundColor, String textColor, boolean bold) {
        this.type = type;
        this.icon = icon;
        this.backgroundColor = backgroundColor;
        this.textColor = textColor;
        this.bold = bold;
        this.artwork = new byte[ARTWORK_BYTES];
        Arrays.fill(this.artwork, (byte) type.ordinal());
    }

    public BadgeType type() {
        return type;
    }

    public int artworkBytes() {
        return artwork.length;
    }

    /**
     * Renders this style for one specific listing. {@code listingId} and
     * {@code customLabel} are extrinsic state — supplied by the caller at
     * render time, never stored on the flyweight itself.
     */
    public String render(String listingId, String customLabel) {
        String label = customLabel != null ? customLabel : type.name().replace('_', ' ');
        String text = bold ? label.toUpperCase() : label;
        return "[%s] %s %s on %s (bg=%s, fg=%s)"
                .formatted(type, icon, text, listingId, backgroundColor, textColor);
    }
}
