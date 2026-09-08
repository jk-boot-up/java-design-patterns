package com.jk.explore.bridge;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.math.BigDecimal;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * Confirms the naive classes produce the exact same output as the bridge
 * equivalents -- the naive approach is not wrong, it is just duplicated.
 */
class NaiveNotificationsTest {

    private final PrintStream originalOut = System.out;
    private final ByteArrayOutputStream captured = new ByteArrayOutputStream();

    @BeforeEach
    void redirectOut() {
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreOut() {
        System.setOut(originalOut);
    }

    @Test
    void naiveOrderConfirmationEmailMatchesTheBridgeEquivalent() {
        new NaiveOrderConfirmationEmail("ORD-1042", new BigDecimal("129.99")).send("alex@example.com");
        String naive = captured.toString();
        captured.reset();

        new OrderConfirmationNotification(new EmailChannel(), "ORD-1042", new BigDecimal("129.99"))
                .send("alex@example.com");
        String bridge = captured.toString();

        assertEquals(naive, bridge);
    }

    @Test
    void naiveShippingUpdateSmsMatchesTheBridgeEquivalent() {
        new NaiveShippingUpdateSms("ORD-1042", "out for delivery").send("+1-555-0142");
        String naive = captured.toString();
        captured.reset();

        new ShippingUpdateNotification(new SmsChannel(), "ORD-1042", "out for delivery").send("+1-555-0142");
        String bridge = captured.toString();

        assertEquals(naive, bridge);
    }
}
