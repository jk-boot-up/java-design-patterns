package com.jk.explore.cleanspring;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The demo is what the video shows and what the README quotes, so its
 * output is pinned here — including the one line unique to this project:
 * the container failing at startup, with the missing type named.
 */
class DemoRunsTest {

    private String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            Application.main(new String[]{"--spring.main.banner-mode=off",
                    "--logging.level.root=WARN"});
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }

    @Test
    void allFiveActsRunAndTheContrastIsReal() {
        String output = runTheDemo();

        assertTrue(output.contains("ONE. The naive version"), output);
        assertTrue(output.contains("TWO. The graph, wired by Spring instead of by hand."), output);
        assertTrue(output.contains("THREE. Recognition: @Bean is those twenty lines."), output);
        assertTrue(output.contains("FOUR. The forced change still costs nothing extra."), output);
        assertTrue(output.contains("FIVE. Hand-wiring fails at compile time."), output);
        assertTrue(output.contains("STARTUP FAILED"), output);
        assertTrue(output.contains("NotificationGateway"), output);
        assertTrue(output.contains("ACCEPTANCE"), output);
        assertTrue(output.contains(
                "order ord-1001 for cust-8801: PLACED, 3 lines, £382.50"), output);
        assertTrue(output.contains("stock ESP-001 3, GRD-014 1, BNS-220 38"), output);
        assertTrue(output.contains("charged cust-8801 £382.50 once"), output);
        assertTrue(output.contains(
                "refused: not enough stock, unknown product, payment declined"), output);
    }
}
