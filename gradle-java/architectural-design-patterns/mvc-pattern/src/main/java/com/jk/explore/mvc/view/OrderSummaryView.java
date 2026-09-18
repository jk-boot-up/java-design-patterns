package com.jk.explore.mvc.view;

import com.jk.explore.mvc.model.OrderSummaryModel;

/**
 * A view's one job: turn a {@link OrderSummaryModel} into text. Nothing here
 * adds up a price, checks stock, or talks to a card network — every number a
 * view prints comes from asking the model for it.
 *
 * <p><strong>What this interface must never grow.</strong> No method here
 * accepts a {@code Product} or a raw price. The moment a view can be handed
 * anything other than the finished model, it can start recomputing a total
 * for itself — which is exactly the shortcut this project's naive package
 * demonstrates, and exactly what {@code ArchitectureTest} exists to catch.
 */
public interface OrderSummaryView {

    String render(OrderSummaryModel model);
}
