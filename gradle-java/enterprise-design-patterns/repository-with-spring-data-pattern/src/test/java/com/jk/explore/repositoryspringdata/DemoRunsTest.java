package com.jk.explore.repositoryspringdata;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() {
        System.setProperty("spring.datasource.url", "jdbc:h2:mem:sd-demo;DB_CLOSE_DELAY=-1");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            CustomerApplication.main(new String[0]);
        } finally {
            System.setOut(original);
            System.clearProperty("spring.datasource.url");
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("[Ada, Grace]"), out);
        assertTrue(out.contains("7 orders, 7 statements"), out);
        assertTrue(out.contains("Ada's city in the database now: Manchester"), out);
    }
}
