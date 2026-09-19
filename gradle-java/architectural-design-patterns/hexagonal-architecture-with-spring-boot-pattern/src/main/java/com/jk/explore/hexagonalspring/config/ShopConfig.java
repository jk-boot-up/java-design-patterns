package com.jk.explore.hexagonalspring.config;

import com.jk.explore.hexagonalspring.core.PlaceOrderService;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import com.jk.explore.hexagonalspring.core.port.Payments;
import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import com.jk.explore.hexagonalspring.core.port.Warehouse;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** The one place the core meets the container: it is handed its adapters, and stays free of annotations. */
@Configuration
public class ShopConfig {

    @Bean
    PlaceOrder placeOrder(OrderStore orders, Warehouse warehouse, Payments payments) {
        return new PlaceOrderService(orders, warehouse, payments);
    }
}
