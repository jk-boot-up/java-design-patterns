package com.jk.explore.messagechannelrabbitmq;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every number quoted in the README, in the slides and in the
 * narration is asserted here, so a change to the code that changes a figure fails the build
 * instead of quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstARealBrokerAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(Broker.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("orders placed: 3. checkouts that failed: 3."), out);
        assertTrue(out.contains("takes them, each once: [ORD-1, ORD-2, ORD-3]. left waiting: 0."), out);
        assertTrue(out.contains("checkout sends 3, and none fail. the broker is holding: 3."), out);
        assertTrue(out.contains("works through them, in order: [ORD-1, ORD-2, ORD-3]."), out);
        assertTrue(out.contains("the broker puts it back. waiting again: 1."), out);
        assertTrue(out.contains("marked as seen before: true"), out);
        assertTrue(out.contains("deliveries: 2, orders picked: 1, waiting: 0."), out);
        assertTrue(out.contains("two pickers share one channel, one slow and one fast. checkout sends 10 orders."), out);
        assertTrue(out.contains("in turn: slow picker 5, fast picker 5."), out);
        assertTrue(out.contains("before handing it another: the fast picker took most of them."), out);
        assertTrue(out.contains("two channels hold 3 orders each."), out);
        assertTrue(out.contains("written to disk: 3 orders still waiting. held in memory only: 0."), out);
        assertTrue(out.contains("a channel with room for 5 is given 8: 5 accepted, 3 refused."), out);
        assertTrue(out.contains("1 container for 1 shop and 1 warehouse."), out);
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            RabbitMessageChannelDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
