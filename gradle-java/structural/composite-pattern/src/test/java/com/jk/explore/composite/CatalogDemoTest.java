package com.jk.explore.composite;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class CatalogDemoTest {

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
        CatalogDemo.main(new String[0]);
        String output = captured.toString();

        assertTrue(output.contains("+ Electronics/"));
        assertTrue(output.contains("- Phone ($599.99)"));
        assertTrue(output.contains("+ Cables/"));
        assertTrue(output.contains("- USB-C Cable ($9.99)"));
        assertTrue(output.contains("Total price:  $659.96"));
        assertTrue(output.contains("Product count: 4"));
        assertTrue(output.contains("Phone -> $599.99 across 1 product(s)"));
        assertTrue(output.contains("Accessories -> $59.97 across 3 product(s)"));
    }
}
