package com.jk.explore.mediator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The mediated form: one rule, in one place, applied every time. */
class CheckoutFormTest {

    @Test
    @DisplayName("a fresh form offers nothing and cannot be submitted")
    void freshFormIsEmpty() {
        CheckoutForm form = new CheckoutForm();

        assertEquals(List.of(), form.shipping().options());
        assertEquals(40, form.total().pounds());
        assertFalse(form.placeOrder().isEnabled());
    }

    @Test
    @DisplayName("choosing a country refills the shipping options")
    void countryDrivesShippingOptions() {
        CheckoutForm form = new CheckoutForm();

        form.country().select("UK");
        assertEquals(List.of("Standard", "Express"), form.shipping().options());

        form.country().select("US");
        assertEquals(List.of("International"), form.shipping().options());
    }

    @Test
    @DisplayName("the total follows shipping and gift wrap")
    void totalAddsUp() {
        CheckoutForm form = new CheckoutForm();

        form.country().select("UK");
        form.shipping().select("Express");
        assertEquals(46, form.total().pounds());

        form.giftWrap().tick(true);
        assertEquals(48, form.total().pounds());
    }

    @Test
    @DisplayName("going overseas withdraws gift wrap AND clears the tick")
    void withdrawingGiftWrapAlsoClearsIt() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);
        assertEquals(48, form.total().pounds());

        form.country().select("US");

        assertFalse(form.giftWrap().isAvailable());
        assertFalse(form.giftWrap().isTicked());
        // Basket only: shipping was cleared too, and nothing has been re-picked.
        assertEquals(40, form.total().pounds());
    }

    @Test
    @DisplayName("clearing the shipping method disables the button again")
    void countryChangeDisablesTheButton() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("UK");
        form.shipping().select("Express");
        assertTrue(form.placeOrder().isEnabled());

        form.country().select("US");

        assertEquals("", form.shipping().chosen());
        assertFalse(form.placeOrder().isEnabled());
    }

    @Test
    @DisplayName("picking a method from the new list enables the button")
    void repickingReEnablesTheButton() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("US");

        form.shipping().select("International");

        assertTrue(form.placeOrder().isEnabled());
        assertEquals(52, form.total().pounds());
    }

    @Test
    @DisplayName("coming home again offers gift wrap back, but does not re-tick it")
    void comingHomeAgainLeavesNothingStuck() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("UK");
        form.giftWrap().tick(true);
        form.country().select("US");

        form.country().select("UK");

        // The option is offered again, because availability is recomputed from
        // the country every time rather than remembered.
        assertTrue(form.giftWrap().isAvailable());
        // But the tick is not restored: the shopper unticked nothing, the form
        // withdrew it, and guessing that they still want it would be inventing
        // an answer. Nothing here is left in a stale state either way.
        assertFalse(form.giftWrap().isTicked());
        assertEquals(List.of("Standard", "Express"), form.shipping().options());
        assertEquals(40, form.total().pounds());
        assertFalse(form.placeOrder().isEnabled());
    }

    @Test
    @DisplayName("a withdrawn gift-wrap box cannot be ticked at all")
    void withdrawnBoxIgnoresClicks() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("US");

        form.giftWrap().tick(true);

        assertFalse(form.giftWrap().isTicked());
        assertEquals(40, form.total().pounds());
    }
}
