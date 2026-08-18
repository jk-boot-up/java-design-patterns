package com.jk.explore.facade;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

class OrderFacadeTest {

    private final ByteArrayOutputStream outContent = new ByteArrayOutputStream();
    private final PrintStream originalOut = System.out;

    @BeforeEach
    void setUp() {
        System.setOut(new PrintStream(outContent));
    }

    @AfterEach
    void tearDown() {
        System.setOut(originalOut);
    }

    @Test
    void placeOrderCoordinatesSubsystemsInOrder() {
        OrderRequest request = new OrderRequest("CUST-001", "SKU-1234", 2, 49.98, "221B Baker Street, London");

        OrderConfirmation confirmation = new OrderFacade().placeOrder(request);

        assertNotNull(confirmation.orderId());
        assertNotNull(confirmation.paymentId());
        assertNotNull(confirmation.trackingId());

        String output = outContent.toString();
        int inventoryIndex = output.indexOf("Inventory: reserving");
        int paymentIndex = output.indexOf("Payment: charged");
        int shippingIndex = output.indexOf("Shipping: scheduled shipment");
        int notificationIndex = output.indexOf("Notification: emailed customer");

        assertTrue(inventoryIndex >= 0 && inventoryIndex < paymentIndex, "stock should be reserved before payment");
        assertTrue(paymentIndex < shippingIndex, "payment should be charged before shipment is scheduled");
        assertTrue(shippingIndex < notificationIndex, "shipment should be scheduled before confirmation is sent");
    }
}
