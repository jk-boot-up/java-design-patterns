package com.jk.explore.abstractfactory;

public class DollarFormatter implements CurrencyFormatter {

    @Override
    public String currencyCode() {
        return "USD";
    }

    @Override
    public String format(double amount) {
        return String.format("$%,.2f", amount);
    }
}
