package com.jk.explore.interpreterspel;

/** The context: one order, and everything a rule may ask about. Getters, because SpEL reads properties. */
public class Order {

    private final String country;
    private final long basketPence;
    private final int items;
    private final boolean firstOrder;
    private final String voucher;

    public Order(String country, long basketPence, int items, boolean firstOrder, String voucher) {
        this.country = country;
        this.basketPence = basketPence;
        this.items = items;
        this.firstOrder = firstOrder;
        this.voucher = voucher;
    }

    public String getCountry() { return country; }
    public long getBasketPence() { return basketPence; }
    public int getItems() { return items; }
    public boolean isFirstOrder() { return firstOrder; }
    public String getVoucher() { return voucher; }
}
