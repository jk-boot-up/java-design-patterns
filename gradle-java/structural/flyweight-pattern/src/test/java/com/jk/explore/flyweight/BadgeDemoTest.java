package com.jk.explore.flyweight;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import static org.junit.jupiter.api.Assertions.assertTrue;

class BadgeDemoTest {

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
    void demoRuns() {
        BadgeDemo.main(new String[0]);

        String output = outContent.toString();

        assertTrue(output.contains("== Rendering badges for five listings =="));
        assertTrue(output.contains("[SALE] ★ FLASH SALE on LST-1003"));
        assertTrue(output.contains("styleFor(SALE) == styleFor(SALE): true"));
        assertTrue(output.contains("sample.get(1).style() == sample.get(2).style(): true"));
        assertTrue(output.contains("naiveA == naiveB (both SALE): false"));
        assertTrue(output.contains("== Memory arithmetic for a 100000-listing catalog =="));
    }
}
