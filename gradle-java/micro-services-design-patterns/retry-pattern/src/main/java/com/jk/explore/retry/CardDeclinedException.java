package com.jk.explore.retry;

/**
 * The bank said no. Not worth trying again — ever.
 *
 * A declined card will be declined identically on the second and third attempt. A
 * retry here buys nothing, costs the customer three delays, and hides a clear
 * answer behind a vague one. Telling this apart from a timeout is half of what this
 * pattern is.
 */
public class CardDeclinedException extends RuntimeException {

    public CardDeclinedException(String message) {
        super(message);
    }
}
