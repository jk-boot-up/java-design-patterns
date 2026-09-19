package com.jk.explore.sidecarkubernetes;

import org.junit.jupiter.api.Test;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;

import static org.junit.jupiter.api.Assertions.assertTrue;

class DemoRunsTest {

    @Test
    void allSixActsRun() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            PodDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("Pod 2/2, proxy restarts 1, checkout restarts 0"), out);
        assertTrue(out.contains("READY 2/2"), out);
        assertTrue(out.contains("[sidecar-proxy, checkout]"), out);
    }
}
