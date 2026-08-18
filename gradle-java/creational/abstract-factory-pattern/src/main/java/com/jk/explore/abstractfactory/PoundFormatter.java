package com.jk.explore.abstractfactory;

public class PoundFormatter implements CurrencyFormatter {

    @Override
    public String currencyCode() {
        return "GBP";
    }

    @Override
    public String format(double amount) {
        return String.format("£%,.2f", amount);
    }
}
