package com.jk.explore.callback;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

/**
 * A payment gateway that answers later. A charge is only requested here. The answer is delivered when
 * the demo or a test calls complete, so the order of events is chosen, and never left to timing.
 */
public class Gateway {

    private record Pending(String orderId, Consumer<Result> onResult) {
    }

    private final List<Pending> pending = new ArrayList<>();
    private final List<String> callbackErrors = new ArrayList<>();

    /** Asks for a charge, and remembers what to call when the answer comes. Returns at once. */
    public void charge(String orderId, Consumer<Result> onResult) {
        pending.add(new Pending(orderId, onResult));
    }

    /** The answer for one order arrives. The gateway calls back whoever asked. */
    public void complete(String orderId, boolean paid) {
        Pending p = pending.stream().filter(x -> x.orderId().equals(orderId)).findFirst().orElseThrow();
        pending.remove(p);
        Result result = new Result(orderId, paid, paid ? "paid" : "card declined");
        try {
            p.onResult().accept(result);
        } catch (RuntimeException e) {
            callbackErrors.add(orderId + ": " + e.getMessage());
        }
    }

    public int pending() {
        return pending.size();
    }

    public List<String> callbackErrors() {
        return List.copyOf(callbackErrors);
    }
}
