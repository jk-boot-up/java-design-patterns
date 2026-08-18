package com.jk.explore.abstractfactory;

/**
 * One member of the product family: how this market writes an amount of
 * money, and which currency that amount is in.
 */
public interface CurrencyFormatter {

    String currencyCode();

    String format(double amount);
}
