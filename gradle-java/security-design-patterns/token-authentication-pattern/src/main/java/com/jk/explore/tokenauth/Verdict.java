package com.jk.explore.tokenauth;

/**
 * The result of checking a token: the customer it names, or why it was refused.
 */
public record Verdict(boolean valid, String customer, String reason) {

    static Verdict ok(String customer) {
        return new Verdict(true, customer, "");
    }

    static Verdict refused(String reason) {
        return new Verdict(false, null, reason);
    }
}
