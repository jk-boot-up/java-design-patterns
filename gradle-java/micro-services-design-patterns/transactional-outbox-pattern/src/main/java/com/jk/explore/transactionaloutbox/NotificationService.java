package com.jk.explore.transactionaloutbox;

import java.util.ArrayList;
import java.util.List;

/**
 * Whoever is on the other end of the message. Here, the service that emails the customer.
 *
 * It is deliberately as simple as a subscriber can be: a message arrives, an email goes out.
 * It keeps no record of what it has already seen, so if the same message arrives twice the
 * customer gets two emails. That is not an oversight in this project — it is the thing the
 * next pattern in the category fixes, and it has to be visible here first.
 */
public final class NotificationService {

    private final List<String> emails = new ArrayList<>();
    private final CallLog log;

    public NotificationService(CallLog log) {
        this.log = log;
    }

    /** Handles a message with no memory of whether it has handled it before. */
    public void on(OutboxMessage message) {
        emails.add("your order " + message.orderId() + " for " + message.total()
                + " is confirmed");
        log.note("Notifications", "EMAILED", "message " + message.messageId());
    }

    public List<String> emails() {
        return List.copyOf(emails);
    }

    public int emailsSent() {
        return emails.size();
    }
}
