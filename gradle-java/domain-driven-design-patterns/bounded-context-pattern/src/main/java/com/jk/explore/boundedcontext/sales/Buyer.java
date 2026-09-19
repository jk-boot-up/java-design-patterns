package com.jk.explore.boundedcontext.sales;

import com.jk.explore.boundedcontext.shared.CustomerId;

import java.time.LocalDate;

/** In Sales, a customer is a buyer: someone with a credit limit and a purchase history. Active means bought lately. */
public record Buyer(CustomerId id, String name, long creditLimitPence, LocalDate lastPurchase) {

    public boolean isActive(LocalDate today) {
        return !lastPurchase.isBefore(today.minusDays(90));
    }
}
