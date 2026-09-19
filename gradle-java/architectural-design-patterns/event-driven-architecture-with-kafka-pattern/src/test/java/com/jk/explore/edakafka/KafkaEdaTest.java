package com.jk.explore.edakafka;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import org.junit.jupiter.api.Test;

class KafkaEdaTest {

    @Test
    void directShopLosesTheOrderWhenShippingIsDown() {
        assertFalse(new DirectShop(false).place("ORD-1"));
    }

    @Test
    void theWarehouseCountsOnlyPlacedOrders() {
        Warehouse w = new Warehouse(10);
        w.reserve("OrderPlaced ORD-1");
        w.reserve("something else");
        assertEquals(9, w.stock());
    }

    @Test
    void theSixActsRunAgainstARealKafka() throws Exception {
        assumeTrue(Broker.toolsAvailable(), "needs Docker and the Kafka image");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            KafkaEdaDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("which gave it offset 0"), out);
        assertTrue(out.contains("shipping is 3 events behind"), out);
        assertTrue(out.contains("planned 4 orders, and is 0 behind"), out);
        assertTrue(out.contains("[OrderPlaced ORD-1, OrderPlaced ORD-2]"), out);
        assertTrue(out.contains("stock in the warehouse: 10. it should be 9."), out);
        assertTrue(out.contains("without a duplicate check 8, with one 9"), out);
    }
}
