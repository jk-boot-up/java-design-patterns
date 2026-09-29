package com.jk.explore.tdgjdbc;

import java.util.List;
import java.util.Map;
import org.springframework.jdbc.core.DataClassRowMapper;
import org.springframework.jdbc.core.namedparam.NamedParameterJdbcTemplate;
import org.springframework.stereotype.Repository;

/**
 * The pattern: every piece of SQL for the product table, in one class. JdbcTemplate opens and closes
 * connections, maps rows to records, and turns database errors into Spring's own exception types.
 */
@Repository
public class ProductGateway {

    private final NamedParameterJdbcTemplate jdbc;
    private final DataClassRowMapper<Row> rows = new DataClassRowMapper<>(Row.class);

    public ProductGateway(NamedParameterJdbcTemplate jdbc) {
        this.jdbc = jdbc;
    }

    public Row find(String sku) {
        return jdbc.queryForObject("SELECT sku, name, pence, quantity FROM product WHERE sku = :sku", Map.of("sku", sku), rows);
    }

    public int countOutOfStock() {
        return jdbc.queryForObject("SELECT count(*) FROM product WHERE quantity = 0", Map.of(), Integer.class);
    }

    public List<Row> cheaperThan(int pence) {
        return jdbc.query("SELECT sku, name, pence, quantity FROM product WHERE pence < :pence ORDER BY pence DESC",
                Map.of("pence", pence), rows);
    }

    public void insert(Row row) {
        jdbc.update("INSERT INTO product (sku, name, pence, quantity) VALUES (:sku, :name, :pence, :quantity)",
                Map.of("sku", row.sku(), "name", row.name(), "pence", row.pence(), "quantity", row.quantity()));
    }

    /** Takes one from stock in a single statement; returns false if there was none, never going below zero. */
    public boolean takeOne(String sku) {
        return jdbc.update("UPDATE product SET quantity = quantity - 1 WHERE sku = :sku AND quantity > 0",
                Map.of("sku", sku)) == 1;
    }
}
