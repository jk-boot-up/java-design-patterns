package com.jk.explore.abstractfactory;

/**
 * The abstract factory. It creates a whole <em>family</em> of products that
 * belong together — a market's tax rules, its currency and its address
 * format — and it guarantees the three always match.
 *
 * <p>Nothing here says how any of them are built, or which classes are
 * involved. A client that holds one of these cannot mix a British tax rate
 * with an American ZIP code, because it never picks the pieces itself.
 */
public interface MarketFactory {

    /** The market this family belongs to, for logs and receipts. */
    String market();

    TaxCalculator createTaxCalculator();

    CurrencyFormatter createCurrencyFormatter();

    AddressValidator createAddressValidator();
}
