package com.jk.explore.abstractfactory;

public class RupeeFormatter implements CurrencyFormatter {

    @Override
    public String currencyCode() {
        return "INR";
    }

    @Override
    public String format(double amount) {
        return String.format("₹%,.2f", amount);
    }
}
