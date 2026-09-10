package com.jk.explore.facade;

import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * Tests for the facade itself: the sequence it enforces, the plumbing it does
 * between the four subsystems, and the confirmation it hands back.
 */
class OrderFacadeTest {

    private static final OrderRequest REQUEST =
            new OrderRequest("CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

    @Test
    void callsTheFourSubsystemsInTheDocumentedOrder() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        subsystems.facade().placeOrder(REQUEST);

        assertEquals(
                List.of("reserveStock", "charge", "scheduleShipment", "sendOrderConfirmation"),
                stepNames(subsystems.calls),
                "the facade exists to hold this order in one place");
    }

    @Test
    void reservesStockBeforeChargingTheCard() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        subsystems.facade().placeOrder(REQUEST);

        List<String> steps = stepNames(subsystems.calls);
        assertTrue(steps.indexOf("reserveStock") < steps.indexOf("charge"),
                "charging before stock is confirmed is the bug the facade prevents");
    }

    @Test
    void callsEachSubsystemExactlyOnce() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        subsystems.facade().placeOrder(REQUEST);

        assertEquals(4, subsystems.calls.size());
        assertEquals(4, stepNames(subsystems.calls).stream().distinct().count());
    }

    @Test
    void passesTheRequestThroughUnchanged() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        subsystems.facade().placeOrder(REQUEST);

        assertEquals("reserveStock:SKU-1234:2", subsystems.calls.get(0));
        assertEquals("charge:CUST-001:49.98", subsystems.calls.get(1));
        assertTrue(subsystems.calls.get(2).endsWith(":221B Baker Street, London"));
    }

    @Test
    void addsNoBusinessRulesOfItsOwn() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        // Two units at 49.98 is a total the facade must not recompute, discount,
        // round or tax. A facade that grows arithmetic has stopped being one.
        subsystems.facade().placeOrder(REQUEST);

        assertEquals("charge:CUST-001:49.98", subsystems.calls.get(1),
                "the facade must charge exactly the amount it was given");
    }

    @Test
    void feedsTheShipmentsTrackingIdIntoTheNotification() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        OrderConfirmation confirmation = subsystems.facade().placeOrder(REQUEST);

        assertEquals("sendOrderConfirmation:CUST-001:" + confirmation.orderId() + ":TRK-TEST",
                subsystems.calls.get(3),
                "moving one subsystem's output into the next one's input is the plumbing "
                        + "every caller would otherwise repeat");
    }

    @Test
    void returnsTheIdentifiersMintedByTheSubsystems() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        OrderConfirmation confirmation = subsystems.facade().placeOrder(REQUEST);

        assertEquals("PMT-TEST", confirmation.paymentId());
        assertEquals("TRK-TEST", confirmation.trackingId());
        assertTrue(confirmation.orderId().startsWith("ORD-"),
                "the order id is the one thing the facade mints itself");
    }

    @Test
    void mintsADifferentOrderIdForEveryOrder() {
        OrderFacade facade = new RecordingSubsystems().facade();

        assertNotEquals(facade.placeOrder(REQUEST).orderId(), facade.placeOrder(REQUEST).orderId());
    }

    @Test
    void usesTheSameOrderIdForTheShipmentAndTheConfirmation() {
        RecordingSubsystems subsystems = new RecordingSubsystems();

        OrderConfirmation confirmation = subsystems.facade().placeOrder(REQUEST);

        assertTrue(subsystems.calls.get(2).startsWith("scheduleShipment:" + confirmation.orderId() + ":"));
        assertTrue(subsystems.calls.get(3).contains(":" + confirmation.orderId() + ":"));
    }

    @Test
    void refusesTheOrderWhenStockCannotBeReserved() {
        RecordingSubsystems subsystems = new RecordingSubsystems(false);

        IllegalStateException failure =
                assertThrows(IllegalStateException.class, () -> subsystems.facade().placeOrder(REQUEST));

        assertTrue(failure.getMessage().contains("SKU-1234"),
                "the message should name the product that could not be reserved");
    }

    @Test
    void chargesNothingAndShipsNothingWhenStockCannotBeReserved() {
        RecordingSubsystems subsystems = new RecordingSubsystems(false);

        assertThrows(IllegalStateException.class, () -> subsystems.facade().placeOrder(REQUEST));

        assertEquals(List.of("reserveStock"), stepNames(subsystems.calls),
                "a customer whose item is gone must not be charged, shipped to or emailed");
    }

    @Test
    void theNoArgumentConstructorWiresUpTheRealSubsystems() {
        // The constructor the demo and every caller uses. It has to work without
        // anybody assembling four services by hand.
        OrderConfirmation confirmation = new OrderFacade().placeOrder(REQUEST);

        assertTrue(confirmation.orderId().startsWith("ORD-"));
        assertTrue(confirmation.paymentId().startsWith("PMT-"));
        assertTrue(confirmation.trackingId().startsWith("TRK-"));
    }

    /** "reserveStock:SKU-1234:2" -> "reserveStock". */
    private static List<String> stepNames(List<String> calls) {
        return calls.stream().map(call -> call.substring(0, call.indexOf(':'))).toList();
    }
}
