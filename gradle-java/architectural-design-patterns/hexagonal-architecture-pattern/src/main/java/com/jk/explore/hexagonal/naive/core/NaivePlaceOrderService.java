package com.jk.explore.hexagonal.naive.core;

import com.jk.explore.hexagonal.adapter.payment.InMemoryPaymentGateway;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryProductCatalog;
import com.jk.explore.hexagonal.core.PlaceOrderRequest;
import com.jk.explore.hexagonal.core.PlaceOrderResult;
import com.jk.explore.hexagonal.core.domain.CheckoutRefusedException;
import com.jk.explore.hexagonal.core.domain.Order;
import com.jk.explore.hexagonal.core.domain.OrderLine;
import com.jk.explore.hexagonal.core.domain.Product;
import com.jk.explore.hexagonal.core.port.PaymentDeclinedException;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The naive version — the layered project's shape, honestly
 * reproduced.</strong> This class does exactly what {@code PlaceOrderService}
 * does, with one difference that matters: its fields are typed as the
 * concrete adapters, not as ports. {@code InMemoryOrderStore},
 * {@code InMemoryProductCatalog} and {@code InMemoryPaymentGateway} are all
 * named here directly, which means this class — the core's own use case —
 * reaches down into {@code adapter} to even compile.
 *
 * <p>It works. Every test in this project that exercises it passes. And to
 * write a unit test against it, you must construct three adapter classes
 * first, because there is no interface here narrow enough to fake. Swap the
 * storage strategy, and this class has to be edited — not because its logic
 * changed, but because its constructor named a concrete type that no longer
 * exists.
 */
public class NaivePlaceOrderService {

    private final InMemoryProductCatalog catalog;
    private final InMemoryOrderStore orders;
    private final InMemoryPaymentGateway payments;
    private int nextOrderNumber = 1001;

    public NaivePlaceOrderService(InMemoryProductCatalog catalog, InMemoryOrderStore orders,
                                  InMemoryPaymentGateway payments) {
        this.catalog = catalog;
        this.orders = orders;
        this.payments = payments;
    }

    public PlaceOrderResult place(PlaceOrderRequest request) {
        try {
            List<OrderLine> lines = new ArrayList<>();
            for (PlaceOrderRequest.RequestedLine requested : request.lines()) {
                Product product = catalog.find(requested.sku())
                        .orElseThrow(() -> new CheckoutRefusedException(
                                "no such product: " + requested.sku()));
                if (catalog.stockOf(requested.sku()) < requested.quantity()) {
                    throw new CheckoutRefusedException(
                            "only " + catalog.stockOf(requested.sku()) + " of "
                                    + requested.sku() + " left");
                }
                lines.add(OrderLine.of(product, requested.quantity()));
            }
            Order order = Order.placed("ord-" + nextOrderNumber++, request.customerId(), lines);

            payments.charge(order.customerId(), order.total());
            for (OrderLine line : order.lines()) {
                catalog.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);

            return PlaceOrderResult.placed(order.id(), order.total());
        } catch (CheckoutRefusedException refused) {
            return PlaceOrderResult.refused(refused.getMessage());
        } catch (PaymentDeclinedException declined) {
            return PlaceOrderResult.refused(declined.getMessage());
        }
    }
}
