package com.jk.explore.eventbusnats;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/** The six acts, run end to end, with every number the README quotes asserted exactly. */
class DemoRunsTest {

    @Test
    void allSixActsRunAndPrintTheNumbersTheDocumentsQuote() throws Exception {
        assumeTrue(NatsServer.containerRuntimeAvailable(), "needs a container runtime");
        String out = run();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("20 wires between them"), out);
        assertTrue(out.contains("add a sixth service and it needs 10 more"), out);
        assertTrue(out.contains("[email saw OrderPlaced ORD-1, warehouse saw OrderPlaced ORD-1, analytics saw OrderPlaced ORD-1]"), out);
        assertTrue(out.contains("5 wires, not 20"), out);
        assertTrue(out.contains("store.orders.placed received 1: [OrderPlaced ORD-1]"), out);
        assertTrue(out.contains("received 2: [OrderPlaced ORD-1, OrderCancelled ORD-1]"), out);
        assertTrue(out.contains("received 4: [OrderPlaced ORD-1, OrderCancelled ORD-1, PaymentTaken ORD-1, StockLow SKU-42]"), out);
        assertTrue(out.contains("recorded: [OrderPlaced ORD-1: mail server timed out]"), out);
        assertTrue(out.contains("[warehouse reserved ORD-1]"), out);
        assertTrue(out.contains("the first event the warehouse ever received was OrderPlaced ORD-2"), out);
        assertTrue(out.contains("2 orders published, 1 received"), out);
        assertTrue(out.contains("came back at once with no responders"), out);
        assertTrue(out.contains("3 listeners for store events"), out);
        assertTrue(out.contains("left its connection open: 2 listeners"), out);
        assertTrue(out.contains("closed their connections: 0 listeners"), out);
        assertTrue(out.contains("this demo needed 1 container"), out);
    }

    private static String run() throws Exception {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            EventBusNatsDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
