package com.jk.explore.singleton;

import static org.junit.jupiter.api.Assertions.assertAll;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("OrderSequenceGeneratorDemo — runs end to end and proves the enum singleton resists both attacks")
class OrderSequenceGeneratorDemoTest {

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
    void demoRuns() throws Exception {
        OrderSequenceGeneratorDemo.main(new String[0]);

        String out = captured.toString();

        assertAll(
                () -> assertTrue(out.contains("first == second: true"), out),
                () -> assertTrue(out.contains("Rejected: Cannot reflectively create enum objects"), out),
                () -> assertTrue(out.contains("roundTripped == INSTANCE: true"), out),
                () -> assertTrue(out.contains("legacyFirst == legacySecond: true"), out),
                () -> assertTrue(out.contains("forged == legacyFirst: false"), out),
                () -> assertTrue(out.contains("legacyRoundTripped == legacyFirst: false"), out));
    }
}
