package com.jk.explore.staticfactory;

/**
 * The do-nothing discount. Because it holds no state, one instance serves
 * the whole program — which is exactly the freedom a static factory buys.
 */
final class NoDiscount implements Discount {

    static final NoDiscount INSTANCE = new NoDiscount();

    private NoDiscount() {
    }

    @Override
    public Money appliedTo(Order order) {
        return Money.zero();
    }

    @Override
    public String describe() {
        return "No discount";
    }
}
