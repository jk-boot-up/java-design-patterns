package com.jk.explore.privateclassdata;

/**
 * The pattern: the invoice keeps its figures in a private, unchangeable data object.
 *
 * <p>Its own methods can read the figures but cannot write them, so a
 * shortcut like the loose invoice's cannot compile. Working state that is
 * meant to change, such as how many times it was printed, stays an ordinary
 * field beside the data.
 */
public final class Invoice {

    private final InvoiceData data;
    private int timesPrinted;

    public Invoice(String number, String customer, long netPence) {
        this.data = new InvoiceData(number, customer, netPence);
    }

    public String printWithStaffDiscount(int percent) {
        timesPrinted++;
        long discounted = data.netPence() - data.netPence() * percent / 100;
        return data.number() + ": " + PrivateClassDataDemo.pounds(discounted);
    }

    public long netPence() {
        return data.netPence();
    }

    public int timesPrinted() {
        return timesPrinted;
    }

    public String customer() {
        return data.customer();
    }
}
