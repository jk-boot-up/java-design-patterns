package com.jk.explore.competingconsumersrabbitmq;

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
        assertTrue(out.contains("12 orders, one picker taking one at a time. being picked: 1. waiting: 11."), out);
        assertTrue(out.contains("three pickers on the same queue. being picked: 3. waiting: 9."), out);
        assertTrue(out.contains("300 orders, three pickers: 300 picked, 300 different orders. every picker did some, and none did more than half."), out);
        assertTrue(out.contains("with no limit set. handed to it: 12. waiting: 0."), out);
        assertTrue(out.contains("handed to it: 0. it stands idle while the slow one holds 12."), out);
        assertTrue(out.contains("picked by the slow picker: 12. by the fast one: 0."), out);
        assertTrue(out.contains("20 orders, prefetch 10. handed to the slow picker: 10. to the fast one: 10."), out);
        assertTrue(out.contains("the fast one picks its 10 and stands idle. waiting: 0. still held by the slow one: 10."), out);
        assertTrue(out.contains("the same 20, prefetch 1. the slow picker holds 1. the fast one picks the other 19."), out);
        assertTrue(out.contains("picker A is handed 5, picks ORD-1 and ORD-2, reserves the stock for ORD-3"), out);
        assertTrue(out.contains("was not told was done. waiting again: 3."), out);
        assertTrue(out.contains("marked as seen before: 3 of 3. only ORD-3 had been started."), out);
        assertTrue(out.contains("deliveries: 8 for 5 orders. stock reserved for ORD-3: 2 times. for ORD-4: 1."), out);
        assertTrue(out.contains("count each order as done on handover. handed: 5. waiting: 0."), out);
        assertTrue(out.contains("picked: 2. waiting again: 0. lost: 3."), out);
        assertTrue(out.contains("3 pickers, delivered 3 times, marked seen before on 2, picked 0 times. waiting again: 1."), out);
        assertTrue(out.contains("act four made 8 deliveries for 5 orders, and reserved the stock for ORD-3 2 times."), out);
        assertTrue(out.contains("left unset, one picker took 12 of 12 while another stood idle."), out);
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            RabbitCompetingConsumersDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
