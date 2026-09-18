package com.jk.explore.mvc.application;

import com.jk.explore.mvc.domain.CheckoutRefusedException;
import com.jk.explore.mvc.domain.Order;
import com.jk.explore.mvc.domain.OrderLine;
import com.jk.explore.mvc.domain.Product;
import com.jk.explore.mvc.infrastructure.CardNetwork;
import com.jk.explore.mvc.infrastructure.OrderTable;
import com.jk.explore.mvc.infrastructure.PaymentDeclinedException;
import com.jk.explore.mvc.infrastructure.ProductTable;

import java.util.ArrayList;
import java.util.List;

/**
 * Places the order. Check, charge, reduce, store — the same four steps every
 * project in this category performs, and in the same order: the card is
 * charged before anything is written down, so a decline leaves nothing
 * behind to undo.
 *
 * <p>Notice what this class does <em>not</em> do: it does not render a
 * screen, and it does not send an email. Sending the confirmation is a
 * rendering decision — what the confirmation says, and in which format — and
 * this MVC category's whole argument is that rendering decisions belong to a
 * View, not to the use case. {@link com.jk.explore.mvc.controller.OrderSummaryController}
 * is what turns a successful placement into something a customer sees.
 */
public class PlaceOrderService {

    private final ProductTable products;
    private final OrderTable orders;
    private final CardNetwork cards;
    private int nextOrderNumber = 1001;

    public PlaceOrderService(ProductTable products, OrderTable orders, CardNetwork cards) {
        this.products = products;
        this.orders = orders;
        this.cards = cards;
    }

    public PlaceOrderResult place(PlaceOrderRequest request) {
        try {
            List<OrderLine> lines = priceEveryLine(request);
            Order order = Order.placed(nextId(), request.customerId(), lines);

            cards.charge(order.customerId(), order.total());

            for (OrderLine line : order.lines()) {
                products.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);

            return PlaceOrderResult.placed(order.id(), order.total());
        } catch (CheckoutRefusedException refused) {
            return PlaceOrderResult.refused(refused.getMessage());
        } catch (PaymentDeclinedException declined) {
            return PlaceOrderResult.refused(declined.getMessage());
        }
    }

    private List<OrderLine> priceEveryLine(PlaceOrderRequest request) {
        List<OrderLine> lines = new ArrayList<>();
        for (PlaceOrderRequest.RequestedLine requested : request.lines()) {
            Product product = products.find(requested.sku())
                    .orElseThrow(() -> new CheckoutRefusedException(
                            "no such product: " + requested.sku()));
            int available = products.stockOf(requested.sku());
            if (available < requested.quantity()) {
                throw new CheckoutRefusedException(
                        "only " + available + " of " + requested.sku() + " left");
            }
            lines.add(OrderLine.of(product, requested.quantity()));
        }
        return lines;
    }

    private String nextId() {
        return "ord-" + nextOrderNumber++;
    }
}
