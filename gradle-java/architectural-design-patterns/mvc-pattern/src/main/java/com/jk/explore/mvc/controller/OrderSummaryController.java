package com.jk.explore.mvc.controller;

import com.jk.explore.mvc.application.PlaceOrderRequest;
import com.jk.explore.mvc.application.PlaceOrderResult;
import com.jk.explore.mvc.application.PlaceOrderService;
import com.jk.explore.mvc.domain.Order;
import com.jk.explore.mvc.infrastructure.EmailServer;
import com.jk.explore.mvc.infrastructure.OrderTable;
import com.jk.explore.mvc.model.OrderSummaryModel;
import com.jk.explore.mvc.view.OrderSummaryView;

/**
 * Turns a checkout request into calls: the use case first, then a model, then
 * a view. This is what a controller is once the annotations are stripped off
 * — one method, three steps, in order.
 *
 * <p>This class is also where classic MVC's observation is deliberately
 * simplified for this teaching project. A textbook Smalltalk controller
 * updates the model and lets the model notify views that have subscribed to
 * it; here the controller builds the model once and hands it directly to
 * whichever views the caller wants rendered, because a synchronous console
 * demo has no independent redraw to trigger. The relationship the video and
 * the written notes draw is the same one either way: <strong>the view never
 * initiates a fetch, and never sees anything but the finished model.</strong>
 */
public final class OrderSummaryController {

    private final PlaceOrderService placeOrder;
    private final OrderTable orders;
    private final EmailServer email;

    public OrderSummaryController(PlaceOrderService placeOrder, OrderTable orders,
                                  EmailServer email) {
        this.placeOrder = placeOrder;
        this.orders = orders;
        this.email = email;
    }

    /**
     * Places the order and renders it with the given views, mailing the text
     * {@code emailView} produces (if one is supplied). Returns the rendered
     * text of {@code screen}, which is what the caller treats as "the
     * screen".
     *
     * <p>The model is built by reading the order back from storage rather
     * than from anything the request carried, so it reflects exactly what
     * was saved — not what was asked for.
     */
    public CheckoutOutcome checkout(PlaceOrderRequest request, String customerEmail,
                                    OrderSummaryView screen, OrderSummaryView emailView) {
        PlaceOrderResult result = placeOrder.place(request);
        if (!result.placed()) {
            return CheckoutOutcome.refused(result.reason());
        }

        Order placed = orders.find(result.orderId())
                .orElseThrow(() -> new IllegalStateException(
                        "placed order " + result.orderId() + " was not found in storage"));
        OrderSummaryModel model = OrderSummaryModel.of(placed);

        String screenText = screen.render(model);
        if (emailView != null) {
            email.send(customerEmail, emailView.render(model));
        }
        return CheckoutOutcome.rendered(screenText, model);
    }

    public record CheckoutOutcome(boolean placed, String screenText,
                                  OrderSummaryModel model, String reason) {

        static CheckoutOutcome rendered(String screenText, OrderSummaryModel model) {
            return new CheckoutOutcome(true, screenText, model, null);
        }

        static CheckoutOutcome refused(String reason) {
            return new CheckoutOutcome(false, null, null, reason);
        }
    }
}
