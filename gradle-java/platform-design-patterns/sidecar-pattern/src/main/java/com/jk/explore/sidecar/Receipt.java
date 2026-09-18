package com.jk.explore.sidecar;

/**
 * What comes back when the money is taken.
 *
 * <p>{@code attempts} is the number of times the payment gateway was actually asked, not
 * the number of times the caller asked. A caller makes one call; the retry code behind it
 * may turn that into six. The gap between those two numbers is what this whole project is
 * about, so the receipt carries it rather than hiding it.
 */
public record Receipt(String orderRef, String providerRef, int attempts, long waitedMillis) {

    public String describe() {
        String tries = attempts == 1 ? "1 attempt" : attempts + " attempts";
        return providerRef + " (" + tries + ", " + waitedMillis + "ms waiting)";
    }
}
