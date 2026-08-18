package com.jk.explore.abstractfactory;

public class UsSalesTaxCalculator implements TaxCalculator {

    private static final double RATE = 0.08875;

    @Override
    public String label() {
        return "Sales Tax";
    }

    @Override
    public double taxOn(double subtotal) {
        return round(subtotal * RATE);
    }

    private static double round(double amount) {
        return Math.round(amount * 100.0) / 100.0;
    }
}
