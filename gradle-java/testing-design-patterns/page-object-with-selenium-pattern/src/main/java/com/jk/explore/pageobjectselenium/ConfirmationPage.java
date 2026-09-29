package com.jk.explore.pageobjectselenium;

import java.time.Duration;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

/**
 * The Page Object for the page shown after placing an order.
 */
public final class ConfirmationPage {

    private final WebDriver driver;

    ConfirmationPage(WebDriver driver) {
        this.driver = driver;
        new WebDriverWait(driver, Duration.ofSeconds(5)).until(ExpectedConditions.presenceOfElementLocated(By.id("order-number")));
    }

    public String orderNumber() {
        return driver.findElement(By.id("order-number")).getText();
    }

    public String message() {
        return driver.findElement(By.id("message")).getText();
    }
}
