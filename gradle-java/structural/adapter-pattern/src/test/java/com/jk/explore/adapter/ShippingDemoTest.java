package com.jk.explore.adapter;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class ShippingDemoTest {

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
        ShippingDemo.main(new String[0]);
        String output = captured.toString();

        assertTrue(output.contains("Acme (adapted):  $63.46"));
        assertTrue(output.contains("Flat rate (native):  $57.48"));
        assertTrue(output.contains("Quoted rate: $13.48"));
        assertTrue(output.contains("NaiveCheckoutService:    $13.48"));
        assertTrue(output.contains("NaiveShippingEstimator:  $13.48"));
    }
}
