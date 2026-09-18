package com.jk.explore.sidecarjavaproxy;

/**
 * What comes back when the money is taken.
 *
 * <p>Two numbers, and this project is the difference between them. {@code attempts} is
 * how many times the provider was asked; {@code waitedMillis} is how long the proxy
 * spent getting there. Both proxies in this project are allowed exactly three attempts,
 * so {@code attempts} comes out the same for both of them and tells you nothing. The
 * second number is where they differ, and the second number is what decides whether the
 * payment goes through.
 */
public record Receipt(String orderRef, String providerRef, int attempts, long waitedMillis) {

    public String describe() {
        String tries = attempts == 1 ? "1 attempt" : attempts + " attempts";
        return providerRef + " (" + tries + ", " + waitedMillis + "ms waiting)";
    }
}
