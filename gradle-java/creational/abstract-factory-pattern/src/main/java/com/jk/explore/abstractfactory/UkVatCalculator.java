package com.jk.explore.abstractfactory;

public class UkVatCalculator implements TaxCalculator {

    private static final double RATE = 0.20;

    @Override
    public String label() {
        return "VAT";
    }

    @Override
    public double taxOn(double subtotal) {
        return round(subtotal * RATE);
    }

    private static double round(double amount) {
        return Math.round(amount * 100.0) / 100.0;
    }
}
