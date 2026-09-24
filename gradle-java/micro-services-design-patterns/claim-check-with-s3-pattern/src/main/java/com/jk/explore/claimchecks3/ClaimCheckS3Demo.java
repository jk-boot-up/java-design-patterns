package com.jk.explore.claimchecks3;

import java.time.Duration;
import java.time.ZoneOffset;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import software.amazon.awssdk.awscore.exception.AwsServiceException;

/**
 * Six acts against real Amazon S3 and SQS APIs, played by LocalStack in a container that this
 * program starts and stops.
 *
 * <p>Checkout hands each invoice PDF to the email service through a queue. The first act
 * shows a PDF the queue genuinely refuses. The rest store the PDF in a bucket and send only
 * a ticket, and show what S3 and SQS do with the ticket and the luggage that a simulation
 * cannot.
 */
public class ClaimCheckS3Demo {

    /** A business customer's monthly invoice, with every order and a scanned signature. */
    static final int BIG_INVOICE = 1_500_000;

    /** An ordinary invoice, small enough to go through the queue whole. */
    static final int SMALL_INVOICE = 600_000;

    public static void main(String[] args) {
        if (!LocalStack.containerRuntimeAvailable()) {
            System.out.println(LocalStack.NO_RUNTIME_ADVICE);
            return;
        }
        try (LocalStack aws = new LocalStack()) {
            try {
                aws.start();
            } catch (RuntimeException e) {
                System.out.println(LocalStack.WOULD_NOT_START_ADVICE);
                return;
            }
            one(aws);
            two(aws);
            three(aws);
            four(aws);
            five(aws);
            six(aws);
        }
    }

    /** The whole PDF, as a message. SQS refuses it. */
    private static void one(LocalStack aws) {
        System.out.println("ONE. An invoice too big for the queue.");
        Queue queue = Queue.create(aws.sqs(), "invoices-whole");
        System.out.println("  the email service's queue is on Amazon SQS, played by LocalStack. it reports its longest message as " + queue.maximumMessageBytes() + " bytes.");
        byte[] pdf = InvoicePdf.of("ORD-1001", BIG_INVOICE);
        String text = Sender.asMessageText(pdf);
        System.out.println("  a business customer's monthly invoice is a PDF of " + pdf.length + " bytes. a message is text, so it goes as base64: " + text.length() + " characters.");
        System.out.println("  SQS refuses it: " + refusal(() -> queue.send(text)));

        byte[] fits = InvoicePdf.of("ORD-1002", 786_432);
        byte[] oneMore = InvoicePdf.of("ORD-1003", 786_433);
        String fitsVerdict = refusal(() -> queue.send(Sender.asMessageText(fits)));
        String oneMoreVerdict = refusal(() -> queue.send(Sender.asMessageText(oneMore)));
        System.out.println("  a PDF of " + fits.length + " bytes becomes " + Sender.asMessageText(fits).length() + " characters and is " + verdict(fitsVerdict)
                + ". one byte more, " + oneMore.length + ", becomes " + Sender.asMessageText(oneMore).length() + " and is " + verdict(oneMoreVerdict) + ".");
        System.out.println("  base64 spells 3 bytes with 4 letters, so the largest PDF that fits is three quarters of the limit.");
    }

    /** Store the PDF, send the ticket, redeem it at the other end. */
    private static void two(LocalStack aws) {
        System.out.println("TWO. Send the ticket, not the luggage.");
        Bucket bucket = Bucket.create(aws.s3(), "invoice-pdfs");
        Queue queue = Queue.create(aws.sqs(), "invoice-tickets");
        byte[] pdf = InvoicePdf.of("ORD-1001", BIG_INVOICE);
        Claim claim = new Sender(bucket, queue).send(pdf);
        System.out.println("  checkout stores the PDF in an S3 bucket under a random key of " + claim.key().length() + " characters, then sends a ticket.");
        System.out.println("  the ticket is " + claim.bytesOnTheQueue() + " bytes of text: bucket, key, size " + claim.size() + ", checksum " + claim.sha256() + ".");
        byte[] got = new Receiver(bucket, queue).redeemNext();
        System.out.println("  the email service takes the ticket and fetches " + got.length + " bytes, identical to what was sent: " + Receiver.same(got, pdf) + ".");
        Poll.until("the queue to be empty", () -> queue.waiting() == 0);
        System.out.println("  it deletes the object, then the message. objects left in the bucket: " + bucket.keysListed() + ". messages waiting: " + queue.waiting() + ".");
    }

    /** Ten sent, six collected, and one stored whose ticket never went. */
    private static void three(LocalStack aws) {
        System.out.println("THREE. Luggage nobody collected.");
        Bucket bucket = Bucket.create(aws.s3(), "invoice-pdfs-uncollected");
        Queue queue = Queue.create(aws.sqs(), "invoice-tickets-uncollected");
        Sender sender = new Sender(bucket, queue);
        for (int i = 1; i <= 10; i++) {
            sender.send(InvoicePdf.of("ORD-" + (2000 + i), BIG_INVOICE));
        }
        Receiver receiver = new Receiver(bucket, queue);
        for (int i = 1; i <= 6; i++) {
            receiver.redeemNext();
        }
        Poll.until("four tickets to be waiting", () -> queue.waiting() == 4);
        System.out.println("  checkout sends 10 invoices by ticket. the email service collects 6, then stops.");
        System.out.println("  S3 still holds " + bucket.keysListed() + " invoices, and SQS still holds " + queue.waiting() + " tickets for them.");

        Sender broken = new Sender(bucket, Queue.missing(aws.sqs(), queue));
        String failure = refusal(() -> broken.send(InvoicePdf.of("ORD-2011", BIG_INVOICE)));
        System.out.println("  an 11th invoice is stored, and then its send fails: " + failure);
        int stored = bucket.keysListed();
        int tickets = queue.waiting();
        System.out.println("  S3 now holds " + stored + " invoices and SQS holds " + tickets + " tickets. " + (stored - tickets) + " invoice has no ticket, and nobody will ever ask for it.");
    }

    /** Two stores under one key: the checksum notices, versioning keeps both, delete keeps paying. */
    private static void four(LocalStack aws) {
        System.out.println("FOUR. The same key, twice.");
        Bucket plain = Bucket.create(aws.s3(), "invoice-pdfs-by-order");
        Queue plainQueue = Queue.create(aws.sqs(), "invoice-tickets-by-order");
        Sender sender = new Sender(plain, plainQueue);
        String key = "invoices/ORD-1042.pdf";
        byte[] first = InvoicePdf.of("ORD-1042", BIG_INVOICE, 1);
        byte[] corrected = InvoicePdf.of("ORD-1042", BIG_INVOICE, 2);
        sender.sendUnder(key, first);
        System.out.println("  a bucket keyed by order: ORD-1042's invoice is stored under " + key + " and its ticket sent.");
        sender.sendUnder(key, corrected);
        System.out.println("  a corrected invoice is stored under the same key before the first ticket is collected. S3 keeps " + plain.versionsStored() + " object.");
        try {
            new Receiver(plain, plainQueue).redeemNext();
        } catch (Receiver.NotTheSamePayload e) {
            System.out.println("  the email service redeems the first ticket: " + e.getMessage() + ".");
        }

        Bucket versioned = Bucket.create(aws.s3(), "invoice-pdfs-versioned").keepEveryVersion();
        Queue versionedQueue = Queue.create(aws.sqs(), "invoice-tickets-versioned");
        Sender versionedSender = new Sender(versioned, versionedQueue);
        versionedSender.sendUnder(key, first);
        versionedSender.sendUnder(key, corrected);
        byte[] got = new Receiver(versioned, versionedQueue).redeemNext();
        System.out.println("  with versioning on, each store keeps its own version and the ticket names one. first ticket, identical to the first invoice: " + Receiver.same(got, first) + ".");
        System.out.println("  the email service deletes the key as before. keys listed: " + versioned.keysListed() + ". versions still stored: " + versioned.versionsStored() + ". delete markers: " + versioned.deleteMarkers() + ".");
        for (String version : versioned.versionIds(key)) {
            versioned.delete(key, version);
        }
        System.out.println("  in a versioned bucket, delete hides the luggage and keeps paying for it. deleting each version by its id: " + versioned.versionsStored() + " stored.");
    }

    /** The ticket's clock and the luggage's clock are two different clocks. */
    private static void five(LocalStack aws) {
        System.out.println("FIVE. How long each one waits.");
        Bucket bucket = Bucket.create(aws.s3(), "invoice-pdfs-expiring").removeEverythingAfterDays(1);
        Queue queue = Queue.create(aws.sqs(), "invoice-tickets-expiring");
        System.out.println("  the bucket gets a rule: remove every invoice 1 day after it was stored. a day is the smallest unit S3 takes.");
        Claim claim = new Sender(bucket, queue).send(InvoicePdf.of("ORD-3001", BIG_INVOICE));
        String expiry = bucket.expiryOf(claim.key());
        System.out.println("  the invoice comes back stamped to expire at a midnight UTC, between 24 and 48 hours away: " + stampedForMidnightWithinTwoDays(expiry) + ".");
        int seconds = queue.keepsUnreadSeconds();
        System.out.println("  the queue keeps a ticket nobody has taken for " + seconds + " seconds, which is " + Duration.ofSeconds(seconds).toDays() + " days.");
        bucket.delete(claim.key());
        Poll.until("the ticket to be waiting", () -> queue.waiting() == 1);
        System.out.println("  the demo cannot wait a day, so it removes the invoice as the rule would. tickets still waiting: " + queue.waiting() + ".");
        System.out.println("  a slow email service redeems it: " + refusal(() -> new Receiver(bucket, queue).redeemNext()));
        System.out.println("  the ticket and the luggage each have their own clock, and nothing keeps the two in step.");
    }

    /** What the pattern costs, counted as requests the services actually received. */
    private static void six(LocalStack aws) {
        System.out.println("SIX. The bill.");
        Bucket bucket = Bucket.create(aws.s3(), "invoice-pdfs-bill");
        Queue queue = Queue.create(aws.sqs(), "invoice-tickets-bill");
        byte[] pdf = InvoicePdf.of("ORD-4001", SMALL_INVOICE);

        aws.resetCount();
        String text = Sender.asMessageText(pdf);
        new Sender(bucket, queue).sendWhole(pdf);
        queue.delete(queue.take());
        System.out.println("  a " + pdf.length + "-byte invoice sent whole: " + aws.requestTotal() + " requests " + names(aws.requests()) + ". the queue carried " + text.length() + " bytes.");

        aws.resetCount();
        Claim claim = new Sender(bucket, queue).send(pdf);
        new Receiver(bucket, queue).redeemNext();
        System.out.println("  the same invoice by ticket: " + aws.requestTotal() + " requests " + names(aws.requests()) + ". the queue carried " + claim.bytesOnTheQueue() + " bytes.");
        System.out.println("  twice the requests, two services to run and pay for, and a gap between storing and sending.");
        System.out.println("  this demo needed 1 container for 1 queue service and 1 storage service.");
    }

    private static String names(Map<String, Integer> requests) {
        StringBuilder out = new StringBuilder("(");
        requests.forEach((name, count) -> out.append(out.length() > 1 ? ", " : "").append(name).append(count > 1 ? " x" + count : ""));
        return out.append(")").toString();
    }

    /** Runs a request and returns the service's own reason for refusing it, or "accepted". */
    static String refusal(Runnable request) {
        try {
            request.run();
            return "accepted";
        } catch (AwsServiceException e) {
            String message = e.awsErrorDetails().errorMessage();
            int reason = message.indexOf("Reason: ");
            return reason >= 0 ? message.substring(reason + "Reason: ".length()) : message;
        }
    }

    private static String verdict(String refusal) {
        return refusal.equals("accepted") ? "accepted" : "refused";
    }

    /** S3 stamps an object with the midnight UTC after its lifecycle days have passed. */
    static boolean stampedForMidnightWithinTwoDays(String expiration) {
        if (expiration == null) {
            return false;
        }
        Matcher m = Pattern.compile("expiry-date=\"([^\"]+)\"").matcher(expiration);
        if (!m.find()) {
            return false;
        }
        ZonedDateTime at = ZonedDateTime.parse(m.group(1), DateTimeFormatter.RFC_1123_DATE_TIME).withZoneSameInstant(ZoneOffset.UTC);
        long hours = Duration.between(ZonedDateTime.now(ZoneOffset.UTC), at).toHours();
        return at.getHour() == 0 && at.getMinute() == 0 && hours >= 23 && hours <= 48;
    }
}
