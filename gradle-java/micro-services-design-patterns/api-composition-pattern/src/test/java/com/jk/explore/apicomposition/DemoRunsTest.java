package com.jk.explore.apicomposition;

import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The demo is teaching material too, so it is tested like the rest of it. */
class DemoRunsTest {

    @Test
    @DisplayName("all five acts run and print what they promise")
    void itRunsEveryAct() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true));
            OrderDetailsDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }

        String output = captured.toString();
        assertTrue(output.contains("Act 1"), output);
        assertTrue(output.contains("Act 5"), output);
        assertTrue(output.contains("waited 210ms"), output);
        assertTrue(output.contains("waited 150ms"), output);
        assertTrue(output.contains("delivery status"), output);
        assertTrue(output.contains("99.700%"), output);
    }
}
