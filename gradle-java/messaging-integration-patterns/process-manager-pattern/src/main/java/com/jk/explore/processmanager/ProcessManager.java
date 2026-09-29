package com.jk.explore.processmanager;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * The pattern: one component that keeps each order's state, sends it to the next step, and decides what happens after each reply.
 *
 * <p>The services never call each other. They only answer the process
 * manager, which holds the whole route, including the unhappy paths: try the
 * partner warehouse when the main one is out of stock, release the stock and
 * email the customer when the card is declined.
 */
public final class ProcessManager {

    private final Services.Warehouse main;
    private final Services.Warehouse partner;
    private final Services.Payments payments;
    private final Services.Shipping shipping;
    private final Services.Emails emails;
    private final Map<String, String> state = new LinkedHashMap<>();
    private final Map<String, List<String>> history = new LinkedHashMap<>();

    public ProcessManager(Services.Warehouse main, Services.Warehouse partner, Services.Payments payments,
                          Services.Shipping shipping, Services.Emails emails) {
        this.main = main;
        this.partner = partner;
        this.payments = payments;
        this.shipping = shipping;
        this.emails = emails;
    }

    public void start(Order o) {
        history.put(o.id(), new ArrayList<>());
        step(o, "RESERVING", main.name() + " " + main.reserve(o.sku()));
    }

    /** Every reply comes back here; the manager decides the next step from the order's state and the reply. */
    private void step(Order o, String now, String reply) {
        state.put(o.id(), now);
        history.get(o.id()).add(reply);
        switch (reply) {
            case String r when r.endsWith("RESERVED") -> {
                Services.Warehouse from = r.startsWith(main.name()) ? main : partner;
                state.put(o.id(), "PAYING");
                step2(o, from, payments.charge(o.card()));
            }
            case String r when r.equals(main.name() + " OUT_OF_STOCK") ->
                    step(o, "RESERVING AT PARTNER", partner.name() + " " + partner.reserve(o.sku()));
            case String r when r.equals(partner.name() + " OUT_OF_STOCK") -> {
                state.put(o.id(), "CANCELLED: no stock anywhere");
                emails.send(o.id() + ": sorry, out of stock");
            }
            default -> state.put(o.id(), "STUCK on " + reply);
        }
    }

    private void step2(Order o, Services.Warehouse from, String reply) {
        history.get(o.id()).add(reply);
        if (reply.equals("PAID")) {
            state.put(o.id(), "SHIPPING");
            history.get(o.id()).add(shipping.ship(o.id()));
            state.put(o.id(), "DONE");
        } else {
            from.release(o.sku());
            history.get(o.id()).add(from.name() + " RELEASED");
            emails.send(o.id() + ": your card was declined");
            state.put(o.id(), "CANCELLED: payment declined, stock released");
        }
    }

    public String state(String orderId) {
        return state.get(orderId);
    }

    public List<String> history(String orderId) {
        return history.get(orderId);
    }

    public Map<String, String> allStates() {
        return state;
    }
}
