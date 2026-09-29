package com.jk.explore.railway;

import java.util.Map;

/**
 * Before: each step throws its own exception, and the caller has to remember to catch every one.
 */
public final class ExceptionCheckout {

    static class OutOfStockException extends RuntimeException {
        OutOfStockException(String m) {
            super(m);
        }
    }

    static class PaymentDeclinedException extends RuntimeException {   // added later by the payments team
        PaymentDeclinedException(String m) {
            super(m);
        }
    }

    static String place(Cart cart) {
        for (Map.Entry<String, Integer> line : cart.items().entrySet()) {
            if (CheckoutSteps.STOCK.getOrDefault(line.getKey(), 0) < line.getValue()) {
                throw new OutOfStockException(line.getKey() + " is out of stock");
            }
        }
        if (cart.card().endsWith("0002")) {
            throw new PaymentDeclinedException("card declined");
        }
        return "order ORD-1 confirmed";
    }

    /** The web controller: written before PaymentDeclinedException existed. */
    public static String controller(Cart cart) {
        try {
            return "200 " + place(cart);
        } catch (OutOfStockException e) {
            return "409 " + e.getMessage();
        } catch (RuntimeException unexpected) {
            return "500 internal server error";
        }
    }

    private ExceptionCheckout() {
    }
}
