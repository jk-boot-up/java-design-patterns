package com.jk.explore.actorpattern;

import java.util.HashMap;
import java.util.Map;

/** Owns the stock. Nobody else can read or change the map: they send messages, and the actor decides. */
public class InventoryActor extends Actor {

    private final Map<String, Integer> initial;
    private Map<String, Integer> stock;

    public InventoryActor(Map<String, Integer> initial) {
        super("inventory");
        this.initial = Map.copyOf(initial);
        this.stock = new HashMap<>(initial);
    }

    @Override
    protected Object receive(Object message) {
        if (message instanceof Messages.Reserve r) {
            int left = stock.getOrDefault(r.sku(), 0);
            if (left < r.quantity()) {
                return new Messages.OutOfStock(r.sku(), r.quantity(), left);
            }
            stock.put(r.sku(), left - r.quantity());
            return new Messages.Reserved(r.sku(), r.quantity());
        }
        if (message instanceof Messages.Restock r) {
            stock.merge(r.sku(), r.quantity(), Integer::sum);
            return null;
        }
        if (message instanceof Messages.StockOf q) {
            return stock.getOrDefault(q.sku(), 0);
        }
        if (message instanceof Messages.Poison) {
            throw new IllegalStateException("a message this actor cannot handle");
        }
        throw new IllegalArgumentException("unknown message " + message);
    }

    @Override
    protected void restart() {
        stock = new HashMap<>(initial);
    }
}
