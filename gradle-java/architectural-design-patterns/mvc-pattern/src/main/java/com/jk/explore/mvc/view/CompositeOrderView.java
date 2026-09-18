package com.jk.explore.mvc.view;

import com.jk.explore.mvc.model.OrderSummaryModel;

import java.util.List;
import java.util.stream.Collectors;

/**
 * Several views, rendered together as one — the same interface as any single
 * view, which is what lets the controller treat "print the screen and the
 * email" and "print just the screen" identically. Adding a third view later
 * means constructing this list one element longer; nothing that calls a
 * {@link OrderSummaryView} has to change.
 */
public final class CompositeOrderView implements OrderSummaryView {

    private final List<OrderSummaryView> views;

    public CompositeOrderView(List<OrderSummaryView> views) {
        this.views = List.copyOf(views);
    }

    @Override
    public String render(OrderSummaryModel model) {
        return views.stream()
                .map(view -> view.render(model))
                .collect(Collectors.joining("\n---\n"));
    }
}
