package com.jk.explore.mvc.naive.view;

import com.jk.explore.mvc.domain.OrderLine;
import com.jk.explore.mvc.infrastructure.ProductTable;
import com.jk.explore.mvc.model.OrderSummaryModel;
import com.jk.explore.mvc.view.OrderSummaryView;

/**
 * <strong>The second naive version, and the one that matters.</strong>
 *
 * <p>The screen already exists and works. Somebody is then asked for a
 * confirmation email, and the model does not (yet) have a method for "unit
 * prices rounded to the nearest pound, for a cleaner-looking line" — so
 * rather than ask for one, this view reaches straight into
 * {@link ProductTable}, the catalogue, and rounds each unit price itself
 * before multiplying by quantity.
 *
 * <p>It compiles. It is not a hack, and a reviewer skimming the diff would
 * see a small, self-contained view doing its own formatting. And it prints a
 * different total from the screen — the burr grinder's eighty-nine pounds
 * fifty rounds to ninety before it is multiplied, and the fifty pence never
 * comes back. Nothing in the build objects, because reaching into the
 * catalogue is a perfectly ordinary import; only
 * {@code ArchitectureRuleCatchesTheShortcutTest}, which widens the dependency
 * rule to include this package, says so.
 */
public final class RoundedEmailView implements OrderSummaryView {

    private final ProductTable products;

    public RoundedEmailView(ProductTable products) {
        this.products = products;
    }

    @Override
    public String render(OrderSummaryModel model) {
        long total = 0;
        for (OrderLine line : model.lines()) {
            long unitPence = products.find(line.sku())
                    .orElseThrow()
                    .price()
                    .pence();
            long roundedUnitPence = Math.round(unitPence / 100.0) * 100;
            total += roundedUnitPence * line.quantity();
        }
        return "Thank you. Your order " + model.orderId() + " for "
                + formatted(total) + " is confirmed.";
    }

    private static String formatted(long pence) {
        return String.format("£%d.%02d", pence / 100, pence % 100);
    }
}
