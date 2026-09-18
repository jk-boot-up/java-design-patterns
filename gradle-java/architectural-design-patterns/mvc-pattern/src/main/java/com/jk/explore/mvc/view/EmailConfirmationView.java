package com.jk.explore.mvc.view;

import com.jk.explore.mvc.model.OrderSummaryModel;

/**
 * <strong>The forced change.</strong> A second view, added over the model
 * {@link ScreenSummaryView} already renders, written and added without
 * touching the model, the controller, or the screen at all.
 *
 * <p>Read {@link #render} and notice what is missing: no multiplication, no
 * addition, no rounding. The total it prints is {@code model.total()},
 * character for character the same value the screen prints, because it is
 * literally the same call. Two views cannot disagree about a number neither
 * of them is allowed to calculate.
 */
public final class EmailConfirmationView implements OrderSummaryView {

    @Override
    public String render(OrderSummaryModel model) {
        return "Thank you. Your order " + model.orderId() + " for "
                + model.total() + " is confirmed.";
    }
}
