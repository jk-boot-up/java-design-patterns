package com.jk.explore.hexagonalspring.core.port;

import com.jk.explore.hexagonalspring.core.Receipt;

/** Driving port: what the outside world may ask of the shop. */
public interface PlaceOrder {
    Receipt place(String customer, String sku, int quantity);
}
