package com.jk.explore.tabledatagateway;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.sql.Connection;
import java.sql.SQLException;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class ProductGatewayTest {

    private Connection c;
    private ProductGateway g;

    @BeforeEach
    void open() throws SQLException {
        c = Database.open("test-" + System.nanoTime());
        g = new ProductGateway(c);
    }

    @AfterEach
    void close() throws SQLException {
        c.close();
    }

    @Test
    void findsARow() {
        assertEquals(new ProductGateway.Row("MUG-1", "mug", 800, 20), g.findBySku("MUG-1").orElseThrow());
    }

    @Test
    void unknownSkuIsEmpty() {
        assertTrue(g.findBySku("NOPE").isEmpty());
    }

    @Test
    void cheaperThanIsSortedByPrice() {
        assertEquals(List.of("tea towel", "mug"), g.cheaperThan(1000).stream().map(ProductGateway.Row::name).toList());
    }

    @Test
    void takeStockReducesIt() {
        g.takeStock("MUG-1", 5);
        assertEquals(15, g.findBySku("MUG-1").orElseThrow().stock());
    }

    @Test
    void worksAfterTheRenameWhenToldTheNewName() throws SQLException {
        Database.renameStockColumn(c);
        assertEquals(1, new ProductGateway(c, "quantity").countOutOfStock());
    }
}
