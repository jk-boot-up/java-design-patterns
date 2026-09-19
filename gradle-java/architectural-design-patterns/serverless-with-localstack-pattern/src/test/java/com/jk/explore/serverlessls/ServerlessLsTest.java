package com.jk.explore.serverlessls;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.zip.ZipInputStream;
import org.junit.jupiter.api.Test;

class ServerlessLsTest {

    @Test
    void theHandlerIsZippedForUpload() throws Exception {
        byte[] zip = Platform.zipOf("handler.py", Platform.handlerSource());
        try (ZipInputStream in = new ZipInputStream(new java.io.ByteArrayInputStream(zip))) {
            assertEquals("handler.py", in.getNextEntry().getName());
        }
    }

    @Test
    void aCallReadsItsFieldsFromTheAnswer() {
        Platform.Call c = new Platform.Call("{\"receipt\": \"sent for ORD-1\", \"instance\": \"ab12\", \"callsOnThisInstance\": 2}", false, 5);
        assertEquals("ab12", c.field("instance"));
        assertEquals("2", c.field("callsOnThisInstance"));
    }

    @Test
    void theSixActsRunAgainstARealLambdaApi() throws Exception {
        assumeTrue(Platform.toolsAvailable(), "needs Docker, LocalStack and the Lambda image");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            ServerlessLsDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("receipts sent: 3."), out);
        assertTrue(out.contains("before any order, copies running: 0."), out);
        assertTrue(out.contains("distinct copies that answered 5"), out);
        assertTrue(out.contains("quiet seconds later, with no orders: copies running 0."), out);
        assertTrue(out.contains("the cold call was slower: true"), out);
        assertTrue(out.contains("it has handled 1 calls. a different copy answered: true"), out);
        assertTrue(out.contains("Task timed out after 3.00 seconds"), out);
    }
}
