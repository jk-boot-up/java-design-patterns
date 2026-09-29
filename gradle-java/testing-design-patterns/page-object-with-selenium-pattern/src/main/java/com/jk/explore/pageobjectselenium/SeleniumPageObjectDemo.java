package com.jk.explore.pageobjectselenium;

import java.util.ArrayList;
import java.util.List;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

/**
 * The five acts: a real Chromium browser, driven by Selenium, on the shop's real checkout page.
 */
public final class SeleniumPageObjectDemo {

    static final int TESTS = 5;

    public static void main(String[] args) throws Exception {
        if (!Browser.containerRuntimeAvailable()) {
            System.out.println(Browser.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        java.util.logging.Logger.getLogger("org.openqa.selenium").setLevel(java.util.logging.Level.OFF);   // Selenium's own log lines
        try (ShopSite site = new ShopSite(); Browser browser = new Browser(site.port())) {
            try {
                browser.start();
            } catch (RuntimeException e) {
                out.add(Browser.WOULD_NOT_START_ADVICE);
                return out;
            }
            WebDriver driver = browser.newSession();
            try {
                out.add("ONE. A test that clicks selectors itself, in a real browser.");
                out.add("  type #coupon, click #apply-btn, read #total: " + rawTest(driver, browser.checkoutUrl(), "apply-btn"));
                out.add("  the coupon was applied, but the test read the total before the page updated");

                out.add("");
                out.add("TWO. The designers rename #apply-btn to #apply-coupon.");
                site.renameApplyButton("apply-coupon");
                int passed = 0;
                for (int i = 0; i < TESTS; i++) {
                    try {
                        rawTest(driver, browser.checkoutUrl(), "apply-btn");
                        passed++;
                    } catch (org.openqa.selenium.NoSuchElementException gone) {
                        // the test fails
                    }
                }
                out.add("  " + TESTS + " coupon tests that name the selector themselves: " + passed + " of " + TESTS
                        + " pass (NoSuchElementException)");

                out.add("");
                out.add("THREE. A Page Object knows the page; tests speak in shop terms.");
                passed = 0;
                for (int i = 0; i < TESTS; i++) {
                    if (CheckoutPage.open(driver, browser.checkoutUrl()).applyCoupon("SAVE10").total().equals("45.00")) {
                        passed++;
                    }
                }
                out.add("  " + TESTS + " tests using CheckoutPage, after one selector is changed in it: " + passed + " of " + TESTS + " pass");
                CheckoutPage checkout = CheckoutPage.open(driver, browser.checkoutUrl());
                out.add("  checkout.applyCoupon(\"SAVE10\").total(): " + checkout.applyCoupon("SAVE10").total()
                        + "  (it waits with WebDriverWait until the page has answered)");

                out.add("");
                out.add("FOUR. Actions that change the page return the next page.");
                ConfirmationPage confirmation = checkout.placeOrder();
                out.add("  checkout.placeOrder() -> ConfirmationPage: " + confirmation.orderNumber() + ", \"" + confirmation.message() + "\"");

                out.add("");
                out.add("FIVE. The bill: one more layer, and a real browser to run.");
                out.add("  every page needs its object, kept in step with the real page");
                out.add("  the checks stay in the tests: page objects report, tests decide");
                out.add("  and browser tests are slow: this demo started a browser in a container, and each page load is real");
            } finally {
                driver.quit();
            }
        }
        return out;
    }

    /** A test that knows the selectors itself. Returns the total it saw straight after clicking. */
    private static String rawTest(WebDriver driver, String url, String applyId) {
        driver.get(url);
        driver.findElement(By.id("coupon")).sendKeys("SAVE10");
        driver.findElement(By.id(applyId)).click();
        return driver.findElement(By.id("total")).getText();
    }

    private SeleniumPageObjectDemo() {
    }
}
