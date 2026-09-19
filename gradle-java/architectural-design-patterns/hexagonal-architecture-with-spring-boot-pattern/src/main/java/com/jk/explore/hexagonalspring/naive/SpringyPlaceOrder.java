package com.jk.explore.hexagonalspring.naive;

import com.jk.explore.hexagonalspring.core.Receipt;
import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import org.springframework.jdbc.core.simple.JdbcClient;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * The shortcut, kept for contrast and never scanned: a use case that would sit in the core and reaches
 * for the framework and the database directly. It works, and the core can no longer be built without Spring.
 */
@Service
public class SpringyPlaceOrder implements PlaceOrder {

    private final JdbcClient jdbc;

    public SpringyPlaceOrder(JdbcClient jdbc) {
        this.jdbc = jdbc;
    }

    @Override
    @Transactional
    public Receipt place(String customer, String sku, int quantity) {
        jdbc.sql("UPDATE stock SET on_hand = on_hand - ? WHERE sku = ?").param(quantity).param(sku).update();
        return new Receipt("ORD-X", 0);
    }
}
