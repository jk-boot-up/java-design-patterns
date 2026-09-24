package com.jk.explore.claimchecks3;

import java.nio.charset.StandardCharsets;
import java.util.Random;

/**
 * An invoice as a PDF file: a header line, then bytes of every value from 0 to 255, the way a
 * real PDF's compressed pages and embedded fonts look.
 *
 * <p>The bytes are made from the order id and an edition number, so the same order always
 * gives the same file, and a corrected edition of the same order gives a different one of the
 * same size.
 */
public final class InvoicePdf {

    private InvoicePdf() {
    }

    public static byte[] of(String orderId, int bytes) {
        return of(orderId, bytes, 1);
    }

    public static byte[] of(String orderId, int bytes, int edition) {
        byte[] pdf = new byte[bytes];
        new Random((orderId + "#" + edition).hashCode()).nextBytes(pdf);
        byte[] header = ("%PDF-1.7 invoice " + orderId + " edition " + edition + "\n").getBytes(StandardCharsets.US_ASCII);
        System.arraycopy(header, 0, pdf, 0, Math.min(header.length, bytes));
        return pdf;
    }
}
