package com.jk.explore.layeredspring.application;

import com.jk.explore.layeredspring.domain.CheckoutRefused;
import com.jk.explore.layeredspring.domain.Order;
import com.jk.explore.layeredspring.infrastructure.CardNetwork;
import com.jk.explore.layeredspring.infrastructure.OrderRepository;
import com.jk.explore.layeredspring.infrastructure.PaymentDeclined;
import com.jk.explore.layeredspring.infrastructure.ProductRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.atomic.AtomicInteger;

/** The use case. One transaction covers reserving stock, charging the card and saving the order. */
@Service
public class PlaceOrderService {

    private final ProductRepository products;
    private final OrderRepository orders;
    private final CardNetwork cards;
    private final AtomicInteger sequence = new AtomicInteger();

    public PlaceOrderService(ProductRepository products, OrderRepository orders, CardNetwork cards) {
        this.products = products;
        this.orders = orders;
        this.cards = cards;
    }

    @Transactional
    public PlaceOrderResult place(PlaceOrderRequest request) {
        if (!products.reserve(request.sku(), request.quantity())) {
            throw new CheckoutRefused(CheckoutRefused.Reason.OUT_OF_STOCK, "not enough " + request.sku() + " in stock");
        }
        long total = products.priceOf(request.sku()) * request.quantity();
        try {
            cards.charge(total);
        } catch (PaymentDeclined declined) {
            throw new CheckoutRefused(CheckoutRefused.Reason.PAYMENT_DECLINED, declined.getMessage());
        }
        String id = "ORD-" + String.format("%06d", sequence.incrementAndGet());
        orders.save(new Order(id, request.customer(), request.sku(), request.quantity(), total,
                products.costOf(request.sku()) * request.quantity(), "PAID"));
        return new PlaceOrderResult(id, total, "PAID");
    }
}
