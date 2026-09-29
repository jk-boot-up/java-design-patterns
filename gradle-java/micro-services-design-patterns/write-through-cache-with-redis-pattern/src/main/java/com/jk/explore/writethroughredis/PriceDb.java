package com.jk.explore.writethroughredis;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.Statement;

/**
 * The prices table in PostgreSQL: the record of truth.
 */
public final class PriceDb {

    private final Infra infra;
    private int reads;

    public PriceDb(Infra infra) throws Exception {
        this.infra = infra;
        try (Connection c = infra.database(); Statement s = c.createStatement()) {
            s.execute("CREATE TABLE IF NOT EXISTS prices (sku TEXT PRIMARY KEY, pence INT NOT NULL)");
        }
    }

    public void write(String sku, int pence, boolean readOnly) throws Exception {
        try (Connection c = infra.database()) {
            if (readOnly) {
                try (Statement s = c.createStatement()) {
                    s.execute("SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY");
                }
            }
            try (PreparedStatement p = c.prepareStatement(
                    "INSERT INTO prices VALUES (?, ?) ON CONFLICT (sku) DO UPDATE SET pence = EXCLUDED.pence")) {
                p.setString(1, sku);
                p.setInt(2, pence);
                p.executeUpdate();
            }
        }
    }

    public int read(String sku) throws Exception {
        reads++;
        try (Connection c = infra.database(); PreparedStatement p = c.prepareStatement("SELECT pence FROM prices WHERE sku = ?")) {
            p.setString(1, sku);
            try (ResultSet r = p.executeQuery()) {
                return r.next() ? r.getInt(1) : -1;
            }
        }
    }

    public int reads() {
        return reads;
    }
}
