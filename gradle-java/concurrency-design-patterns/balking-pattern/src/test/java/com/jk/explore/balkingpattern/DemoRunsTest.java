package com.jk.explore.balkingpattern;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() throws Exception {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            BalkingDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("their click did nothing"), out);
    }
}
