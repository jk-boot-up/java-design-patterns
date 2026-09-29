package com.jk.explore.pageobject;

import java.util.HashMap;
import java.util.Map;
import java.util.NoSuchElementException;

/**
 * A tiny stand-in for a real browser driver such as Selenium's WebDriver, showing the store's
 * checkout page. Applying a coupon updates the page a moment later, the way JavaScript does:
 * the new total only appears after a few more reads.
 */
public final class FakeBrowser {

    private final Map<String, String> elements = new HashMap<>();
    private final String applyId;
    private int readsUntilUpdate = -1;
    private String pendingTotal;
    private String page = "checkout";

    /** {@code applyId} lets the designers rename the apply button. */
    public FakeBrowser(String applyId) {
        this.applyId = applyId;
        elements.put("#coupon", "");
        elements.put(applyId, "Apply");
        elements.put("#total", "50.00");
        elements.put("#coupon-status", "");
        elements.put("#place-order", "Place order");
    }

    public void type(String selector, String text) {
        find(selector);
        elements.put(selector, text);
    }

    public void click(String selector) {
        find(selector);
        if (selector.equals(applyId) && elements.get("#coupon").equals("SAVE10")) {
            pendingTotal = "45.00";
            readsUntilUpdate = 3;   // the page updates a moment later
        } else if (selector.equals("#place-order")) {
            page = "confirmation";
            elements.clear();
            elements.put("#order-number", "ORD-1042");
            elements.put("#message", "Thank you for your order");
        }
    }

    public String text(String selector) {
        if (readsUntilUpdate > 0 && --readsUntilUpdate == 0) {
            elements.put("#total", pendingTotal);
            elements.put("#coupon-status", "applied");
        }
        return find(selector);
    }

    public String page() {
        return page;
    }

    private String find(String selector) {
        String value = elements.get(selector);
        if (value == null) {
            throw new NoSuchElementException("no element " + selector);
        }
        return value;
    }
}
