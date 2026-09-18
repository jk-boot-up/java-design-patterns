package com.jk.explore.cleanspring.naive.usecases;

import com.jk.explore.cleanspring.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.cleanspring.entities.CheckoutRefusedException;
import com.jk.explore.cleanspring.entities.Order;
import com.jk.explore.cleanspring.entities.OrderLine;
import com.jk.explore.cleanspring.entities.Product;
import com.jk.explore.cleanspring.usecases.PaymentDeclinedException;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput;
import com.jk.explore.cleanspring.usecases.PlaceOrderOutput;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>The naive version — a use case whose fields are gateways, not
 * boundaries.</strong> Same four steps, same outcome. The difference is in
 * the constructor: it takes {@code InMemoryOrderRepository},
 * {@code InMemoryProductRepository} and {@code InMemoryPaymentGateway}
 * directly, all three defined two circles further out. This class — which
 * calls itself a use case — reaches straight through the interface-adapters
 * circle it is supposed to be inside of.
 */
public class NaivePlaceOrderInteractor {

    private final InMemoryProductRepository products;
    private final InMemoryOrderRepository orders;
    private final InMemoryPaymentGateway payments;
    private int nextOrderNumber = 1001;

    public NaivePlaceOrderInteractor(InMemoryProductRepository products,
                                     InMemoryOrderRepository orders,
                                     InMemoryPaymentGateway payments) {
        this.products = products;
        this.orders = orders;
        this.payments = payments;
    }

    public PlaceOrderOutput execute(PlaceOrderInput input) {
        try {
            List<OrderLine> lines = new ArrayList<>();
            for (PlaceOrderInput.RequestedLine requested : input.lines()) {
                Product product = products.find(requested.sku())
                        .orElseThrow(() -> new CheckoutRefusedException(
                                "no such product: " + requested.sku()));
                if (products.stockOf(requested.sku()) < requested.quantity()) {
                    throw new CheckoutRefusedException(
                            "only " + products.stockOf(requested.sku()) + " of "
                                    + requested.sku() + " left");
                }
                lines.add(OrderLine.of(product, requested.quantity()));
            }
            Order order = Order.placed("ord-" + nextOrderNumber++, input.customerId(), lines);

            payments.charge(order.customerId(), order.total());
            for (OrderLine line : order.lines()) {
                products.reduceStock(line.sku(), line.quantity());
            }
            orders.save(order);

            return PlaceOrderOutput.placed(order.id(), order.total());
        } catch (CheckoutRefusedException refused) {
            return PlaceOrderOutput.refused(refused.getMessage());
        } catch (PaymentDeclinedException declined) {
            return PlaceOrderOutput.refused(declined.getMessage());
        }
    }
}
