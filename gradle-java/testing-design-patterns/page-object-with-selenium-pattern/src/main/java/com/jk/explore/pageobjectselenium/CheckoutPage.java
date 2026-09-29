package com.jk.explore.pageobjectselenium;

import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * The Page Object for the checkout page: the only class that knows its selectors and its timing.
 * Tests talk to it in shop terms.
 */
public final class CheckoutPage {

    static final By COUPON = By.id("coupon");
    static final By APPLY = By.id("apply-coupon");     // renamed from apply-btn: the only edit needed
    static final By TOTAL = By.id("total");
    static final By STATUS = By.id("coupon-status");
    static final By PLACE_ORDER = By.id("place-order");

    private final WebDriver driver;

    public CheckoutPage(WebDriver driver) {
        this.driver = driver;
    }

    public static CheckoutPage open(WebDriver driver, String url) {
        driver.get(url);
        return new CheckoutPage(driver);
    }

    /** Types the code, clicks apply, and waits until the page says whether it worked. */
    public CheckoutPage applyCoupon(String code) {
        driver.findElement(COUPON).sendKeys(code);
        driver.findElement(APPLY).click();
        new WebDriverWait(driver, Duration.ofSeconds(5)).until(
                ExpectedConditions.not(ExpectedConditions.textToBe(STATUS, "")));
        return this;
    }

    public String total() {
        return driver.findElement(TOTAL).getText();
    }

    public ConfirmationPage placeOrder() {
        driver.findElement(PLACE_ORDER).click();
        return new ConfirmationPage(driver);
    }
}
