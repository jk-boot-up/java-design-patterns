package com.jk.explore.circuitbreaker;

/**
 * Checkout: the same breaker, and no fallback at all.
 *
 * This is the half of the pattern that gets left out of the tutorials. A breaker is
 * not a device for making failures disappear; it is a device for failing
 * <em>quickly</em>. On the product page that fast failure buys a fallback. Here
 * there is no fallback to buy, because there is nothing a shop can substitute for
 * taking the money — so what the speed buys instead is an honest message in a
 * hundredth of a second rather than a spinner for three seconds.
 *
 * <p>The breaker is still worth having. It stops a thousand shoppers each spending
 * three seconds discovering the same outage, and it stops their thousand waiting
 * threads from taking down the parts of the shop that still work.
 */
public final class CheckoutService {

    private final PaymentsService payments;
    private final CircuitBreaker breaker;
    private final CallLog log;

    public CheckoutService(PaymentsService payments, CircuitBreaker breaker, CallLog log) {
        this.payments = payments;
        this.breaker = breaker;
        this.log = log;
    }

    /**
     * Takes payment, or says plainly that it cannot.
     *
     * @throws CheckoutUnavailableException if payments cannot be reached, whether
     *         because the call failed or because the breaker refused to make it
     */
    public String pay(String orderId, Money amount) {
        try {
            return breaker.call(() -> payments.charge(orderId, amount));
        } catch (CircuitOpenException refused) {
            log.note("Checkout", "HONEST-NO", "told the shopper at once, card untouched");
            throw new CheckoutUnavailableException(
                    "We cannot take payment at the moment. Your basket is saved.");
        } catch (ServiceUnavailableException failed) {
            log.note("Checkout", "HONEST-NO", "told the shopper after a timeout");
            throw new CheckoutUnavailableException(
                    "We cannot take payment at the moment. Your basket is saved.");
        }
    }
}
