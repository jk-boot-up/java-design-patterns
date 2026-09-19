package com.jk.explore.unitofworkspring;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() {
        System.setProperty("spring.datasource.url", "jdbc:h2:mem:demo-run;DB_CLOSE_DELAY=-1");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            OrderApplication.main(new String[0]);
        } finally {
            System.setOut(original);
            System.clearProperty("spring.datasource.url");
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("orders 1, lines 2, stock keyboard 8, mouse 9, monitor 10"), out);
        assertTrue(out.contains("after running an unrelated query:         1"), out);
    }
}
