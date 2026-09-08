package com.jk.explore.templatemethod;

/**
 * The store's own warehouse. The ordinary route, and the one whose behaviour
 * the base class defaults were written for.
 *
 * <p>Notice what is <em>not</em> here: no {@code pack}, no
 * {@code notifyCustomer}, no {@code requiresShippingAddress}, no
 * {@code afterFulfilment}. This route wants the base class's answer to all
 * four, so it says nothing about them. A subclass that overrides only what
 * genuinely differs is the sign that the split between abstract steps,
 * defaults and hooks was drawn in the right place.
 */
public final class WarehouseFulfilment extends FulfilmentProcess {

    private final StockLedger ledger;
    private final String site;

    public WarehouseFulfilment(StockLedger ledger, String site) {
        this.ledger = ledger;
        this.site = site;
    }

    @Override
    protected String routeName() {
        return "warehouse";
    }

    @Override
    protected void reserveStock(Order order, FulfilmentReport report) {
        for (OrderLine line : order.lines()) {
            ledger.reserve(line.sku(), line.quantity());
        }
        report.step("reserve", order.itemCount() + " unit(s) held at " + site);
    }

    @Override
    protected void charge(Order order, FulfilmentReport report) {
        report.charged(order.subtotal());
        report.step("charge", order.subtotal() + " taken by the store");
    }

    @Override
    protected void dispatch(Order order, FulfilmentReport report) {
        String consignment = "CON-" + order.id();
        report.dispatchedAs(consignment);
        report.step("dispatch", "courier collected, consignment " + consignment);
    }
}
