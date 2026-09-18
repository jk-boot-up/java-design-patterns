package com.jk.explore.externalisedconfig;

/**
 * The same checkout, with the threshold read from outside the program.
 *
 * <p>Compare the body of {@link #quote(Basket)} with the one in
 * {@link HardCodedCheckout}. The arithmetic is identical. The only change is
 * where the number comes from: a constant in the class becomes a read through a
 * {@link SettingsReader}, and that read happens <em>inside the method</em>.
 *
 * <p>That placement is the entire pattern, and it is the detail people get wrong.
 * Reading the value once in the constructor and keeping it in a field would look
 * tidier and would externalise nothing useful, because the value would then be
 * fixed for the life of the object — you would have swapped a rebuild for a
 * restart, which on a Saturday morning is not much of a trade. Reading it per
 * quote is what makes a change take effect on the next order.
 *
 * <p>The cost of reading per quote is a lookup, and in a real system a cached one
 * with a short refresh interval rather than a network call on every checkout. The
 * cost you cannot cache away is the one this project is really about: a number
 * that used to be governed by the compiler, a reviewer and a test suite is now
 * governed by whoever has the password to the config server.
 */
public final class ConfiguredCheckout implements Checkout {

    /**
     * The declaration of the setting: its name, the value to fall back on, and
     * the range the shop will believe.
     *
     * <p>Five pounds to two hundred. Below five pounds free delivery is being
     * given away on a basket of crisps; above two hundred nobody ever qualifies
     * and the promotion is broken in the other direction. Both ends are business
     * judgements rather than technical limits, which is exactly why they have to
     * be written down somewhere a program can enforce them.
     */
    public static final MoneySetting FREE_DELIVERY_OVER = new MoneySetting(
            "delivery.freeOver", Money.pounds(50), Money.pounds(5), Money.pounds(200));

    private final SettingsReader settings;
    private final Money standardDelivery;

    public ConfiguredCheckout(SettingsReader settings) {
        this(settings, Money.pence(499));
    }

    public ConfiguredCheckout(SettingsReader settings, Money standardDelivery) {
        this.settings = settings;
        this.standardDelivery = standardDelivery;
    }

    @Override
    public DeliveryQuote quote(Basket basket) {
        SettingValue threshold = settings.money(FREE_DELIVERY_OVER);
        Money cost = basket.goodsTotal().isAtLeast(threshold.amount())
                ? Money.zero()
                : standardDelivery;
        return new DeliveryQuote(basket, cost, threshold.amount(), threshold.origin());
    }

    @Override
    public String describe() {
        return "ConfiguredCheckout using " + settings.describe();
    }
}
