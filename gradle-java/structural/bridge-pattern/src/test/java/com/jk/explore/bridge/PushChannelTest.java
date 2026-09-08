package com.jk.explore.bridge;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

class PushChannelTest {

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
    void deliversOnlyTheSubjectNeverTheBody() {
        new PushChannel().deliver("device-1", "Title", "this body must not appear");

        String line = captured.toString();
        assertTrue(line.contains("Title"));
        assertFalse(line.contains("this body must not appear"));
    }
}
