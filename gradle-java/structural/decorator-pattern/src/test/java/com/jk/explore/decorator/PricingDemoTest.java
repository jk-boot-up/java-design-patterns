package com.jk.explore.decorator;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class PricingDemoTest {

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
        PricingDemo.main(new String[0]);
        String output = captured.toString();

        assertTrue(output.contains("Wireless Headphones: $79.99"));
        assertTrue(output.contains("Wireless Headphones, gift-wrapped: $83.49"));
        assertTrue(output.contains("Wireless Headphones, gift-wrapped, insured: $85.16"));
        assertTrue(output.contains("Wireless Headphones, gift-wrapped, insured, express handling: $95.15"));
        assertTrue(output.contains("Wireless Headphones, insured, gift-wrapped: $85.09"));
    }
}
