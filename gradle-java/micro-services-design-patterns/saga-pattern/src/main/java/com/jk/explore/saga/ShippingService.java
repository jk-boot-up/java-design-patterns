package com.jk.explore.saga;

import java.util.ArrayList;
import java.util.List;

/**
 * Shipping. Schedules a shipment, and is the step most likely to refuse.
 *
 * It refuses for reasons that have nothing to do with the shop: no courier covers the
 * postcode, the parcel is too heavy for the service chosen, the depot is closed for the
 * bank holiday. That is why the demo has it fail last — a step that can refuse for reasons
 * you do not control is exactly the step whose failure has to be survivable.
 */
public final class ShippingService {

    public static final long LATENCY_MILLIS = 60;

    private final List<String> shipments = new ArrayList<>();
    private final RemoteCall<SagaContext, String> schedule;
    private final RemoteCall<String, String> cancel;
    private int nextRef = 1;
    private boolean refuseEveryPostcode;

    public ShippingService(SimulatedClock clock, CallLog log) {
        this.schedule = new RemoteCall<>("Shipping", LATENCY_MILLIS, this::doSchedule,
                clock, log);
        this.cancel = new RemoteCall<>("Shipping", LATENCY_MILLIS, this::doCancel, clock, log);
    }

    public String schedule(SagaContext context) {
        return schedule.invoke(context);
    }

    public String cancel(String shipmentRef) {
        return cancel.invoke(shipmentRef);
    }

    public void failNextSchedule(int count) {
        schedule.failNext(count);
    }

    /** No courier will take it. Not an outage, and not worth retrying. */
    public void refuseEveryPostcode() {
        refuseEveryPostcode = true;
    }

    public int shipmentsScheduled() {
        return shipments.size();
    }

    private String doSchedule(SagaContext context) {
        if (refuseEveryPostcode) {
            throw new CannotDeliverException(context.orderId());
        }
        String ref = "shp-" + nextRef++;
        shipments.add(ref);
        return ref;
    }

    private String doCancel(String shipmentRef) {
        shipments.remove(shipmentRef);
        return "cancelled " + shipmentRef;
    }
}
