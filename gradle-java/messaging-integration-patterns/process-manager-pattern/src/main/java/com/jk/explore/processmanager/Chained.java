package com.jk.explore.processmanager;

/**
 * Without the pattern: each step hands straight on to the next, and nobody owns the order's journey.
 *
 * <p>The warehouse reserves and passes to payments; payments passes to
 * shipping. When payment is declined, the chain just stops: the warehouse
 * never hears, so the reserved stock is never released.
 */
public final class Chained {

    private final Services.Warehouse warehouse;
    private final Services.Payments payments;
    private final Services.Shipping shipping;

    public Chained(Services.Warehouse warehouse, Services.Payments payments, Services.Shipping shipping) {
        this.warehouse = warehouse;
        this.payments = payments;
        this.shipping = shipping;
    }

    public String fulfil(Order o) {
        if (!warehouse.reserve(o.sku()).equals("RESERVED")) {
            return "stopped at the warehouse";
        }
        if (!payments.charge(o.card()).equals("PAID")) {
            return "stopped at payments";
        }
        return shipping.ship(o.id());
    }
}
