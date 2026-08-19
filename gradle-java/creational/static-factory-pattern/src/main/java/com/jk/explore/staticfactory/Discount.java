package com.jk.explore.staticfactory;

/**
 * A discount on an order.
 *
 * <p>This interface is also the only door into every discount the program
 * has. The implementing classes are package-private, so a caller outside
 * this package cannot name them, cannot {@code new} them, and never learns
 * how many there are.
 *
 * <p>Read the factory methods below and notice three things a constructor
 * could not have done:
 *
 * <ul>
 *   <li>They have <em>names</em>. {@code percentage(10)} and
 *       {@code amountOff(Money.pounds(10))} are unmistakable; two
 *       constructors taking one number could not even coexist.</li>
 *   <li>They may hand back an <em>existing</em> object rather than a new
 *       one — {@link #none()} always returns the same instance.</li>
 *   <li>They choose the <em>class</em> of what comes back.
 *       {@code percentage(0)} quietly returns the do-nothing discount, and
 *       nobody outside notices.</li>
 * </ul>
 */
public interface Discount {

    /** How much comes off this order. Never more than the order is worth. */
    Money appliedTo(Order order);

    /** Wording for the receipt line. */
    String describe();

    /** No discount at all. Always the same instance — there is nothing to vary. */
    static Discount none() {
        return NoDiscount.INSTANCE;
    }

    /**
     * A percentage off the subtotal. Asking for 0% gives you back
     * {@link #none()}: the caller said what it wanted, not which class to
     * build, so we are free to pick the cheaper one.
     */
    static Discount percentage(int percent) {
        if (percent < 0 || percent > 100) {
            throw new IllegalArgumentException("percentage must be 0-100, was " + percent);
        }
        return percent == 0 ? none() : new PercentageDiscount(percent);
    }

    /** A flat amount off the subtotal. */
    static Discount amountOff(Money amount) {
        return amount.isZero() ? none() : new AmountOffDiscount(amount);
    }

    /** Shipping on the house. Nothing to vary, so again one shared instance. */
    static Discount freeShipping() {
        return FreeShippingDiscount.INSTANCE;
    }

    /**
     * Whichever of the two takes more off this particular order. The
     * composite that does the comparing is a class the caller never sees
     * and could not have written itself.
     */
    static Discount bestOf(Discount first, Discount second) {
        return new BestOfDiscount(first, second);
    }

    /**
     * Turns a coupon code from the storefront into a discount. Every code
     * produces a different implementation class, and the calling code is
     * identical for all of them.
     */
    static Discount forCoupon(String code) {
        return switch (code.trim().toUpperCase()) {
            case "SAVE10" -> percentage(10);
            case "SAVE25" -> percentage(25);
            case "FIVEROFF" -> amountOff(Money.pounds(5));
            case "FREESHIP" -> freeShipping();
            case "BESTDEAL" -> bestOf(percentage(10), amountOff(Money.pounds(5)));
            case "" -> none();
            default -> throw new IllegalArgumentException("unknown coupon code: " + code);
        };
    }
}
