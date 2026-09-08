package com.jk.explore.builder;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("PurchaseOrderDemo — runs end to end and rejects the incomplete orders")
class PurchaseOrderDemoTest {

    private final PrintStream realOut = System.out;
    private ByteArrayOutputStream captured;

    @BeforeEach
    void captureStdout() {
        captured = new ByteArrayOutputStream();
        System.setOut(new PrintStream(captured));
    }

    @AfterEach
    void restoreStdout() {
        System.setOut(realOut);
    }

    @Test
    void demoRuns() {
        PurchaseOrderDemo.main(new String[0]);

        String out = captured.toString();

        assertAll(
                () -> assertTrue(out.contains("giftWrapped=true"), out),
                () -> assertTrue(out.contains("first items: 1, second items: 2"), out),
                () -> assertTrue(out.contains("Rejected: a purchase order needs at least one item"), out),
                () -> assertTrue(out.contains("Rejected: a purchase order needs a shipping address"), out));
    }
}
