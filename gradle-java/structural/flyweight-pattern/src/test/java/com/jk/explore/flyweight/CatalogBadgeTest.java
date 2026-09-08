package com.jk.explore.flyweight;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertSame;

class CatalogBadgeTest {

    @Test
    void twoBadgesOfTheSameTypeShareOneStyleInstance() {
        CatalogBadge first = new CatalogBadge(BadgeType.SALE, "LST-1002", null);
        CatalogBadge second = new CatalogBadge(BadgeType.SALE, "LST-1003", "Flash Sale");

        assertSame(first.style(), second.style());
    }

    @Test
    void renderCombinesTheSharedStyleWithThisBadgesOwnListingAndLabel() {
        CatalogBadge badge = new CatalogBadge(BadgeType.LOW_STOCK, "LST-1005", "Only 2 left");

        assertEquals("[LOW_STOCK] ⚠ Only 2 left on LST-1005 (bg=#6B7280, fg=#FFFFFF)", badge.render());
    }
}
