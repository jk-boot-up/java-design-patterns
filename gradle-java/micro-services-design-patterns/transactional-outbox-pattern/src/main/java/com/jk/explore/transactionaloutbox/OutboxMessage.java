package com.jk.explore.transactionaloutbox;

/**
 * A message waiting in the out-tray.
 *
 * The only surprising thing about it is where it lives: not in a broker, not in a queue, but
 * in a row in the Orders service's own database, right next to the order it is about. That
 * is the whole trick of the pattern, and everything else follows from it.
 *
 * <p>The {@code messageId} is generated here, by the service that wrote the message, and
 * never changes — not even when the same message is published a second time. Whoever
 * receives it can therefore recognise a duplicate, which is what the next pattern in the
 * category does with it.
 */
public record OutboxMessage(String messageId, String type, String orderId, Money total) {

    /** How the message reads on the wire. */
    @Override
    public String toString() {
        return type + "(" + orderId + ", " + total + ")";
    }
}
