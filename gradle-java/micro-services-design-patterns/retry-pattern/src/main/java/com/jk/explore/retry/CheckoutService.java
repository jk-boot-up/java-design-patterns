package com.jk.explore.retry;

/**
 * Checkout, done carefully.
 *
 * The whole of the care is in one line: the {@link PaymentRequest} is built
 * <em>once</em>, outside the retry, so every attempt carries the same idempotency
 * key. Move that line inside the lambda and this class becomes the naive one.
 */
public final class CheckoutService {

    private final PaymentGateway payments;
    private final RetryPolicy policy;
    private final SimulatedClock clock;
    private final CallLog log;

    public CheckoutService(PaymentGateway payments, RetryPolicy policy,
                           SimulatedClock clock, CallLog log) {
        this.payments = payments;
        this.policy = policy;
        this.clock = clock;
        this.log = log;
    }

    /**
     * Takes payment for an order, surviving a flaky network.
     *
     * @throws CardDeclinedException straight away, with no retries, if the bank
     *         refuses
     * @throws GatewayTimeoutException if the gateway never answers, after every
     *         attempt allowed by the policy
     */
    public Receipt pay(String orderId, Money amount) {
        PaymentRequest request = PaymentRequest.forOrder(orderId, amount);
        Retrier retrier = new Retrier(policy, clock, log);
        return retrier.call("payment for " + orderId, () -> payments.charge(request));
    }
}
