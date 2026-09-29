package com.jk.explore.wiretap;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import java.util.function.Consumer;

/**
 * A point-to-point channel from checkout to payment, with a place to attach wire taps.
 */
public final class Channel {

    private final Consumer<PaymentMessage> destination;
    private final List<Consumer<PaymentMessage>> taps = new CopyOnWriteArrayList<>();

    public Channel(Consumer<PaymentMessage> destination) {
        this.destination = destination;
    }

    public void attach(Consumer<PaymentMessage> tap) {
        taps.add(tap);
    }

    public void detach(Consumer<PaymentMessage> tap) {
        taps.remove(tap);
    }

    public void send(PaymentMessage m) {
        taps.forEach(t -> t.accept(m));
        destination.accept(m);
    }
}
