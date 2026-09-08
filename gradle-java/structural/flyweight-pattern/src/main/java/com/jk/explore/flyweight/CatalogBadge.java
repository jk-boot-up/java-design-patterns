package com.jk.explore.flyweight;

/**
 * What a listing actually holds: a reference to a shared {@link BadgeStyle}
 * plus its own extrinsic state — which listing this is, and an optional
 * label override. This object is cheap regardless of how many listings
 * exist, because the expensive part, the {@link BadgeStyle}, is shared
 * across every listing of the same {@link BadgeType}.
 */
public final class CatalogBadge {

    private final BadgeStyle style;
    private final String listingId;
    private final String customLabel;

    public CatalogBadge(BadgeType type, String listingId, String customLabel) {
        this.style = BadgeStyleFactory.styleFor(type);
        this.listingId = listingId;
        this.customLabel = customLabel;
    }

    public BadgeStyle style() {
        return style;
    }

    public String render() {
        return style.render(listingId, customLabel);
    }
}
