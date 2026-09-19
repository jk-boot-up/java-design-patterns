package com.jk.explore.boundedcontext.naive;

import java.time.LocalDate;

/**
 * One Customer for the whole company. Every context added what it needed, so every context now depends on
 * everyone else's fields, and "active" has to mean three things at once.
 */
public class GodCustomer {
    public String id;
    public String name;
    public long creditLimitPence;
    public LocalDate lastPurchase;
    public String address;
    public int parcelsInTransit;
    public String deliveryNotes;
    public String phone;
    public int openTickets;
    public String preferredContactHour;
    public boolean marketingConsent;
    public String loyaltyTier;

    /** Sales wants one answer, Shipping another and Support a third. This is the one somebody picked. */
    public boolean isActive(LocalDate today) {
        return lastPurchase != null && !lastPurchase.isBefore(today.minusDays(90));
    }

    public static int fieldCount() {
        return GodCustomer.class.getDeclaredFields().length;
    }
}
