package com.jk.explore.cleanspring.config;

import com.jk.explore.cleanspring.adapters.controller.BatchOrderController;
import com.jk.explore.cleanspring.adapters.controller.CheckoutController;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.cleanspring.usecases.NotificationGateway;
import com.jk.explore.cleanspring.usecases.OrderRepository;
import com.jk.explore.cleanspring.usecases.PaymentGateway;
import com.jk.explore.cleanspring.usecases.PlaceOrderInputBoundary;
import com.jk.explore.cleanspring.usecases.PlaceOrderInteractor;
import com.jk.explore.cleanspring.usecases.ProductRepository;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * <strong>This class is §66's composition root, said with annotations
 * instead of {@code new}.</strong> Read it next to
 * {@code clean-architecture-pattern}'s {@code PlaceAnOrderDemo.shop()}. Same
 * four gateways, same interactor, same four constructor arguments — the
 * difference is who calls the constructors. There, a Java method did, by
 * hand, when the demo ran. Here, Spring does, once, when the context starts,
 * by reading this file and matching parameter types to bean methods.
 *
 * <p>Not one class in {@code entities}, {@code usecases} or {@code adapters}
 * carries a Spring annotation. Every one of those forty-odd files is
 * byte-for-byte the file the hand-wired project already built and tested.
 * The only new code in this whole project is this configuration and the
 * class below it, {@link com.jk.explore.cleanspring.Application} — the
 * outermost circle, exactly where Clean Architecture said a framework
 * belongs.
 */
@Configuration
public class AppConfig {

    @Bean
    public ProductRepository productRepository() {
        return InMemoryProductRepository.seeded();
    }

    @Bean
    public OrderRepository orderRepository() {
        return new InMemoryOrderRepository();
    }

    @Bean
    public PaymentGateway paymentGateway() {
        return InMemoryPaymentGateway.working();
    }

    @Bean
    public NotificationGateway notificationGateway() {
        return new InMemoryNotificationGateway();
    }

    @Bean
    public PlaceOrderInputBoundary placeOrderInputBoundary(ProductRepository products,
            OrderRepository orders, PaymentGateway payments, NotificationGateway notifications) {
        return new PlaceOrderInteractor(products, orders, payments, notifications);
    }

    @Bean
    public CheckoutController checkoutController(PlaceOrderInputBoundary placeOrder) {
        return new CheckoutController(placeOrder);
    }

    @Bean
    public BatchOrderController batchOrderController(PlaceOrderInputBoundary placeOrder) {
        return new BatchOrderController(placeOrder);
    }
}
