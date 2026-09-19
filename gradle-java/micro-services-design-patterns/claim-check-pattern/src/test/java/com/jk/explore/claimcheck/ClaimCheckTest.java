package com.jk.explore.claimcheck;

import org.junit.jupiter.api.Test;

import java.util.Arrays;

import static com.jk.explore.claimcheck.ClaimCheckDemo.invoicePdf;
import static org.junit.jupiter.api.Assertions.*;

class ClaimCheckTest {

    @Test
    void aBigMessageIsRefusedByTheBroker() {
        assertThrows(MessageTooLarge.class, () -> new Broker(1000).publish(new Broker.Message("x", invoicePdf(5000))));
    }

    @Test
    void theClaimGoesThroughAndTheReceiverGetsTheSameBytes() {
        Broker b = new Broker(1000);
        BlobStore s = new BlobStore(new Clock(), 60);
        new Sender(b, s).send("invoice", invoicePdf(5000));
        assertTrue(Arrays.equals(invoicePdf(5000), new Receiver(b, s).receive()));
        assertEquals(0, s.stored());
    }

    @Test
    void theBrokerCarriesOnlyTheSmallTicket() {
        Broker b = new Broker(1000);
        BlobStore s = new BlobStore(new Clock(), 60);
        for (int i = 0; i < 100; i++) new Sender(b, s).send("invoice", invoicePdf(5000));
        assertTrue(b.bytesCarried() < 100 * 100);
        assertEquals(100, s.stored());
    }

    @Test
    void anUncollectedBlobIsSweptAfterItsTimeAndAClaimAfterThatIsRefused() {
        Clock c = new Clock();
        Broker b = new Broker(1000);
        BlobStore s = new BlobStore(c, 60);
        new Sender(b, s).send("a", invoicePdf(10));
        c.advance(60);
        assertThrows(BlobStore.ClaimExpired.class, () -> new Receiver(b, s).receive());
        assertEquals(1, s.deleteExpired());
        assertEquals(0, s.stored());
    }

    @Test
    void aTamperedBlobIsRefusedByItsChecksum() {
        Broker b = new Broker(1000);
        BlobStore s = new BlobStore(new Clock(), 60);
        Claim claim = new Sender(b, s).send("a", invoicePdf(100));
        s.tamper(claim.blobId());
        assertThrows(IllegalStateException.class, () -> new Receiver(b, s).receive());
    }

    @Test
    void aClaimRoundTripsThroughBytes() {
        Claim c = new Claim("blob-1", 5000, Claim.checksum(invoicePdf(5000)));
        assertEquals(c, Claim.fromBytes(c.toBytes()));
    }

    @Test
    void sequentialClaimsAreGuessableAndRandomOnesAreNot() {
        BlobStore counting = new BlobStore(new Clock(), 60, BlobStore.sequential());
        counting.put("a".getBytes());
        counting.put("b".getBytes());
        assertEquals("b", new String(counting.get("blob-2")));
        BlobStore random = new BlobStore(new Clock(), 60);
        String id = random.put("a".getBytes());
        assertTrue(id.length() > 30);
        assertThrows(BlobStore.ClaimExpired.class, () -> random.get("blob-1"));
    }

    @Test
    void oneInvoiceCostsThreeStorageOperations() {
        Broker b = new Broker(1000);
        BlobStore s = new BlobStore(new Clock(), 60);
        new Sender(b, s).send("a", invoicePdf(100));
        new Receiver(b, s).receive();
        assertEquals(3, s.operations());
    }
}
