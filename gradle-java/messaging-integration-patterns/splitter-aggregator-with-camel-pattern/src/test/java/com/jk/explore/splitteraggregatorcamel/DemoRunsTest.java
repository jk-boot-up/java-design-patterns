package com.jk.explore.splitteraggregatorcamel;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertTrue;

/** The six acts run, and print the figures every document in this project quotes. */
class DemoRunsTest {

    @Test
    void allSixActsRunAndPrintTheirFigures() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            CamelSplitterAggregatorDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("3 steps of work on 1 thread"), out);
        assertTrue(out.contains("the basket comes to £283.42"), out);
        assertTrue(out.contains("ORD-4471 shipment 2 of 3 to Reading: 1 x ESP-001, £249.99"), out);
        assertTrue(out.contains("completed by: size. 3 of 3 shipments"), out);
        assertTrue(out.contains("total £283.42"), out);
        assertTrue(out.contains("answers out of the aggregator: 0. orders still open: 1."), out);
        assertTrue(out.contains("a deadline of 600 milliseconds, looked at every 100"), out);
        assertTrue(out.contains("completed by: timeout. 2 of 3 shipments, missing [Glasgow]"), out);
        assertTrue(out.contains("gathered so far £265.97"), out);
        assertTrue(out.contains("1000 orders held in the aggregator's memory"), out);
        assertTrue(out.contains("at 2 of 3 lines, with 1 duplicate noted"), out);
        assertTrue(out.contains("£265.97 with the check, £515.96 without it"), out);
    }
}
