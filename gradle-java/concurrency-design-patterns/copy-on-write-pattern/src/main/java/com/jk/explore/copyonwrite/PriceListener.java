package com.jk.explore.copyonwrite;

/**
 * Something that wants to hear when a product's price changes: the web page cache, the app, the email service.
 */
public interface PriceListener {

    void priceChanged(String sku, long pence);
}
