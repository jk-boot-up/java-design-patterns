package com.jk.explore.mediator;

import java.util.List;

/**
 * The concrete mediator: the checkout page itself.
 *
 * <p>Every rule about how the form's parts affect one another lives in this one
 * class, in one method. Read {@link #changed} and you have read the entire
 * behaviour of the page; there is nowhere else for a rule to hide.
 *
 * <p>The widgets are created here and handed {@code this}, so the wiring is a
 * hub: five widgets, five references, all pointing at the same place.
 */
public class CheckoutForm implements CheckoutMediator {

    /** What is in the basket, before shipping and extras. */
    private static final int BASKET_POUNDS = 40;
    private static final int GIFT_WRAP_POUNDS = 2;

    private final CountrySelector country = new CountrySelector(this);
    private final ShippingSelector shipping = new ShippingSelector(this);
    private final GiftWrapCheckbox giftWrap = new GiftWrapCheckbox(this);
    private final TotalLabel total = new TotalLabel(this);
    private final PlaceOrderButton placeOrder = new PlaceOrderButton(this);

    public CheckoutForm() {
        // The form opens with no country chosen, so nothing is offered yet.
        shipping.showOptions(List.of());
        refreshTotal();
        refreshButton();
    }

    @Override
    public void changed(FormWidget source) {
        // The country is the only change that reshapes the form. The other two
        // only move the price.
        if (source == country) {
            shipping.showOptions(methodsFor(country.country()));
            giftWrap.setAvailable(isDomestic(country.country()));
        }
        refreshTotal();
        refreshButton();
    }

    /** The couriers that serve a country, and nothing else. */
    private static List<String> methodsFor(String country) {
        return isDomestic(country)
                ? List.of("Standard", "Express")
                : List.of("International");
    }

    private static boolean isDomestic(String country) {
        return "UK".equals(country);
    }

    /** What a courier charges. An unchosen method costs nothing yet. */
    private static int priceOf(String method) {
        return switch (method) {
            case "Standard" -> 3;
            case "Express" -> 6;
            case "International" -> 12;
            default -> 0;
        };
    }

    private void refreshTotal() {
        int sum = BASKET_POUNDS + priceOf(shipping.chosen());
        if (giftWrap.isTicked()) {
            sum += GIFT_WRAP_POUNDS;
        }
        total.show(sum);
    }

    private void refreshButton() {
        boolean ready = !country.country().isEmpty() && !shipping.chosen().isEmpty();
        placeOrder.setEnabled(ready);
    }

    public CountrySelector country() {
        return country;
    }

    public ShippingSelector shipping() {
        return shipping;
    }

    public GiftWrapCheckbox giftWrap() {
        return giftWrap;
    }

    public TotalLabel total() {
        return total;
    }

    public PlaceOrderButton placeOrder() {
        return placeOrder;
    }
}
