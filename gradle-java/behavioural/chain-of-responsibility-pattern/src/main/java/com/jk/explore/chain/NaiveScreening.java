package com.jk.explore.chain;

import java.util.Map;

/**
 * The version everybody writes first — and it is not a straw man. Four checks,
 * in order, early return on the first failure. For one market with rules that
 * never change, this is the right answer and the rest of this project would be
 * over-engineering.
 *
 * <p>Two things go wrong once it is real, and both are visible when you run the
 * demo:
 *
 * <ol>
 *   <li><b>The order of the checks is welded in.</b> Payment is checked before
 *       fraud, so an order that is both over the card limit and scoring 92 is
 *       reported as a card problem. The customer is invited to try another
 *       card — and there was nothing wrong with their cards — while the fraud
 *       team never hears that the account exists.</li>
 *   <li><b>A variant means a copy.</b> Trade accounts are invoiced monthly, so
 *       somebody copied the method and deleted the card check. In the same edit
 *       the address check went too. Nothing in the code relates the two
 *       methods, so nothing noticed.</li>
 * </ol>
 */
public final class NaiveScreening {

    /** Yes or no, and a sentence. There is no third answer, and no "who said so". */
    public record Result(boolean accepted, String message) {

        @Override
        public String toString() {
            return (accepted ? "ACCEPTED" : "REJECTED") + " — " + message;
        }
    }

    private static final Result OK = new Result(true, "nothing objected");

    private final Map<String, Integer> onShelf;

    public NaiveScreening(Map<String, Integer> onShelf) {
        this.onShelf = Map.copyOf(onShelf);
    }

    /** The standard flow. Four checks, in the order somebody happened to type them. */
    public Result validate(CheckoutRequest request) {
        if (!request.country().equals("GB") && !request.country().equals("IE")) {
            return new Result(false, "we do not ship to " + request.country());
        }
        for (String prefix : new String[] {"JE", "GY", "IM"}) {
            if (request.postcode().startsWith(prefix)) {
                return new Result(false, "no courier covers " + request.postcode());
            }
        }
        for (BasketItem item : request.items()) {
            if (onShelf.getOrDefault(item.sku(), 0) < item.quantity()) {
                return new Result(false, item.description() + " is out of stock");
            }
        }
        if (request.totalPounds() > request.cardLimitPounds()) {
            return new Result(false, "card limit exceeded, please try another card");
        }
        if (request.fraudScore() >= 80) {
            return new Result(false, "we are unable to process this order");
        }
        return OK;
    }

    /**
     * The trade-account flow: the same rules, minus the card limit, because
     * trade accounts are invoiced monthly.
     *
     * <p>This is a copy of {@link #validate} with one check deliberately
     * removed and one check accidentally removed. Read the two side by side and
     * try to spot the second one before running the demo.
     */
    public Result validateTradeAccount(CheckoutRequest request) {
        for (BasketItem item : request.items()) {
            if (onShelf.getOrDefault(item.sku(), 0) < item.quantity()) {
                return new Result(false, item.description() + " is out of stock");
            }
        }
        if (request.fraudScore() >= 80) {
            return new Result(false, "we are unable to process this order");
        }
        return OK;
    }
}
