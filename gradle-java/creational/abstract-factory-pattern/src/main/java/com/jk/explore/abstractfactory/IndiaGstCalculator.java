package com.jk.explore.abstractfactory;

public class IndiaGstCalculator implements TaxCalculator {

    private static final double RATE = 0.18;

    @Override
    public String label() {
        return "GST";
    }

    @Override
    public double taxOn(double subtotal) {
        return round(subtotal * RATE);
    }

    private static double round(double amount) {
        return Math.round(amount * 100.0) / 100.0;
    }
}
