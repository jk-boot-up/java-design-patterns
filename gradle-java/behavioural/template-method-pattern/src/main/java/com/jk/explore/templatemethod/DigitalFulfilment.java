package com.jk.explore.templatemethod;

/**
 * A download. No stock to hold, nothing to put in a box, and nowhere to ship
 * to — and yet it runs the same six steps as everything else, because the
 * shape of fulfilment does not change just because the goods are weightless.
 *
 * <p>This is the route that justifies each kind of hole in the base class:
 *
 * <ul>
 *   <li>the {@code requiresShippingAddress} <b>hook</b> is what lets an order
 *       with no address through validation, without weakening validation for
 *       anybody else;</li>
 *   <li>{@code reserveStock} and {@code pack} are overridden to <b>record
 *       that they had nothing to do</b> rather than to disappear — the report
 *       still shows six steps, and "nothing to reserve" is a fact worth
 *       printing;</li>
 *   <li>{@code notifyCustomer} is overridden to include the licence key, and
 *       it can only do that because the base class fixed the order and
 *       {@code dispatch} has already run. That guarantee is the whole reason
 *       {@code fulfil} is {@code final}.</li>
 * </ul>
 */
public final class DigitalFulfilment extends FulfilmentProcess {

    @Override
    protected String routeName() {
        return "digital";
    }

    @Override
    protected boolean requiresShippingAddress() {
        return false;
    }

    @Override
    protected void reserveStock(Order order, FulfilmentReport report) {
        report.step("reserve", "nothing to reserve, " + order.itemCount() + " download(s)");
    }

    @Override
    protected void charge(Order order, FulfilmentReport report) {
        report.charged(order.subtotal());
        report.step("charge", order.subtotal() + " taken by the store");
    }

    @Override
    protected void pack(Order order, FulfilmentReport report) {
        report.step("pack", "nothing to pack");
    }

    @Override
    protected void dispatch(Order order, FulfilmentReport report) {
        String key = LicenceKeys.mint(order);
        report.dispatchedAs(key);
        report.step("dispatch", "licence key issued: " + key);
    }

    @Override
    protected void notifyCustomer(Order order, FulfilmentReport report) {
        String message = "Order " + order.id() + " is ready to download. Key: "
                + report.dispatchReference();
        report.notified(order.customerEmail() + ": " + message);
        report.step("notify", "emailed " + order.customerEmail() + " with the key");
    }
}
