package com.jk.explore.bgk8s;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

class BlueGreenK8sTest {

    @Test
    void outcomeCountsByVersion() {
        Traffic.Outcome o = new Traffic.Outcome(java.util.Map.of("v1", 3), 2);
        assertEquals(3, o.from("v1"));
        assertEquals(0, o.from("v2"));
        assertEquals(2, o.failed());
    }

    @Test
    void theSixActsRunAgainstARealCluster() throws Exception {
        assumeTrue(Cluster.toolsAvailable(), "needs Docker, kind and kubectl");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            BlueGreenK8sDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("failed 20 of 20"), out);
        assertTrue(out.contains("failed 0."), out);
        assertTrue(out.contains("a small share, as a canary should be"), out);
        assertTrue(out.contains("buggy v2: halted true"), out);
        assertTrue(out.contains("4 pods"), out);
    }
}
