package com.jk.explore.hexagonal;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PlaceAnOrderDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    @DisplayName("the demo runs end to end and prints all five acts plus the acceptance block")
    void allFiveActsRun() {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. The naive version"), output);
        assertTrue(output.contains("TWO. The real core, driven by HTTP."), output);
        assertTrue(output.contains("THREE. The driven side swapped"), output);
        assertTrue(output.contains("FOUR. The driving side swapped"), output);
        assertTrue(output.contains("FIVE. The rule, and the bill."), output);
        assertTrue(output.contains("ACCEPTANCE"), output);
    }

    @Test
    @DisplayName("the numbers the README and narration quote are the numbers the demo prints")
    void theQuotedNumbersAreReal() {
        String output = runTheDemo();

        assertTrue(output.contains("store is now an append-only log, read backwards"), output);
        assertTrue(output.contains("PlaceOrderService.java: zero lines changed."), output);
        assertTrue(output.contains("classes in the core : 14"), output);
        assertTrue(output.contains("of those, never opened : 14"), output);
        assertTrue(output.contains(
                "order ord-1001 for cust-8801: PLACED, 3 lines, £382.50"), output);
        assertTrue(output.contains("stock ESP-001 3, GRD-014 1, BNS-220 38"), output);
        assertTrue(output.contains("charged cust-8801 £382.50 once"), output);
        assertTrue(output.contains(
                "refused: not enough stock, unknown product, payment declined"), output);
    }

    @Test
    @DisplayName("the demo is deterministic: two runs produce byte-identical output")
    void theDemoIsDeterministic() {
        assertEquals(runTheDemo(), runTheDemo());
    }
}
