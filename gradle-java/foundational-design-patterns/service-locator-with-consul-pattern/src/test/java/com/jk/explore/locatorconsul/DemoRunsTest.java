package com.jk.explore.locatorconsul;

import com.jk.explore.locatorconsul.consul.ConsulAgent;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() throws Exception {
        Assumptions.assumeTrue(ConsulAgent.available(), "consul is not installed");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            ConsulDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("served by gateway-1: 2, by gateway-2: 2"), out);
        assertTrue(out.contains("no healthy instance of \"notifier\""), out);
        assertTrue(out.contains("ConnectException"), out);
    }
}
