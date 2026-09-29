package com.jk.explore.pageobject;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;

/**
 * The five acts: tests full of selectors, a renamed button, the page object, waiting in one place,
 * and the bill.
 */
public final class PageObjectDemo {

    static final String OLD_BUTTON = "#apply-btn";
    static final String NEW_BUTTON = "#apply-coupon";
    static final int TESTS = 5;

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Tests click selectors directly.");
        FakeBrowser raw = new FakeBrowser(OLD_BUTTON);
        raw.type("#coupon", "SAVE10");
        raw.click(OLD_BUTTON);
        out.add("  type #coupon, click #apply-btn, read #total: " + raw.text("#total"));
        out.add("  the coupon was applied, but the test read the total before the page updated");

        out.add("");
        out.add("TWO. The designers rename #apply-btn to #apply-coupon.");
        out.add("  " + TESTS + " coupon tests that name the selector themselves: "
                + passing(b -> rawTest(b, OLD_BUTTON), NEW_BUTTON) + " of " + TESTS + " pass");
        out.add("  every test must be found and edited");

        out.add("");
        out.add("THREE. A Page Object knows the page; tests speak in shop terms.");
        out.add("  " + TESTS + " tests using CheckoutPage, after one selector is changed in it: "
                + passing(b -> new CheckoutPage(b).applyCoupon("SAVE10").total(), NEW_BUTTON)
                + " of " + TESTS + " pass");
        CheckoutPage checkout = new CheckoutPage(new FakeBrowser(NEW_BUTTON));
        out.add("  checkout.applyCoupon(\"SAVE10\").total(): " + checkout.applyCoupon("SAVE10").total());
        out.add("  the page object waits for the update, so no test has to");

        out.add("");
        out.add("FOUR. Actions that change the page return the next page.");
        ConfirmationPage confirmation = checkout.placeOrder();
        out.add("  checkout.placeOrder() -> ConfirmationPage: " + confirmation.orderNumber() + ", \""
                + confirmation.message() + "\"");
        out.add("  the test cannot ask the checkout page for an order number by mistake");

        out.add("");
        out.add("FIVE. The bill: one more layer to look after.");
        out.add("  every page needs its object, kept in step with the real page");
        out.add("  and the checks stay in the tests: page objects report, tests decide");
        return out;
    }

    /** A test that knows the selectors itself. Returns the total it saw. */
    private static String rawTest(FakeBrowser browser, String applyButton) {
        browser.type("#coupon", "SAVE10");
        browser.click(applyButton);
        return browser.text("#total");
    }

    /** Runs the same coupon test {@link #TESTS} times against a page whose button has {@code buttonId}. */
    private static int passing(Function<FakeBrowser, String> test, String buttonId) {
        int passed = 0;
        for (int i = 0; i < TESTS; i++) {
            try {
                if (test.apply(new FakeBrowser(buttonId)).equals("45.00")) {
                    passed++;
                }
            } catch (RuntimeException missing) {
                // no such element: the test fails
            }
        }
        return passed;
    }

    private PageObjectDemo() {
    }
}
