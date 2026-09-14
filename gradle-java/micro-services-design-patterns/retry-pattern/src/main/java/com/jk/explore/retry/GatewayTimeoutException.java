package com.jk.explore.retry;

/**
 * The gateway did not answer in time. Worth trying again.
 *
 * The important word is <em>answer</em>. A timeout tells you nothing about whether
 * the work happened — the request may have been lost on the way out, or the reply
 * may have been lost on the way back after the card was charged. Both look
 * identical from here, which is precisely why the retry needs an idempotency key
 * rather than optimism.
 */
public class GatewayTimeoutException extends RuntimeException {

    public GatewayTimeoutException(String message) {
        super(message);
    }
}
