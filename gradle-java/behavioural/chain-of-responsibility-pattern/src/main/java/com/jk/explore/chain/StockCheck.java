package com.jk.explore.chain;

import java.util.Map;
import java.util.Optional;

/** Can the warehouse actually pick every line? */
public final class StockCheck extends ScreeningHandler {

    private final Map<String, Integer> onShelf;

    /** @param onShelf how many of each SKU the warehouse has */
    public StockCheck(Map<String, Integer> onShelf) {
        this.onShelf = Map.copyOf(onShelf);
    }

    @Override
    public String name() {
        return "stock";
    }

    @Override
    protected Optional<Decision> check(CheckoutRequest request) {
        for (BasketItem item : request.items()) {
            int available = onShelf.getOrDefault(item.sku(), 0);
            if (available < item.quantity()) {
                return Optional.of(Decision.rejected(name(),
                        item.description() + ": " + item.quantity() + " wanted, "
                                + available + " on the shelf"));
            }
        }
        return Optional.empty();
    }
}
