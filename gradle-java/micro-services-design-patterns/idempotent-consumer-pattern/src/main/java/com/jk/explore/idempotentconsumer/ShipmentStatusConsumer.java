package com.jk.explore.idempotentconsumer;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * A consumer with no dedupe store at all, and it does not need one.
 *
 * All it does is set a status: "order ord-1 is SHIPPED". Doing that twice leaves exactly the
 * same row as doing it once, because the operation is an assignment rather than a change. That
 * property has a name — the operation is <b>naturally idempotent</b> — and it is a different
 * thing from the {@link IdempotentNotificationConsumer} above, which is not naturally
 * idempotent and has to be <em>made</em> safe by remembering ids.
 *
 * <p><b>This is always the better answer when it is available</b>, and it should be the first
 * thing you look for. There is no table to operate, no expiry window to guess at, nothing to
 * grow forever, and no ordering worry either.
 *
 * <p>The test for it is one question: <i>if I run this twice, is the result the same?</i>
 *
 * <ul>
 *   <li>"set the status to SHIPPED" — yes. Nothing needed.</li>
 *   <li>"set the stock level to 20" — yes.</li>
 *   <li>"add 70 loyalty points" — no. See {@link LoyaltyPointsConsumer}.</li>
 *   <li>"send an email" — no, and no amount of rewriting will make it so.</li>
 * </ul>
 *
 * <p>Quite often a handler that fails the test can be rewritten into one that passes it — "add
 * 70 points" becomes "set the points for this order to 70" — and doing that is worth more than
 * any dedupe store.
 */
public final class ShipmentStatusConsumer implements MessageConsumer {

    private final Map<String, String> statuses = new LinkedHashMap<>();
    private final CallLog log;

    public ShipmentStatusConsumer(CallLog log) {
        this.log = log;
    }

    @Override
    public String name() {
        return "Shipping";
    }

    /** No id check, no transaction, no store. An assignment cannot happen twice. */
    @Override
    public void handle(Message message) {
        statuses.put(message.orderId(), "SHIPPED");
        log.note(name(), "SET", message.orderId() + " -> SHIPPED");
    }

    public String statusOf(String orderId) {
        return statuses.get(orderId);
    }

    public int ordersKnown() {
        return statuses.size();
    }
}
