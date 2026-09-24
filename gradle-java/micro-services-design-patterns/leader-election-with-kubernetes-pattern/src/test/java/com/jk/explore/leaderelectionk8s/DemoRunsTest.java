package com.jk.explore.leaderelectionk8s;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every figure the README, the slides and the narration quote is
 * asserted here, so a change that alters one fails the build instead of making the documents wrong.
 * The demo makes its own cluster and deletes it before it returns.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealApiServerAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(Cluster.containerRuntimeAvailable() && Cluster.kindAvailable(), "needs a container runtime and kind");
        String out = runTheDemo();
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("run as 3 separate processes"), out);
        assertTrue(out.contains("sent by every copy: [A, B, C]."), out);
        assertTrue(out.contains("the manager receives it 3 times."), out);
        assertTrue(out.contains("holder A, lasts 5 seconds, holder changes 0."), out);
        assertTrue(out.contains("each is told the leader is A."), out);
        assertTrue(out.contains("the report was sent by: [A]."), out);
        assertTrue(out.contains("the second refused with 409 Conflict."), out);
        assertTrue(out.contains("took over within a couple of seconds, well inside one 5-second lease."), out);
        assertTrue(out.contains("took over after about one whole 5-second lease."), out);
        assertTrue(out.contains("the lease says: holder B, holder changes 1."), out);
        assertTrue(out.contains("the report was sent by: [B, A]."), out);
        assertTrue(out.contains("when A sent, the lease named B, renewed after A's last renewal: yes."), out);
        assertTrue(out.contains("A's token is 0, B's is 1."), out);
        assertTrue(out.contains("refused, token 0 is older than 1."), out);
        assertTrue(out.contains("the report was sent by: [B]."), out);
        assertTrue(out.contains("the lease still names B, and nobody leads."), out);
        assertTrue(out.contains("leads again with token 2."), out);
        assertTrue(out.contains("1 cluster, with 1 node, for 1 nightly report."), out);
        assertTrue(!Shell.run("kind", "get", "clusters").contains(Cluster.NAME), "the demo deletes its cluster");
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            KubernetesLeaderElectionDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
