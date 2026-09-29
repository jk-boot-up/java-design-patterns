package com.jk.explore.privateclassdata;

/**
 * Without the pattern: the invoice's figures are ordinary fields, so its own methods can change them.
 *
 * <p>{@code printWithStaffDiscount} takes a shortcut and subtracts the
 * discount from the stored total before printing. Print it twice, and the
 * discount is taken twice, from the invoice itself.
 */
public final class LooseInvoice {

    private final String number;
    private long netPence;

    public LooseInvoice(String number, long netPence) {
        this.number = number;
        this.netPence = netPence;
    }

    public String printWithStaffDiscount(int percent) {
        netPence = netPence - netPence * percent / 100;
        return number + ": " + PrivateClassDataDemo.pounds(netPence);
    }

    public long netPence() {
        return netPence;
    }
}
