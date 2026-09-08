package com.jk.explore.bridge;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SmsChannelTest {

    private final PrintStream originalOut = System.out;
    private final ByteArrayOutputStream captured = new ByteArrayOutputStream();
    private final SmsChannel sms = new SmsChannel();

    @BeforeEach
    void redirectOut() {
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreOut() {
        System.setOut(originalOut);
    }

    @Test
    void shortMessagesAreDeliveredUnchanged() {
        sms.deliver("+1-555-0142", "Hi", "short body");

        String line = captured.toString();
        assertTrue(line.contains("Hi: short body"));
        assertFalse(line.contains("…"));
    }

    @Test
    void longMessagesAreTruncatedWithAnEllipsis() {
        String longBody = "x".repeat(200);
        sms.deliver("+1-555-0142", "Subject", longBody);

        String line = captured.toString();
        assertTrue(line.contains("…"));

        String withoutPrefixAndNewline = line.substring(line.indexOf("] ") + 2).trim();
        assertTrue(withoutPrefixAndNewline.length() <= SmsChannel.MAX_LENGTH);
    }
}
