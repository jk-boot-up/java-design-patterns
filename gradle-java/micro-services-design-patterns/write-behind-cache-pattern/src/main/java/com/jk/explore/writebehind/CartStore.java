package com.jk.explore.writebehind;

import java.util.Map;

/**
 * Where checkout keeps shopping carts: change a quantity, and read a cart back.
 */
public interface CartStore {

    /** Sets how many of an item are in the cart (0 removes it); returns how long the customer waited, in ms. */
    int set(String cartId, String item, int quantity);

    Map<String, Integer> get(String cartId);
}
