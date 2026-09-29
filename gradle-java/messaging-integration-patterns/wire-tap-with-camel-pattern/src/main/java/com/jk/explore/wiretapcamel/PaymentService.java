package com.jk.explore.wiretapcamel;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;

/**
 * The real work: charging and refunding. It knows nothing about auditing.
 */
public final class PaymentService {

    private final List<String> handled = new CopyOnWriteArrayList<>();

    public void handle(PaymentMessage m) {
        handled.add((m.getKind().equals("CHARGE") ? "charged " : "refunded ") + m.getOrderId());
    }

    public List<String> handled() {
        return handled;
    }
}
