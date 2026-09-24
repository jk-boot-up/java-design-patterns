package com.jk.explore.claimchecks3;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import org.junit.jupiter.api.Test;

/** The parts that need no container: the ticket, the invoice bytes, and the base64 arithmetic. */
class PlainPartsTest {

    @Test
    void aTicketSurvivesTheTripAsText() {
        Claim claim = new Claim("invoice-pdfs", "7c1f0e2a-3b4d-4e5f-8a9b-0c1d2e3f4a5b", null, 1_500_000, "bb8711d26a6daf29");
        Claim back = Claim.read(claim.toText());
        assertEquals(claim, back);
        assertNull(back.versionId());
        assertEquals(113, claim.bytesOnTheQueue());
    }

    @Test
    void aTicketCanNameOneVersion() {
        Claim claim = new Claim("invoice-pdfs-versioned", "invoices/ORD-1042.pdf", "AaDP0iYJmbkDXWOZ8jKMwMh.7S5z7mn8", 10, "0011223344556677");
        assertEquals(claim, Claim.read(claim.toText()));
    }

    @Test
    void theSameOrderAlwaysGivesTheSameInvoiceAndACorrectionDiffers() {
        byte[] first = InvoicePdf.of("ORD-1042", 5000, 1);
        assertArrayEquals(first, InvoicePdf.of("ORD-1042", 5000, 1));
        byte[] corrected = InvoicePdf.of("ORD-1042", 5000, 2);
        assertEquals(first.length, corrected.length);
        assertFalse(Claim.checksum(first).equals(Claim.checksum(corrected)));
        assertEquals("bb8711d26a6daf29", Claim.checksum(InvoicePdf.of("ORD-1001", 1_500_000)));
    }

    @Test
    void base64SpellsEveryThreeBytesWithFourLetters() {
        assertEquals(2_000_000, Sender.asMessageText(new byte[1_500_000]).length());
        assertEquals(1_048_576, Sender.asMessageText(new byte[786_432]).length());
        assertEquals(1_048_580, Sender.asMessageText(new byte[786_433]).length());
        assertEquals(800_000, Sender.asMessageText(new byte[600_000]).length());
    }

    @Test
    void anExpiryStampIsReadTheWayS3WritesIt() {
        ZonedDateTime now = ZonedDateTime.now(ZoneOffset.UTC);
        // S3's rule: the stored time plus the rule's days, rounded up to the next midnight UTC.
        ZonedDateTime s3Would = now.plusDays(1).toLocalDate().plusDays(1).atStartOfDay(ZoneOffset.UTC);
        assertTrue(ClaimCheckS3Demo.stampedForMidnightWithinTwoDays(stamp(s3Would)));
        assertFalse(ClaimCheckS3Demo.stampedForMidnightWithinTwoDays(stamp(s3Would.plusDays(3))));
        assertFalse(ClaimCheckS3Demo.stampedForMidnightWithinTwoDays(stamp(s3Would.minusHours(5))));
        assertFalse(ClaimCheckS3Demo.stampedForMidnightWithinTwoDays(null));
    }

    private static String stamp(ZonedDateTime at) {
        return "expiry-date=\"" + DateTimeFormatter.RFC_1123_DATE_TIME.format(at) + "\", rule-id=\"remove-uncollected-invoices\"";
    }
}
