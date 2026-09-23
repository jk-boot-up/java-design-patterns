package com.jk.explore.camelrouter;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/** The whole demo, run once, with every figure the documents quote checked against what it printed. */
class DemoRunsTest {

    @Test
    void allSixActsRunAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(Broker.dockerAvailable(), "needs a container runtime");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            CamelRouterDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("it shipped 3 and could do nothing with 3"), out);
        assertTrue(out.contains("ORD-1 (physical, express, UK, 49.99) -> express-shipping"), out);
        assertTrue(out.contains("ORD-5 (subscription, none, UK, 9.99) -> manual-review"), out);
        assertTrue(out.contains("{express-shipping=[ORD-1], standard-shipping=[ORD-6], digital-delivery=[ORD-2, ORD-4], "
                + "fraud-review=[ORD-3], manual-review=[ORD-5]}"), out);
        assertTrue(out.contains("asks 4 questions"), out);
        assertTrue(out.contains("asked first: fraud-review. with it asked last: digital-delivery"), out);
        assertTrue(out.contains("messages left anywhere in the shop: 0"), out);
        assertTrue(out.contains("names the problem sends it to: unclaimed"), out);
        assertTrue(out.contains("questions before: 4, after: 5"), out);
        assertTrue(out.contains("it now goes to: eu-vat-check"), out);
        assertTrue(out.contains("still goes to: standard-shipping"), out);
        assertTrue(out.contains("ORD-9 lands on: manual-review"), out);
        assertTrue(out.contains("Camel tried it 3 times"), out);
        assertTrue(out.contains("router-errors, which now holds 1"), out);
        assertTrue(out.contains("1 container, 1 exchange and 10 queues"), out);
    }
}
