package com.jk.explore.apigatewaysc;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * The gateway's routing table: one public prefix per internal service. The prefix is stripped
 * before the request is forwarded, and every forwarded request carries a source header.
 */
@Configuration
public class GatewayRoutes {

    @Bean
    RouteLocator routes(RouteLocatorBuilder builder,
                        @Value("${backend.catalogue.port}") int catalogue,
                        @Value("${backend.pricing.port}") int pricing,
                        @Value("${backend.inventory.port}") int inventory,
                        @Value("${backend.recommendations.port}") int recommendations) {
        return builder.routes()
                .route("catalogue", r -> r.path("/api/catalogue/**")
                        .filters(f -> f.stripPrefix(2).addRequestHeader("X-Request-Source", "gateway"))
                        .uri("http://127.0.0.1:" + catalogue))
                .route("pricing", r -> r.path("/api/pricing/**")
                        .filters(f -> f.stripPrefix(2).addRequestHeader("X-Request-Source", "gateway"))
                        .uri("http://127.0.0.1:" + pricing))
                .route("inventory", r -> r.path("/api/inventory/**")
                        .filters(f -> f.stripPrefix(2).addRequestHeader("X-Request-Source", "gateway"))
                        .uri("http://127.0.0.1:" + inventory))
                .route("recommendations", r -> r.path("/api/recommendations/**")
                        .filters(f -> f.stripPrefix(2).addRequestHeader("X-Request-Source", "gateway"))
                        .uri("http://127.0.0.1:" + recommendations))
                .build();
    }
}
