package com.jk.explore.cqrs;

/**
 * Something that has happened in the shop, stated as a fact.
 *
 * Events are past tense on purpose. {@code OrderPlaced} is not an instruction to place
 * an order — the order is already placed, the money is already taken, and nobody
 * receiving this event may refuse it. A read model's job is to believe events, not to
 * argue with them.
 *
 * <p>The three kinds here are the three things the order history page cares about, and
 * that is the only reason there are three. A read model subscribes to exactly the events
 * it needs to answer its own question and ignores the rest of the shop entirely.
 */
public sealed interface ShopEvent {

    /** A customer has placed an order. Carries everything the write side knew. */
    record OrderPlaced(Order order) implements ShopEvent {
    }

    /** The catalog team has renamed a product. */
    record ProductRenamed(String sku, String newName) implements ShopEvent {
    }

    /** The number of a product on the shelf has changed. */
    record StockChanged(String sku, int nowAvailable) implements ShopEvent {
    }
}
