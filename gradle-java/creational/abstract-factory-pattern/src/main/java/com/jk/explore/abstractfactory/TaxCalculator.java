package com.jk.explore.abstractfactory;

/**
 * One member of the product family: how much tax this market charges,
 * and what that market calls it.
 */
public interface TaxCalculator {

    String label();

    double taxOn(double subtotal);
}
