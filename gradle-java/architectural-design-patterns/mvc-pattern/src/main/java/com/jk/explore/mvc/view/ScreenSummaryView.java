package com.jk.explore.mvc.view;

import com.jk.explore.mvc.domain.OrderLine;
import com.jk.explore.mvc.model.OrderSummaryModel;

/**
 * The order-confirmation screen a customer sees immediately after checkout.
 * Every figure on it — the line count, the total — is read from the model,
 * never recomputed.
 */
public final class ScreenSummaryView implements OrderSummaryView {

    @Override
    public String render(OrderSummaryModel model) {
        StringBuilder out = new StringBuilder();
        out.append("Order ").append(model.orderId()).append(" placed.\n");
        for (OrderLine line : model.lines()) {
            out.append("  ").append(line.quantity()).append(" x ").append(line.sku())
                    .append("  ").append(line.lineTotal()).append("\n");
        }
        out.append("  Total: ").append(model.total());
        return out.toString();
    }
}
