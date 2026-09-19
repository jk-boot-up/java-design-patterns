package com.jk.explore.unitofwork;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            OrderDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("order lines in the database: 2 of 3"), out);
        assertTrue(out.contains("0 database operations, 7 changes registered"), out);
        assertTrue(out.contains("locked for 7 ticks, not 22"), out);
        assertTrue(out.contains("orders: 0, lines: 0, stock: keyboard 10, mouse 10, monitor 10"), out);
    }
}
