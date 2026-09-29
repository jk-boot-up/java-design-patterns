package com.jk.explore.lenses;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.List;
import org.junit.jupiter.api.Test;

/**
 * The three rules every lens must keep, checked on the joined ORDER_POSTCODE lens.
 */
class LensLawsTest {

    private final Order order = new Order("O", new Customer("Ana", new Address("s", "c", "P1")), List.of());
    private final Lens<Order, String> lens = Lenses.ORDER_POSTCODE;

    @Test
    void getWhatYouSet() {
        assertEquals("P2", lens.get().apply(lens.set().apply(order, "P2")));
    }

    @Test
    void settingWhatIsThereChangesNothing() {
        assertEquals(order, lens.set().apply(order, lens.get().apply(order)));
    }

    @Test
    void lastSetWins() {
        assertEquals(lens.set().apply(order, "P3"), lens.set().apply(lens.set().apply(order, "P2"), "P3"));
    }
}
