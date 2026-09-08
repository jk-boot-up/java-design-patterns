package com.jk.explore.templatemethod;

/**
 * The template method. {@link #fulfil(Order)} is the whole sequence an order
 * goes through, written once, and it is {@code final} on purpose: a subclass
 * may decide how a step behaves, and may not decide what order the steps run
 * in.
 *
 * <p>That single {@code final} is most of what the pattern is. Everything
 * else here is a decision about <em>which kind</em> of hole each step should
 * be, and there are three kinds:
 *
 * <ul>
 *   <li><b>Abstract steps</b> — {@link #routeName()}, {@link #reserveStock},
 *       {@link #charge}, {@link #dispatch}. Every route must answer, because
 *       there is no sensible default. Reserving stock in a warehouse and
 *       asking a marketplace seller to confirm have nothing in common but
 *       their place in the sequence.</li>
 *   <li><b>Steps with a default</b> — {@link #pack} and
 *       {@link #notifyCustomer}. Most routes want the ordinary behaviour and
 *       say nothing; the odd one out overrides.</li>
 *   <li><b>Hooks</b> — {@link #requiresShippingAddress()} and
 *       {@link #afterFulfilment}. These do nothing (or say "yes, the usual")
 *       and exist purely so a subclass can opt in or out of behaviour the
 *       base class controls.</li>
 * </ul>
 *
 * <p>Validation is deliberately {@code private}. It runs first, always, for
 * everybody. A route cannot replace it — it can only answer the one question
 * validation asks it, through the {@link #requiresShippingAddress()} hook.
 * That is a much smaller permission than "override validate", and it is the
 * difference between a base class that guarantees something and one that
 * merely hopes.
 */
public abstract class FulfilmentProcess {

    /**
     * The invariant sequence. Validate, reserve, charge, pack, dispatch,
     * notify — in that order, for every route this repository will ever add.
     *
     * <p>{@code final} because the order is the guarantee. If a subclass
     * could reorder it, a route could notify the customer before dispatch had
     * produced anything to tell them about, which is exactly the bug
     * {@link NaiveFulfilment} ships.
     */
    public final FulfilmentReport fulfil(Order order) {
        FulfilmentReport report = new FulfilmentReport(order.id(), routeName());
        validate(order, report);
        reserveStock(order, report);
        charge(order, report);
        pack(order, report);
        dispatch(order, report);
        notifyCustomer(order, report);
        afterFulfilment(order, report);
        return report;
    }

    /**
     * The one step no route may touch. Private, not protected: an override
     * that "just skips the address check for now" is how orders ship into the
     * void.
     */
    private void validate(Order order, FulfilmentReport report) {
        if (order.lines().isEmpty()) {
            throw new FulfilmentException("order " + order.id() + " has no lines");
        }
        if (order.customerEmail() == null || order.customerEmail().isBlank()) {
            throw new FulfilmentException("order " + order.id() + " has no customer email");
        }
        if (requiresShippingAddress() && !order.hasShippingAddress()) {
            throw new FulfilmentException("order " + order.id() + " has no shipping address");
        }
        report.step("validate", order.lines().size() + " line(s), "
                + order.itemCount() + " item(s), " + order.subtotal()
                + (requiresShippingAddress() ? ", address checked" : ", no address needed"));
    }

    // ---- required steps -------------------------------------------------

    /** How this route is named in the report. */
    protected abstract String routeName();

    /** Make sure the goods are actually available, however this route can. */
    protected abstract void reserveStock(Order order, FulfilmentReport report);

    /** Take the money, and record on the report how much ended up where. */
    protected abstract void charge(Order order, FulfilmentReport report);

    /** Hand the goods over, and record the reference the customer can chase. */
    protected abstract void dispatch(Order order, FulfilmentReport report);

    // ---- steps with a default -------------------------------------------

    /**
     * Put the goods in a box. The default is the ordinary case, so two of the
     * three routes say nothing about packing at all.
     */
    protected void pack(Order order, FulfilmentReport report) {
        report.step("pack", order.itemCount() + " item(s) boxed and labelled");
    }

    /**
     * Tell the customer. The default is the shipping email; the digital route
     * overrides it to include the licence key that {@code dispatch} has, by
     * then, already minted.
     */
    protected void notifyCustomer(Order order, FulfilmentReport report) {
        String message = "Order " + order.id() + " is on its way. Tracking: "
                + report.dispatchReference();
        report.notified(order.customerEmail() + ": " + message);
        report.step("notify", "emailed " + order.customerEmail());
    }

    // ---- hooks ----------------------------------------------------------

    /**
     * Whether validation should insist on a shipping address. True for
     * anything physical; a route with nothing to ship answers false.
     */
    protected boolean requiresShippingAddress() {
        return true;
    }

    /**
     * Runs after everything else. Does nothing by default — it is here so a
     * route with an extra obligation of its own has somewhere to put it
     * without the base class needing to know what that obligation is.
     */
    protected void afterFulfilment(Order order, FulfilmentReport report) {
        // deliberately empty
    }
}
