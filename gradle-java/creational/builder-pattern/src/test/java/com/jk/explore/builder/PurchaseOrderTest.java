package com.jk.explore.builder;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("PurchaseOrder.Builder — required fields, optional fields, immutability")
class PurchaseOrderTest {

    private static final Address HOME =
            new Address("14 Elm Street", "Leeds", "LS1 4AP", "UK");
    private static final LineItem MUG =
            new LineItem("MUG-01", "Ceramic mug", Money.pounds(8.50), 2);

    @Test
    @DisplayName("no options chained means every option defaults off")
    void defaultsAreAllOff() {
        PurchaseOrder order = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG)
                .shippingAddress(HOME)
                .build();

        assertAll(
                () -> assertFalse(order.isGiftWrapped()),
                () -> assertFalse(order.isPriority()),
                () -> assertTrue(order.giftMessage().isEmpty()),
                () -> assertTrue(order.couponCode().isEmpty()),
                () -> assertTrue(order.notes().isEmpty()));
    }

    @Test
    @DisplayName("building without any item is refused at build(), not one field at a time")
    void requiresAtLeastOneItem() {
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> PurchaseOrder.builder("ORD-1", "CUST-1").shippingAddress(HOME).build());

        assertTrue(e.getMessage().contains("item"), e.getMessage());
    }

    @Test
    @DisplayName("building without a shipping address is refused")
    void requiresAShippingAddress() {
        IllegalStateException e = assertThrows(IllegalStateException.class,
                () -> PurchaseOrder.builder("ORD-1", "CUST-1").addItem(MUG).build());

        assertTrue(e.getMessage().contains("address"), e.getMessage());
    }

    @Test
    @DisplayName("a gift message implies gift wrap, without the caller saying so twice")
    void giftMessageImpliesGiftWrap() {
        PurchaseOrder order = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG)
                .shippingAddress(HOME)
                .giftMessage("Happy birthday!")
                .build();

        assertAll(
                () -> assertTrue(order.isGiftWrapped()),
                () -> assertEquals("Happy birthday!", order.giftMessage().orElseThrow()));
    }

    @Test
    @DisplayName("gift wrap and priority shipping each add a flat fee")
    void feesStack() {
        Money itemsOnly = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG).shippingAddress(HOME).build().total();
        Money withGiftWrap = PurchaseOrder.builder("ORD-2", "CUST-1")
                .addItem(MUG).shippingAddress(HOME).giftWrap().build().total();
        Money withBoth = PurchaseOrder.builder("ORD-3", "CUST-1")
                .addItem(MUG).shippingAddress(HOME).giftWrap().priority().build().total();

        assertAll(
                () -> assertEquals(Money.pounds(17.00), itemsOnly),
                () -> assertEquals(Money.pounds(19.50), withGiftWrap),
                () -> assertEquals(Money.pounds(25.50), withBoth));
    }

    @Test
    @DisplayName("a coupon code takes 10% off the total, fees included")
    void couponDiscountsTheWholeTotal() {
        PurchaseOrder order = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG).shippingAddress(HOME).priority().couponCode("SAVE10").build();

        // (£17.00 + £6.00) * 0.9 = £20.70
        assertEquals(Money.pounds(20.70), order.total());
    }

    @Test
    @DisplayName("items() is a snapshot: mutating the source list after build() changes nothing")
    void itemsAreCopiedNotShared() {
        PurchaseOrder.Builder builder = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG).shippingAddress(HOME);
        PurchaseOrder order = builder.build();

        builder.addItem(new LineItem("BK-42", "Effective Java", Money.pounds(34.99), 1));

        assertEquals(1, order.items().size());
    }

    @Test
    @DisplayName("a builder used a second time does not reach back into the first order")
    void builderIsReusableWithoutMutatingEarlierOrders() {
        PurchaseOrder.Builder builder = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG).shippingAddress(HOME);

        PurchaseOrder first = builder.build();
        builder.priority();
        PurchaseOrder second = builder.build();

        assertAll(
                () -> assertFalse(first.isPriority()),
                () -> assertTrue(second.isPriority()));
    }

    @Test
    @DisplayName("items() cannot be modified by the caller")
    void itemsAreUnmodifiable() {
        PurchaseOrder order = PurchaseOrder.builder("ORD-1", "CUST-1")
                .addItem(MUG).shippingAddress(HOME).build();

        assertThrows(UnsupportedOperationException.class,
                () -> order.items().add(MUG));
    }
}
