package com.jk.explore.guaranteed;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The five acts: messages only in memory, a journal on disk, acknowledgements, a crash between sending and acknowledging, and the bill.
 */
public final class GuaranteedDeliveryDemo {

    public static void main(String[] args) throws IOException {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    static String email(int i) {
        return "Thank you for order ORD-" + i;
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws IOException {
        List<String> out = new ArrayList<>();
        Path dir = Files.createTempDirectory("guaranteed-delivery");

        out.add("ONE. Confirmation emails queued in memory.");
        MemoryQueue memory = new MemoryQueue();
        for (int i = 1; i <= 10; i++) {
            memory.send(email(i));
        }
        out.add("  10 emails queued; the email provider is slow today");
        memory = new MemoryQueue();
        out.add("  the server restarts for an update: queued emails now " + memory.size());
        out.add("  10 customers will never hear that their order was received");

        out.add("");
        out.add("TWO. Every message written to disk before it is accepted.");
        Path file = dir.resolve("emails.journal");
        Journal journal = new Journal(file);
        for (int i = 1; i <= 10; i++) {
            journal.send("MAIL-" + i, email(i));
        }
        out.add("  10 emails accepted; the journal file has " + journal.lines().size() + " lines");
        Journal afterRestart = new Journal(file);
        out.add("  the server restarts; a new journal reads the file: " + afterRestart.unacknowledged().size() + " emails waiting");

        out.add("");
        out.add("THREE. Delivered messages are acknowledged.");
        EmailSender sender = new EmailSender();
        int n = 0;
        for (Map.Entry<String, String> e : afterRestart.unacknowledged().entrySet()) {
            if (n++ == 6) {
                break;
            }
            sender.send(e.getKey(), e.getValue());
            afterRestart.acknowledge(e.getKey());
        }
        out.add("  6 emails sent and acknowledged; then the server crashes");
        Journal third = new Journal(file);
        out.add("  after the restart, still waiting: " + third.unacknowledged().keySet());
        for (Map.Entry<String, String> e : third.unacknowledged().entrySet()) {
            sender.send(e.getKey(), e.getValue());
            third.acknowledge(e.getKey());
        }
        out.add("  sent: " + sender.sent().size() + " of 10, each exactly once; waiting now " + third.unacknowledged().size());

        out.add("");
        out.add("FOUR. A crash between sending and acknowledging.");
        Path file2 = dir.resolve("emails2.journal");
        Journal j = new Journal(file2);
        j.send("MAIL-11", email(11));
        EmailSender s2 = new EmailSender();
        s2.send("MAIL-11", email(11));
        out.add("  MAIL-11 is sent, and the server crashes before writing its acknowledgement");
        Journal j2 = new Journal(file2);
        j2.unacknowledged().forEach((id, body) -> {
            s2.send(id, body);
            j2.acknowledge(id);
        });
        out.add("  after the restart it is sent again: the customer gets " + s2.sent().size() + " emails; duplicates " + s2.duplicates());
        out.add("  guaranteed delivery means at least once, not exactly once");

        out.add("");
        out.add("FIVE. The bill: the disk is in the path of every message.");
        out.add("  10 emails cost " + journal.diskWrites() + " forced disk writes to accept, and one more each to acknowledge");
        out.add("  the journal grows until someone trims acknowledged lines, and receivers must cope with duplicates");
        return out;
    }

    private GuaranteedDeliveryDemo() {
    }
}
