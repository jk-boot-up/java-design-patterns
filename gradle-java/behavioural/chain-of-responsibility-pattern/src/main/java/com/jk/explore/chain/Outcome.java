package com.jk.explore.chain;

/**
 * What screening concluded about a checkout.
 *
 * <p>Three values, not two. A boolean can only say yes or no, and the third
 * answer — "a person needs to look at this" — is the one the naive version in
 * this project cannot express, so it guesses.
 */
public enum Outcome {

    /** Let it through to payment capture. */
    APPROVED,

    /** Stop, and tell the customer why. */
    REJECTED,

    /** Hold it in a queue for a human reviewer. */
    REFERRED
}
