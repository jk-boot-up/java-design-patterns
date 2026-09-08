package com.jk.explore.bridge;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class EmailChannelTest {

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
    void deliversTheFullSubjectAndBodyUnchanged() {
        String longBody = "x".repeat(500);
        new EmailChannel().deliver("alex@example.com", "Subject", longBody);

        String line = captured.toString();
        assertTrue(line.contains("Subject -- " + longBody));
    }
}
