package com.jk.explore.databaseperservice;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The demo is part of the teaching material, so it is tested like the rest of it. */
class DemoRunsTest {

    @Test
    @DisplayName("all five acts run and print what they promise")
    void itRunsEveryAct() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true));
            DatabasePerServiceDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }

        String output = captured.toString();
        assertTrue(output.contains("Act 1"), output);
        assertTrue(output.contains("Act 5"), output);
        assertTrue(output.contains("somebody renamed it"), output);
        assertTrue(output.contains("may not read"), output);
        assertTrue(output.contains(CatalogService.UNKNOWN_PRODUCT), output);
    }
}
