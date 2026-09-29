package com.jk.explore.guaranteedrabbit;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against a real RabbitMQ broker started and stopped by this program.
 */
public final class RabbitGuaranteedDeliveryDemo {

    public static void main(String[] args) throws Exception {
        if (!Broker.containerRuntimeAvailable()) {
            System.out.println(Broker.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Broker broker = new Broker()) {
            try {
                broker.start();
            } catch (RuntimeException e) {
                out.add(Broker.WOULD_NOT_START_ADVICE);
                return out;
            }

            out.add("ONE. A durable queue, but messages sent as not persistent.");
            try (Outbox outbox = new Outbox(broker, "emails-transient", false)) {
                for (int i = 1; i <= 10; i++) {
                    outbox.send("MAIL-" + i);
                }
            }
            out.add("  10 emails queued: waiting " + broker.waiting("emails-transient"));
            broker.restart();
            int after = broker.waiting("emails-transient");
            out.add("  the broker restarts: the queue is still there, waiting " + after);
            out.add("  a durable queue is not enough: each message must be marked persistent too");
            out.add("  10 customers will never hear that their order was received");

            out.add("");
            out.add("TWO. Persistent messages, and publisher confirms.");
            try (Outbox outbox = new Outbox(broker, "emails", true)) {
                for (int i = 1; i <= 10; i++) {
                    outbox.send("MAIL-" + i);
                }
            }
            out.add("  10 emails sent; the broker confirmed each one only after storing it on disk");
            broker.restart();
            out.add("  the broker restarts: waiting " + broker.waiting("emails"));

            out.add("");
            out.add("THREE. The email sender acknowledges each email after sending it.");
            EmailSender sender = new EmailSender();
            sender.take(broker, "emails", 6, false);
            out.add("  6 emails sent and acknowledged; then the sender stops");
            out.add("  still waiting: " + broker.waiting("emails"));
            sender.take(broker, "emails", 10, false);
            out.add("  a new sender takes the rest: sent " + sender.sent().size() + " of 10, each once; waiting now "
                    + broker.waiting("emails"));

            out.add("");
            out.add("FOUR. The sender dies after sending MAIL-11, before acknowledging it.");
            try (Outbox outbox = new Outbox(broker, "emails", true)) {
                outbox.send("MAIL-11");
            }
            sender.take(broker, "emails", 1, true);
            Poll.until("MAIL-11 to be back on the queue", () -> broker.waiting("emails") == 1);
            sender.take(broker, "emails", 1, false);
            out.add("  RabbitMQ puts it back and delivers it again, marked as redelivered: " + sender.redelivered());
            out.add("  the customer gets MAIL-11 " + sender.timesSent("MAIL-11") + " times");
            out.add("  guaranteed delivery means at least once; the redelivered flag lets a receiver check first");

            out.add("");
            out.add("FIVE. The bill.");
            out.add("  every email now waits for a disk write and a confirm from the broker before checkout moves on");
            out.add("  and the broker is one more system to run, back up and watch; one node is still one disk");
        }
        return out;
    }

    private RabbitGuaranteedDeliveryDemo() {
    }
}
