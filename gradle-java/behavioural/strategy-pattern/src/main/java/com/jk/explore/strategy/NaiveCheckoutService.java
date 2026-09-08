package com.jk.explore.strategy;

/**
 * The same four rules, without the pattern — kept so the comparison is
 * against real code rather than a straw man.
 *
 * <p>Nothing here is stupid. This is what a competent developer writes first,
 * and for two rules that never change it would be the right answer. It is
 * included because the problems below are not obvious until the method has
 * been added to three or four times, by which point it is load-bearing and
 * nobody wants to touch it.
 *
 * <p>What has gone wrong by this point:
 *
 * <ul>
 *   <li><b>Four algorithms share one method.</b> The weight bands, the
 *       per-hundred-miles rounding and the campaign threshold are interleaved
 *       in one body, and reading any one of them means reading past the other
 *       three.
 *   <li><b>None of them can be tested alone.</b> Every test of the distance
 *       arithmetic goes through {@code quote}, so it must supply a weight and
 *       a subtotal that are irrelevant to what it is checking.
 *   <li><b>A fifth rule edits this class.</b> The one place that is already
 *       the most tested and the most depended upon is the place that has to
 *       change, and the compiler will not tell you if you add the case to the
 *       enum and forget it here — which is exactly the bug
 *       {@link #quote} carries below.
 *   <li><b>The constants are anonymous.</b> {@code 3.50}, {@code 5},
 *       {@code 12.00} sit in the flow with nothing naming what they are.
 * </ul>
 */
public final class NaiveCheckoutService {

    private final ShippingMethod method;

    public NaiveCheckoutService(ShippingMethod method) {
        this.method = method;
    }

    /**
     * Prices a shipment by branching on the configured method.
     *
     * <p>Note the {@code default}. It exists because the compiler demands the
     * method return something, and it does the only safe-looking thing: it
     * charges nothing. Add a fifth constant to {@link ShippingMethod} and
     * forget to add a case here, and the shop starts shipping free — with no
     * compile error and no exception, just a quietly wrong number on the
     * receipt. The pattern version cannot reach this state, because there is
     * no list of rules to fall off the end of.
     */
    public Quote quote(Shipment shipment) {
        Money delivery;
        String name;

        switch (method) {
            case FLAT_RATE -> {
                name = "Flat rate";
                delivery = Money.pounds(4.99);
            }
            case WEIGHT_BANDED -> {
                name = "Weight banded";
                if (shipment.weightKg() <= 1) {
                    delivery = Money.pounds(3.50);
                } else if (shipment.weightKg() <= 5) {
                    delivery = Money.pounds(6.00);
                } else if (shipment.weightKg() <= 20) {
                    delivery = Money.pounds(12.00);
                } else {
                    delivery = Money.pounds(25.00);
                }
            }
            case DISTANCE_BASED -> {
                name = "Distance based";
                int units = (shipment.distanceMiles() + 99) / 100;
                delivery = Money.pounds(2.00);
                for (int i = 0; i < units; i++) {
                    delivery = delivery.plus(Money.pounds(1.50));
                }
            }
            case FREE_OVER_THRESHOLD -> {
                name = "Free over £50.00";
                delivery = shipment.orderSubtotal().compareTo(Money.pounds(50.00)) >= 0
                        ? Money.zero()
                        : Money.pounds(4.99);
            }
            default -> {
                name = "Unknown";
                delivery = Money.zero();
            }
        }

        return new Quote(name, shipment.orderSubtotal(), delivery);
    }
}
