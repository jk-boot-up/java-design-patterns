package com.jk.explore.actorpattern;

/** The messages the shop's actors send each other. Plain records: nothing in them can be changed. */
public final class Messages {

    private Messages() {
    }

    public record Reserve(String sku, int quantity) {
    }

    public record Reserved(String sku, int quantity) {
    }

    public record OutOfStock(String sku, int wanted, int left) {
    }

    public record StockOf(String sku) {
    }

    public record Restock(String sku, int quantity) {
    }

    public record Poison() {
    }
}
