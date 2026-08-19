package com.jk.explore.staticfactory;

/**
 * Takes the shipping cost off instead of touching the subtotal. Proof that
 * "a discount" is a behaviour, not a number: the caller writes the same
 * line of code either way.
 */
final class FreeShippingDiscount implements Discount {

    static final FreeShippingDiscount INSTANCE = new FreeShippingDiscount();

    private FreeShippingDiscount() {
    }

    @Override
    public Money appliedTo(Order order) {
        return order.shipping();
    }

    @Override
    public String describe() {
        return "Free shipping";
    }
}
