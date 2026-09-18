package com.jk.explore.cleanspring.config;

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
 * <strong>The one bean removed on purpose, for the video's most valuable
 * twenty seconds.</strong> Identical to {@link AppConfig}, with the
 * {@code @Bean} method for {@link NotificationGateway} deleted. Nothing here
 * fails to compile — every remaining line is ordinary, valid Java, and
 * {@code javac} has no opinion about whether a bean exists at runtime.
 *
 * <p>The failure surfaces only when {@link com.jk.explore.cleanspring.Application}
 * asks a context built from this class for a
 * {@code PlaceOrderInputBoundary}, and Spring cannot find anything to put in
 * its fourth constructor parameter. Compare this with deleting the
 * equivalent argument from {@code clean-architecture-pattern}'s hand-wired
 * {@code new PlaceOrderInteractor(...)} call: that fails in your editor,
 * before you have even saved the file. This fails after the JVM has started,
 * after logging has initialised, seconds into what looked like a normal run.
 */
@Configuration
public class BrokenAppConfig {

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

    // No @Bean for NotificationGateway. This is the whole of the mistake.

    @Bean
    public PlaceOrderInputBoundary placeOrderInputBoundary(ProductRepository products,
            OrderRepository orders, PaymentGateway payments, NotificationGateway notifications) {
        return new PlaceOrderInteractor(products, orders, payments, notifications);
    }
}
