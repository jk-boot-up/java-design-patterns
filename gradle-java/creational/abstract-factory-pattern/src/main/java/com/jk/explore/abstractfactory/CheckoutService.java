package com.jk.explore.abstractfactory;

/**
 * The client. It is handed one factory, asks it for the three products it
 * needs, and then works entirely through their interfaces.
 *
 * <p>Read this class looking for the words "UK", "US" or "India". There are
 * none. It has no idea which market it is running in, and it could not
 * assemble a mismatched family even if it tried.
 */
public class CheckoutService {

    private final String market;
    private final TaxCalculator tax;
    private final CurrencyFormatter money;
    private final AddressValidator addresses;

    public CheckoutService(MarketFactory factory) {
        this.market = factory.market();
        this.tax = factory.createTaxCalculator();
        this.money = factory.createCurrencyFormatter();
        this.addresses = factory.createAddressValidator();
    }

    public Quote quote(Order order) {
        if (!addresses.isValid(order.postcode())) {
            throw new IllegalArgumentException(
                    "\"" + order.postcode() + "\" is not a valid " + market + " "
                            + addresses.postcodeLabel());
        }

        System.out.println("Checkout: " + market + " order " + order.orderId()
                + " to " + addresses.postcodeLabel() + " " + order.postcode());

        double taxAmount = tax.taxOn(order.subtotal());
        double total = order.subtotal() + taxAmount;

        System.out.println("Checkout: " + tax.label() + " of "
                + money.format(taxAmount) + " on " + money.format(order.subtotal()));
        System.out.println("Checkout: total " + money.format(total)
                + " " + money.currencyCode());

        return new Quote(market, money.format(order.subtotal()), tax.label(),
                money.format(taxAmount), money.format(total));
    }
}
