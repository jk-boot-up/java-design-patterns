package com.jk.explore.abstractfactory;

/**
 * One concrete factory: the British family. Every method here returns a
 * British product, and that consistency is the factory's whole job.
 */
public class UkMarketFactory implements MarketFactory {

    @Override
    public String market() {
        return "United Kingdom";
    }

    @Override
    public TaxCalculator createTaxCalculator() {
        return new UkVatCalculator();
    }

    @Override
    public CurrencyFormatter createCurrencyFormatter() {
        return new PoundFormatter();
    }

    @Override
    public AddressValidator createAddressValidator() {
        return new UkPostcodeValidator();
    }
}
