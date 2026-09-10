package com.jk.explore.mediator;

import java.util.ArrayList;
import java.util.List;

/**
 * The same checkout page, written the way it usually gets written first: each
 * widget holds the widgets it affects and updates them itself.
 *
 * <p>The whole tangle is gathered into this one file so it can be read at a
 * glance. In real code it would be five files, and that is the point — the
 * rules of the page would be scattered across all five, and no single file
 * would tell you what the page does.
 *
 * <p>It has two bugs. Both are the same bug really: a widget was updated and
 * one of the widgets that depended on it was forgotten. Neither throws.
 *
 * <ol>
 *   <li>Choosing a non-domestic country disables gift wrapping but leaves the
 *       box ticked, so the shopper is charged £2 for wrapping that the London
 *       warehouse will never do.</li>
 *   <li>Choosing a country clears the shipping method but leaves the Place
 *       Order button enabled, so an order can be placed with no courier on
 *       it.</li>
 * </ol>
 */
public class NaiveCheckoutForm {

    private static final int BASKET_POUNDS = 40;

    private final NaiveCountry country = new NaiveCountry();
    private final NaiveShipping shipping = new NaiveShipping();
    private final NaiveGiftWrap giftWrap = new NaiveGiftWrap();
    private final NaiveTotal total = new NaiveTotal();
    private final NaiveButton placeOrder = new NaiveButton();

    public NaiveCheckoutForm() {
        // Every widget must be handed every widget it might ever touch. Add a
        // sixth widget and this list, and several constructors, all change.
        country.wire(shipping, giftWrap, total, placeOrder);
        shipping.wire(giftWrap, total, placeOrder);
        giftWrap.wire(shipping, total);
    }

    public NaiveCountry country() {
        return country;
    }

    public NaiveShipping shipping() {
        return shipping;
    }

    public NaiveGiftWrap giftWrap() {
        return giftWrap;
    }

    public NaiveTotal total() {
        return total;
    }

    public NaiveButton placeOrder() {
        return placeOrder;
    }

    /** The country drop-down, which now has to know about four other widgets. */
    public static class NaiveCountry {
        private NaiveShipping shipping;
        private NaiveGiftWrap giftWrap;
        private NaiveTotal total;
        private NaiveButton button;
        private String country = "";

        void wire(NaiveShipping shipping, NaiveGiftWrap giftWrap,
                  NaiveTotal total, NaiveButton button) {
            this.shipping = shipping;
            this.giftWrap = giftWrap;
            this.total = total;
            this.button = button;
        }

        public String country() {
            return country;
        }

        public void select(String country) {
            this.country = country;

            shipping.showOptions("UK".equals(country)
                    ? List.of("Standard", "Express")
                    : List.of("International"));

            // BUG 1: withdrawn, but the tick is left behind.
            giftWrap.setAvailable("UK".equals(country));

            total.recalculate(shipping, giftWrap);

            // BUG 2: the shipping method was just cleared, and nobody told the
            // button. It stays as it was.
        }
    }

    /** The shipping drop-down, which knows about three others. */
    public static class NaiveShipping {
        private NaiveGiftWrap giftWrap;
        private NaiveTotal total;
        private NaiveButton button;
        private final List<String> options = new ArrayList<>();
        private String chosen = "";

        void wire(NaiveGiftWrap giftWrap, NaiveTotal total, NaiveButton button) {
            this.giftWrap = giftWrap;
            this.total = total;
            this.button = button;
        }

        void showOptions(List<String> newOptions) {
            options.clear();
            options.addAll(newOptions);
            chosen = "";
        }

        public List<String> options() {
            return List.copyOf(options);
        }

        public String chosen() {
            return chosen;
        }

        public void select(String method) {
            this.chosen = method;
            total.recalculate(this, giftWrap);
            button.setEnabled(true);
        }

        int price() {
            return switch (chosen) {
                case "Standard" -> 3;
                case "Express" -> 6;
                case "International" -> 12;
                default -> 0;
            };
        }
    }

    /** The gift-wrap box, which knows about two others. */
    public static class NaiveGiftWrap {
        private NaiveShipping shipping;
        private NaiveTotal total;
        private boolean available = true;
        private boolean ticked;

        void wire(NaiveShipping shipping, NaiveTotal total) {
            this.shipping = shipping;
            this.total = total;
        }

        void setAvailable(boolean available) {
            this.available = available;
        }

        public boolean isAvailable() {
            return available;
        }

        public boolean isTicked() {
            return ticked;
        }

        public void tick(boolean ticked) {
            if (!available) {
                return;
            }
            this.ticked = ticked;
            total.recalculate(shipping, this);
        }
    }

    /** The total, which has to be handed the widgets it needs to add up. */
    public static class NaiveTotal {
        private int pounds = BASKET_POUNDS;

        void recalculate(NaiveShipping shipping, NaiveGiftWrap giftWrap) {
            pounds = BASKET_POUNDS + shipping.price() + (giftWrap.isTicked() ? 2 : 0);
        }

        public int pounds() {
            return pounds;
        }

        public String text() {
            return "Total: £" + pounds;
        }
    }

    /** The button, told what to do by whichever widget remembers it. */
    public static class NaiveButton {
        private boolean enabled;

        void setEnabled(boolean enabled) {
            this.enabled = enabled;
        }

        public boolean isEnabled() {
            return enabled;
        }
    }
}
