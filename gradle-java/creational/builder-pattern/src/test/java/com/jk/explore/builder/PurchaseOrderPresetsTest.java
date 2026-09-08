package com.jk.explore.builder;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("PurchaseOrderPresets — fixed recipes driven through the builder's own methods")
class PurchaseOrderPresetsTest {

    private static final Address HOME =
            new Address("14 Elm Street", "Leeds", "LS1 4AP", "UK");
    private static final LineItem MUG =
            new LineItem("MUG-01", "Ceramic mug", Money.pounds(8.50), 2);

    @Test
    @DisplayName("giftOrder wraps and attaches the message, and nothing else")
    void giftOrderWrapsWithMessage() {
        PurchaseOrder order = PurchaseOrderPresets.giftOrder(
                "ORD-1", "CUST-1", List.of(MUG), HOME, "Congratulations!");

        assertAll(
                () -> assertTrue(order.isGiftWrapped()),
                () -> assertEquals("Congratulations!", order.giftMessage().orElseThrow()),
                () -> assertFalse(order.isPriority()));
    }

    @Test
    @DisplayName("standardOrder switches nothing on")
    void standardOrderHasNoExtras() {
        PurchaseOrder order = PurchaseOrderPresets.standardOrder(
                "ORD-2", "CUST-1", List.of(MUG), HOME);

        assertAll(
                () -> assertFalse(order.isGiftWrapped()),
                () -> assertFalse(order.isPriority()),
                () -> assertTrue(order.notes().isEmpty()));
    }

    @Test
    @DisplayName("expressOrder is priority, with a same-day note")
    void expressOrderIsPriorityWithANote() {
        PurchaseOrder order = PurchaseOrderPresets.expressOrder(
                "ORD-3", "CUST-1", List.of(MUG), HOME);

        assertAll(
                () -> assertTrue(order.isPriority()),
                () -> assertTrue(order.notes().orElseThrow().contains("same-day")));
    }
}
