package com.jk.explore.flyweight;

import java.util.Arrays;

/**
 * Attempt one, kept around as the trap. Every listing builds its own badge
 * top to bottom — including its own copy of the artwork — even though two
 * listings marked {@code SALE} want an identical badge. Nothing here is
 * wrong on its own; the bug is that intrinsic state (the artwork, the
 * colours, the icon) is duplicated once per listing instead of once per
 * badge type.
 */
public final class NaiveListingBadge {

    private final BadgeType type;
    private final String icon;
    private final String backgroundColor;
    private final String textColor;
    private final boolean bold;
    private final byte[] artwork;
    private final String listingId;

    public NaiveListingBadge(BadgeType type, String listingId) {
        this.listingId = listingId;
        this.type = type;
        this.artwork = new byte[BadgeStyle.ARTWORK_BYTES];
        Arrays.fill(this.artwork, (byte) type.ordinal());
        switch (type) {
            case NEW -> {
                this.icon = "✨";
                this.backgroundColor = "#2563EB";
                this.textColor = "#FFFFFF";
                this.bold = false;
            }
            case SALE -> {
                this.icon = "★";
                this.backgroundColor = "#DC2626";
                this.textColor = "#FFFFFF";
                this.bold = true;
            }
            case BESTSELLER -> {
                this.icon = "👑";
                this.backgroundColor = "#D97706";
                this.textColor = "#111827";
                this.bold = true;
            }
            case LOW_STOCK -> {
                this.icon = "⚠";
                this.backgroundColor = "#6B7280";
                this.textColor = "#FFFFFF";
                this.bold = false;
            }
            default -> throw new IllegalArgumentException("Unknown badge type: " + type);
        }
    }

    public int artworkBytes() {
        return artwork.length;
    }

    public String render() {
        String label = type.name().replace('_', ' ');
        String text = bold ? label.toUpperCase() : label;
        return "[%s] %s %s on %s (bg=%s, fg=%s)"
                .formatted(type, icon, text, listingId, backgroundColor, textColor);
    }
}
