package com.jk.explore.pageobject;

/**
 * The Page Object for the page shown after placing an order.
 */
public final class ConfirmationPage {

    private final FakeBrowser browser;

    ConfirmationPage(FakeBrowser browser) {
        this.browser = browser;
    }

    public String orderNumber() {
        return browser.text("#order-number");
    }

    public String message() {
        return browser.text("#message");
    }
}
