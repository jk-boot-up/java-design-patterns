package com.jk.explore.abstractfactory;

/**
 * One concrete factory: the American family.
 */
public class UsMarketFactory implements MarketFactory {

    @Override
    public String market() {
        return "United States";
    }

    @Override
    public TaxCalculator createTaxCalculator() {
        return new UsSalesTaxCalculator();
    }

    @Override
    public CurrencyFormatter createCurrencyFormatter() {
        return new DollarFormatter();
    }

    @Override
    public AddressValidator createAddressValidator() {
        return new UsZipValidator();
    }
}
