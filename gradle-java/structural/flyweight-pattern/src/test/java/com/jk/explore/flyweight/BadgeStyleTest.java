package com.jk.explore.flyweight;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class BadgeStyleTest {

    @Test
    void renderUsesTheTypeNameAsTheDefaultLabelWhenNoCustomLabelIsGiven() {
        BadgeStyle style = BadgeStyleFactory.styleFor(BadgeType.NEW);

        String rendered = style.render("LST-1001", null);

        assertEquals("[NEW] ✨ NEW on LST-1001 (bg=#2563EB, fg=#FFFFFF)", rendered);
    }

    @Test
    void renderUsesTheCustomLabelWhenOneIsGiven() {
        BadgeStyle style = BadgeStyleFactory.styleFor(BadgeType.LOW_STOCK);

        String rendered = style.render("LST-1005", "Only 2 left");

        assertEquals("[LOW_STOCK] ⚠ Only 2 left on LST-1005 (bg=#6B7280, fg=#FFFFFF)", rendered);
    }

    @Test
    void boldStylesUppercaseTheirLabel() {
        BadgeStyle sale = BadgeStyleFactory.styleFor(BadgeType.SALE);

        String rendered = sale.render("LST-1003", "Flash Sale");

        assertTrue(rendered.contains("FLASH SALE"));
    }

    @Test
    void artworkBytesMatchesTheSharedArtworkSize() {
        BadgeStyle style = BadgeStyleFactory.styleFor(BadgeType.BESTSELLER);

        assertEquals(64 * 1024, style.artworkBytes());
    }
}
