package com.jk.explore.abstractfactory;

/**
 * One concrete factory: the Indian family.
 */
public class IndiaMarketFactory implements MarketFactory {

    @Override
    public String market() {
        return "India";
    }

    @Override
    public TaxCalculator createTaxCalculator() {
        return new IndiaGstCalculator();
    }

    @Override
    public CurrencyFormatter createCurrencyFormatter() {
        return new RupeeFormatter();
    }

    @Override
    public AddressValidator createAddressValidator() {
        return new IndiaPinValidator();
    }
}
