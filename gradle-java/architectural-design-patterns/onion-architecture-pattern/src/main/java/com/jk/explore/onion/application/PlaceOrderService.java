package com.jk.explore.onion.application;

import com.jk.explore.onion.domain.model.Order;
import com.jk.explore.onion.domain.model.OrderLine;
import com.jk.explore.onion.domain.model.OrderRepository;
import com.jk.explore.onion.domain.service.PricingService;
import java.util.List;

/** A use case. It arranges the inner rings and gives them a job. It holds no rules of its own. */
public class PlaceOrderService {

    private final OrderRepository repository;
    private final PricingService pricing;

    public PlaceOrderService(OrderRepository repository, PricingService pricing) {
        this.repository = repository;
        this.pricing = pricing;
    }

    public Order place(String id, List<OrderLine> lines) {
        Order order = new Order(id, lines);
        pricing.price(order);
        repository.save(order);
        return order;
    }
}
