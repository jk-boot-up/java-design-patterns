package com.jk.explore.pageobject;

/**
 * The Page Object for the checkout page: the only class that knows its selectors and its timing.
 * Tests talk to it in shop terms.
 */
public final class CheckoutPage {

    static final String APPLY = "#apply-coupon";   // renamed from #apply-btn: the only edit needed
    static final String COUPON = "#coupon";
    static final String TOTAL = "#total";
    static final String STATUS = "#coupon-status";
    static final String PLACE_ORDER = "#place-order";

    private final FakeBrowser browser;

    public CheckoutPage(FakeBrowser browser) {
        this.browser = browser;
    }

    public CheckoutPage applyCoupon(String code) {
        browser.type(COUPON, code);
        browser.click(APPLY);
        for (int i = 0; i < 10 && !browser.text(STATUS).equals("applied"); i++) {
            // wait for the page to finish updating
        }
        return this;
    }

    public String total() {
        return browser.text(TOTAL);
    }

    public ConfirmationPage placeOrder() {
        browser.click(PLACE_ORDER);
        return new ConfirmationPage(browser);
    }
}
