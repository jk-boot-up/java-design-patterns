package com.jk.explore.stranglerfignginx;

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
    void theSixActsRunAgainstARealNginxAndPrintTheFiguresTheDocumentsQuote() {
        assumeTrue(NginxRouter.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] expected = {
            "NGINX 1.31.6 is running in a container, in front of the old shop.",
            "the shop's four pages: prices 200, stock 200, basket 200, orders 200. pages that work: 4 of 4 (4 from the old shop, 0 from the new service).",
            "the four pages: prices 200, stock 404, basket 404, orders 404. pages that work: 1 of 4 (0 from the old shop, 1 from the new service).",
            "NGINX's main process: number 1 before the reload and number 1 after. nothing restarted.",
            "while that request is still open: workers still finishing old requests: 1. workers taking new requests: 1.",
            "a new price request: 200, from the new service.",
            "the open request then finishes: 200, from the old shop. workers still finishing old requests: 0.",
            "the four pages now: prices 200, stock 200, basket 200, orders 200. pages that work: 4 of 4 (3 from the old shop, 1 from the new service).",
            "location ~ ^/api/(prices|stock)/",
            "and a reload. 10 price requests: 10 from the old shop, 0 from the new service.",
            "written as location ^~ /api/prices/, which tells NGINX to stop looking: 10 price requests: 0 from the old shop, 10 from the new service.",
            "proxy_pass http://new_service; the new service is asked for /api/prices/SKU-1 and answers 200.",
            "proxy_pass http://new_service/; the new service is asked for /SKU-1 and answers 404.",
            "10 price requests: 10 answered 502 Bad Gateway, by NGINX itself. 10 stock requests: 10 answered 200, by the old shop.",
            "roll back: the one location removed, and a reload. 10 price requests: 10 answered 200, by the old shop.",
            "moves prices to it again: 10 price requests: 0 from the old shop, 10 from the new service.",
            "a customer puts 3 items in the basket. the old shop answers \"basket: 3 items\" and sets the cookie LEGACYSESSION=L-1.",
            "it receives the cookie LEGACYSESSION=L-1 and has no use for it: 422, your basket is empty.",
            "checkout moved back to the old shop: 200, order 1002 placed: 3 items, 4249 pence.",
            "the old shop still serves 4 of 5 routes: stock, basket, checkout and orders.",
            "1 NGINX container, the old shop and the new service",
        };
        for (String line : expected) {
            assertTrue(out.contains(line), "missing: " + line + "\n" + out);
        }
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            StranglerFigNginxDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
