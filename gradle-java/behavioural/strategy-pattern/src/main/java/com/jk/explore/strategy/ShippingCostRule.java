package com.jk.explore.strategy;

/**
 * One way of pricing a delivery — the Strategy interface.
 *
 * <p>Every implementation is a peer of every other: same input, same output,
 * different algorithm. That is the whole contract, and it is what lets
 * {@link CheckoutService} hold one without knowing or caring which.
 *
 * <p>The interface is deliberately tiny. A strategy interface that grows a
 * second method usually means two decisions have been bundled into one type,
 * and the implementations start having to leave one of them empty.
 */
public interface ShippingCostRule {

    /** How this rule appears on the customer's receipt. */
    String name();

    /**
     * What this shipment costs to deliver under this rule.
     *
     * <p>Implementations must be free of side effects and must not hold
     * per-shipment state: the same rule instance prices every order in the
     * shop, concurrently, so anything remembered between calls is a defect.
     */
    Money costFor(Shipment shipment);
}
