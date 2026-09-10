package com.jk.explore.mediator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * These tests pin the tangled form's bugs in place rather than fixing them.
 *
 * <p>Asserting the wrong answer is deliberate. It makes the cost of the design
 * something the build states out loud, and if someone ever patches
 * {@code NaiveCheckoutForm} these tests fail and say so.
 */
class NaiveCheckoutFormTest {

    @Test
    @DisplayName("the tangled form is right as long as nothing changes twice")
    void happyPathLooksFine() {
        NaiveCheckoutForm form = new NaiveCheckoutForm();

        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);

        assertEquals(48, form.total().pounds());
        assertTrue(form.placeOrder().isEnabled());
    }

    @Test
    @DisplayName("BUG: gift wrap is withdrawn but stays ticked, and stays charged")
    void chargesForWrappingItWillNotDo() {
        NaiveCheckoutForm form = new NaiveCheckoutForm();
        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);

        form.country().select("US");

        assertFalse(form.giftWrap().isAvailable());
        assertTrue(form.giftWrap().isTicked(), "the tick outlives the offer");
        // £40 basket + £0 (shipping was cleared) + £2 for phantom gift wrap.
        assertEquals(42, form.total().pounds());
    }

    @Test
    @DisplayName("BUG: the shipping method is cleared but the button stays enabled")
    void letsAnOrderThroughWithNoCourier() {
        NaiveCheckoutForm form = new NaiveCheckoutForm();
        form.country().select("UK");
        form.shipping().select("Express");
        assertTrue(form.placeOrder().isEnabled());

        form.country().select("US");

        assertEquals("", form.shipping().chosen(), "no courier is selected");
        assertTrue(form.placeOrder().isEnabled(), "and the order can still be placed");
    }

    @Test
    @DisplayName("the mediated form gets both of those right without being told to")
    void mediatedFormDisagrees() {
        CheckoutForm form = new CheckoutForm();
        form.country().select("UK");
        form.shipping().select("Express");
        form.giftWrap().tick(true);

        form.country().select("US");

        assertFalse(form.giftWrap().isTicked());
        assertEquals(40, form.total().pounds());
        assertFalse(form.placeOrder().isEnabled());
    }
}
