package com.jk.explore.immutable;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import java.util.Map;
import org.junit.jupiter.api.Test;

class ImmutableTest {

    @Test
    void withMakesANewAddressAndLeavesTheOldOne() {
        Address a = new Address("4 Mill Lane", "Leeds");
        Address b = a.withCity("York");
        assertNotSame(a, b);
        assertEquals("Leeds", a.city());
        assertEquals("York", b.city());
    }

    @Test
    void equalAddressesAreEqual() {
        assertEquals(new Address("x", "y"), new Address("x", "y"));
        assertEquals(new Address("x", "y").hashCode(), new Address("x", "y").hashCode());
    }

    @Test
    void saleLeavesTheOriginalList() {
        PriceList list = new PriceList(ImmutableObjectDemo.startPrices());
        PriceList sale = list.withSale(10);
        assertEquals(6500, list.total(ImmutableObjectDemo.BASKET));
        assertEquals(5850, sale.total(ImmutableObjectDemo.BASKET));
    }

    @Test
    void constructorCopiesItsInput() {
        Map<String, Long> input = ImmutableObjectDemo.startPrices();
        PriceList list = new PriceList(input);
        input.put("kettle", 1L);
        assertEquals(3000L, list.prices().get("kettle"));
    }

    @Test
    void pricesCannotBeChangedFromOutside() {
        PriceList list = new PriceList(ImmutableObjectDemo.startPrices());
        assertThrows(UnsupportedOperationException.class, () -> list.prices().put("kettle", 1L));
    }

    @Test
    void shopSwapsWholeLists() {
        Shop shop = new Shop(new PriceList(ImmutableObjectDemo.startPrices()));
        PriceList before = shop.prices();
        shop.publish(before.withPrice("mug", 500));
        assertEquals(1000L, before.prices().get("mug"));
        assertEquals(500L, shop.prices().prices().get("mug"));
    }

    @Test
    void mutableListShowsHalfAppliedChanges() {
        MutablePriceList list = new MutablePriceList(ImmutableObjectDemo.startPrices());
        list.set("kettle", 2700);
        assertEquals(6200, list.total(List.of("kettle", "mug", "teapot")));
    }
}
