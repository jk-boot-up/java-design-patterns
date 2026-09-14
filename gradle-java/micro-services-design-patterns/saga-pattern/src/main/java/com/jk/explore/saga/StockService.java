package com.jk.explore.saga;

import java.util.LinkedHashMap;
import java.util.Map;

/** Stock. Reserves what is on the shelf, and releases it again when asked. */
public final class StockService {

    public static final long LATENCY_MILLIS = 30;

    private final Map<String, Integer> onShelf = new LinkedHashMap<>();
    private final Map<String, SagaContext> reservations = new LinkedHashMap<>();
    private final RemoteCall<SagaContext, String> reserve;
    private final RemoteCall<String, String> release;
    private int nextRef = 1;

    public StockService(SimulatedClock clock, CallLog log) {
        this.reserve = new RemoteCall<>("Stock", LATENCY_MILLIS, this::doReserve, clock, log);
        this.release = new RemoteCall<>("Stock", LATENCY_MILLIS, this::doRelease, clock, log);
    }

    public void stock(String sku, int quantity) {
        onShelf.put(sku, quantity);
    }

    public int available(String sku) {
        return onShelf.getOrDefault(sku, 0);
    }

    public String reserve(SagaContext context) {
        return reserve.invoke(context);
    }

    public String release(String reservationRef) {
        return release.invoke(reservationRef);
    }

    public void failNextReserve(int count) {
        reserve.failNext(count);
    }

    public void failNextRelease(int count) {
        release.failNext(count);
    }

    public int reservationsHeld() {
        return reservations.size();
    }

    private String doReserve(SagaContext context) {
        for (SagaContext.Line line : context.lines()) {
            if (available(line.sku()) < line.quantity()) {
                throw new OutOfStockException(line.sku(), line.quantity(),
                        available(line.sku()));
            }
        }
        for (SagaContext.Line line : context.lines()) {
            onShelf.put(line.sku(), available(line.sku()) - line.quantity());
        }
        String ref = "res-" + nextRef++;
        reservations.put(ref, context);
        return ref;
    }

    private String doRelease(String reservationRef) {
        SagaContext context = reservations.remove(reservationRef);
        if (context == null) {
            return reservationRef + " was not held";
        }
        for (SagaContext.Line line : context.lines()) {
            onShelf.put(line.sku(), available(line.sku()) + line.quantity());
        }
        return "released " + reservationRef;
    }
}
