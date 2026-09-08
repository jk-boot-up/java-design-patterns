package com.jk.explore.bridge;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class NotificationDemoTest {

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
    void demoRuns() {
        NotificationDemo.main(new String[0]);
        String output = captured.toString();

        assertTrue(output.contains(
                "[EMAIL to alex@example.com] Order ORD-1042 confirmed -- Your order ORD-1042 totalling $129.99 has been confirmed."));
        assertTrue(output.contains(
                "[SMS to +1-555-0142] Order ORD-1042 confirmed: Your order ORD-1042 totalling $129.99 has been confirmed."));
        assertTrue(output.contains("[PUSH to device-9f31] Order ORD-1042 confirmed"));
        assertTrue(output.contains("[EMAIL to alex@example.com] Password reset requested -- Use code 384920"));
        assertTrue(output.contains("…"));
        assertTrue(output.contains(
                "Four classes just for two notification types across two channels --"));
    }
}
