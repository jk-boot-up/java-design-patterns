package com.jk.explore.mediator;

/**
 * Runs the same three clicks through both checkout forms.
 *
 * <p>The shopper ticks gift wrap for a UK order, then changes their mind and
 * has it delivered to the United States instead. The tangled form charges them
 * for gift wrapping that will not happen, and lets them place an order with no
 * courier on it. The mediated form does neither, and it is not because anyone
 * remembered to handle this case — it is because there is only one place where
 * the reaction to a country change can be written.
 */
public final class CheckoutFormDemo {

    private CheckoutFormDemo() {
    }

    public static void main(String[] args) {
        System.out.println("=== Checkout form: every widget wired to every other ===\n");
        runNaive();

        System.out.println("\n=== Checkout form: every widget wired to the mediator ===\n");
        runMediated();
    }

    private static void runNaive() {
        NaiveCheckoutForm form = new NaiveCheckoutForm();

        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);
        System.out.println("UK, Express, gift wrapped");
        System.out.println("  " + form.total().text()
                + "   place order: " + (form.placeOrder().isEnabled() ? "enabled" : "disabled"));

        form.country().select("US");
        System.out.println("shopper changes the country to US");
        System.out.println("  shipping options : " + form.shipping().options());
        System.out.println("  shipping chosen  : "
                + (form.shipping().chosen().isEmpty() ? "(none)" : form.shipping().chosen()));
        System.out.println("  gift wrap        : offered=" + form.giftWrap().isAvailable()
                + ", ticked=" + form.giftWrap().isTicked()  + "   <-- still ticked");
        System.out.println("  " + form.total().text() + "   <-- £2 for wrapping that will not happen");
        System.out.println("  place order      : "
                + (form.placeOrder().isEnabled() ? "enabled" : "disabled")
                + "   <-- no courier chosen, and it will let them through");
    }

    private static void runMediated() {
        CheckoutForm form = new CheckoutForm();

        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);
        System.out.println("UK, Express, gift wrapped");
        System.out.println("  " + form.total().text()
                + "   place order: " + (form.placeOrder().isEnabled() ? "enabled" : "disabled"));

        form.country().select("US");
        System.out.println("shopper changes the country to US");
        System.out.println("  shipping options : " + form.shipping().options());
        System.out.println("  shipping chosen  : "
                + (form.shipping().chosen().isEmpty() ? "(none)" : form.shipping().chosen()));
        System.out.println("  gift wrap        : offered=" + form.giftWrap().isAvailable()
                + ", ticked=" + form.giftWrap().isTicked() + "   <-- withdrawn and cleared together");
        System.out.println("  " + form.total().text() + "   <-- basket only, nothing chosen yet");
        System.out.println("  place order      : "
                + (form.placeOrder().isEnabled() ? "enabled" : "disabled")
                + "   <-- the form re-checked itself");

        form.shipping().select("International");
        System.out.println("shopper picks International shipping");
        System.out.println("  " + form.total().text()
                + "   place order: " + (form.placeOrder().isEnabled() ? "enabled" : "disabled"));
    }
}
