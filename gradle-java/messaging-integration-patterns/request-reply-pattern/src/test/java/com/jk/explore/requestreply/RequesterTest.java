package com.jk.explore.requestreply;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class RequesterTest {

    @Test
    void repliesAreMatchedByCorrelationId() throws Exception {
        try (InventoryService inv = new InventoryService(); Requester r = new Requester("T", inv.requests())) {
            Requester.Sent slow = r.send("reserve KETTLE-1 x 5");
            Requester.Sent fast = r.send("reserve MUG-1 x 2");
            assertEquals("RESERVED 2 x MUG-1", fast.await(2000));
            assertEquals("REFUSED 5 x KETTLE-1", slow.await(2000));
            assertEquals(0, r.pending());
        }
    }

    @Test
    void eachRequesterGetsOnlyItsOwnReplies() throws Exception {
        try (InventoryService inv = new InventoryService();
             Requester a = new Requester("A", inv.requests());
             Requester b = new Requester("B", inv.requests())) {
            assertEquals("RESERVED 1 x TEAPOT-1", a.send("reserve TEAPOT-1 x 1").await(2000));
            assertEquals("RESERVED 1 x MUG-1", b.send("reserve MUG-1 x 1").await(2000));
        }
    }

    @Test
    void inOrderMatchingGetsItWrong() throws Exception {
        try (InventoryService inv = new InventoryService()) {
            List<String> m = InOrderRequester.ask(inv.requests(), List.of("reserve KETTLE-1 x 5", "reserve MUG-1 x 2"));
            assertTrue(m.get(0).endsWith("RESERVED 2 x MUG-1"));
        }
    }

    @Test
    void lostReplyTimesOut() throws Exception {
        try (InventoryService inv = new InventoryService(); Requester r = new Requester("T", inv.requests())) {
            inv.loseNextReply();
            assertEquals("no reply after 300 ms", r.send("reserve MUG-1 x 1").await(300));
            assertEquals(1, r.pending());
        }
    }
}
