package com.jk.explore.hexagonal.core;

import com.jk.explore.hexagonal.core.domain.CheckoutRefusedException;
import com.jk.explore.hexagonal.core.domain.Order;
import com.jk.explore.hexagonal.core.domain.OrderLine;
import com.jk.explore.hexagonal.core.domain.Product;
import com.jk.explore.hexagonal.core.port.Notifier;
import com.jk.explore.hexagonal.core.port.OrderStore;
import com.jk.explore.hexagonal.core.port.PaymentDeclinedException;
import com.jk.explore.hexagonal.core.port.PaymentGateway;
import com.jk.explore.hexagonal.core.port.ProductCatalog;

import java.util.ArrayList;
import java.util.List;

/**
 * The whole application, from the core's point of view: check, charge,
 * reduce, store. Notice what it imports — {@code core.domain} and
 * {@code core.port}, and nothing else. Not one class from {@code adapter}
 * appears anywhere in this file, in either direction, and
 * {@code ArchitectureTest} exists to keep it that way permanently rather
 * than until the next deadline.
 *
 * <p>This is the same four-step sequence the layered-architecture project
 * runs, for a reason: the feature has not changed, only the direction its
 * dependencies point in has. Where that project's use case named
 * {@code OrderTable}, {@code CardNetwork} and {@code EmailServer} — all
 * three defined in its bottom layer — this one names {@code OrderStore},
 * {@code PaymentGateway} and {@code Notifier}, all three defined right here,
 * in the core. An adapter outside reaches up to implement them; nothing in
 * here reaches down.
 */
public class PlaceOrderService {

    private final ProductCatalog catalog;
    private final OrderStore orders;
    private final PaymentGateway payments;
    private final Notifier notifier;
    private int nextOrderNumber = 1001;

    public PlaceOrderService(ProductCatalog catalog, OrderStore orders,
                             PaymentGateway payments, Notifier notifier) {
        this.catalog = catalog;
        this.orders = orders;
        this.payments = payments;
        this.notifier = notifier;
    }

    public PlaceOrderResult place(PlaceOrderRequest request, String customerContact) {
        try {
            List<OrderLine> lines = priceEveryLine(request);
            Order order = Order.placed(nextId(), request.customerId(), lines);

            payments.charge(order.customerId(), order.total());

            for (OrderLine line : order.lines()) {
                catalog.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);
            notifier.send(customerContact, confirmationFor(order));

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
            Product product = catalog.find(requested.sku())
                    .orElseThrow(() -> new CheckoutRefusedException(
                            "no such product: " + requested.sku()));
            int available = catalog.stockOf(requested.sku());
            if (available < requested.quantity()) {
                throw new CheckoutRefusedException(
                        "only " + available + " of " + requested.sku() + " left");
            }
            lines.add(OrderLine.of(product, requested.quantity()));
        }
        return lines;
    }

    private String confirmationFor(Order order) {
        return "Thank you. Your order " + order.id() + " for " + order.total()
                + " is confirmed.";
    }

    private String nextId() {
        return "ord-" + nextOrderNumber++;
    }
}
