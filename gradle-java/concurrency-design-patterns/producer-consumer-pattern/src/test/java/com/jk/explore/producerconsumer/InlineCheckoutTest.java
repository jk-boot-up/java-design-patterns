package com.jk.explore.producerconsumer;

import com.jk.explore.producerconsumer.domain.Order;
import com.jk.explore.producerconsumer.harness.Gate;
import com.jk.explore.producerconsumer.naive.InlineCheckout;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class InlineCheckoutTest {

    @Test
    void checkoutDoesNotReturnUntilPackingFinishes() throws InterruptedException {
        Gate packDone = new Gate();
        InlineCheckout checkout = new InlineCheckout(order -> packDone.awaitOpen());

        // The gate is opened from a second thread only after we can prove
        // the checkout call is already blocked inside packing — a bounded
        // join on the checkout thread with the gate still closed stands in
        // for "it has not returned", without any sleep.
        Thread checkoutThread = new Thread(() -> checkout.checkout(new Order("ord-1", "BNS-220")));
        checkoutThread.start();

        checkoutThread.join(100);
        assertTrue(checkoutThread.isAlive(), "checkout must still be blocked on packing");

        packDone.open();
        checkoutThread.join(2_000);
        assertEquals(1, checkout.packed().size());
    }
}
