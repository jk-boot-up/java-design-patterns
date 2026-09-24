package com.jk.explore.databaseperservicecontainers;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

/**
 * The demo is the document. Every figure quoted in the README, in the slides and in the
 * narration is asserted here, so a change to the code that changes a figure fails the build
 * instead of quietly making the documents wrong.
 */
class DemoRunsTest {

    @Test
    void theSixActsRunAgainstRealPostgresAndMongoDbAndPrintWhatTheDocumentsQuote() {
        assumeTrue(Engines.containerRuntimeAvailable(), "needs a container runtime");
        String out = runTheDemo();

        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        String[] quoted = {
            "ord-101   SKU-KETTLE   Stainless Steel Kettle       x1",
            "ord-102   SKU-MUG      Blue Stoneware Mug           x4",
            "round trips to a database: 1",
            "ERROR 23503: update or delete on table \"products\" violates foreign key constraint \"orders_sku_fkey\" on table \"orders\"",
            "ERROR 42703: column p.product_name does not exist",
            "Orders owns the orders database on Postgres 18.6: 1 table.",
            "Catalog owns the catalog database on MongoDB 8.3.11: 1 collection of documents.",
            "SKU-KETTLE: _id, name, priceInPence, stock, wattage",
            "SKU-MUG: _id, name, priceInPence, stock, capacityMl",
            "round trips to a database: 2",
            "MongoDB changed 2 documents.",
            "ERROR 42P01: relation \"products\" does not exist",
            "ERROR 0A000: cross-database references are not implemented: \"shop.public.products\"",
            "no error. 2 products came back: SKU-KETTLE with 0 orders, SKU-MUG with 0 orders.",
            "Catalog deletes SKU-KETTLE: MongoDB deleted 1 document. nothing refused.",
            "Postgres still holds 1 order naming SKU-KETTLE.",
            "ord-101   SKU-KETTLE   (no longer in the catalogue) x1",
            "Postgres: ord-103 is gone. orders for cust-7: 2.",
            "MongoDB: SKU-MUG stock 38, was 40. the rollback reached one engine, not both.",
            "ord-101   SKU-KETTLE   (catalog unreachable)        x1",
            "this demo runs 2 containers, 2 drivers and 2 query languages",
        };
        for (String line : quoted) {
            assertTrue(out.contains(line), "missing: " + line + "\n" + out);
        }
    }

    private static String runTheDemo() {
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            DatabasePerServiceWithContainersDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        return captured.toString(StandardCharsets.UTF_8);
    }
}
