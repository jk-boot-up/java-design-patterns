package com.jk.explore.offloadgateway;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;

/**
 * The gateway: one route per service. The chores live in {@link SignInFilter} and in Reactor Netty's
 * response compression, switched on by properties.
 */
@SpringBootApplication
public class GatewayApp {

    @Bean
    RouteLocator routes(RouteLocatorBuilder builder,
                        @Value("${shop.catalog}") String catalog,
                        @Value("${shop.cart}") String cart,
                        @Value("${shop.orders}") String orders) {
        return builder.routes()
                .route("catalog", r -> r.path("/catalog/**").uri(catalog))
                .route("cart", r -> r.path("/cart/**").uri(cart))
                .route("orders", r -> r.path("/orders/**").uri(orders))
                .build();
    }
}
