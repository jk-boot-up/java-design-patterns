package com.jk.explore.hikaripool;

import com.zaxxer.hikari.HikariDataSource;
import org.junit.jupiter.api.Test;

import java.sql.Connection;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.SQLTransientConnectionException;
import java.sql.Statement;
import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** No test asserts a timing. Counts and states only. */
class HikariPoolTest {

    @Test
    void tenSequentialPaymentsThroughAPoolOfTwoOpenOnlyWhatDemandNeeds() {
        try (HikariDataSource ds = Payments.pool(2, 1_000)) {
            for (int i = 0; i < 10; i++) {
                Payments.pay(ds, "c" + i, 100);
            }
            assertEquals(10, Payments.count(ds));
            assertEquals(1, ds.getHikariPoolMXBean().getTotalConnections());
            assertEquals(0, ds.getHikariPoolMXBean().getActiveConnections());
        }
    }

    @Test
    void closingAPooledConnectionGivesItBackRatherThanClosingIt() throws SQLException {
        try (HikariDataSource ds = Payments.pool(1, 1_000)) {
            Connection c = ds.getConnection();
            assertEquals(1, ds.getHikariPoolMXBean().getActiveConnections());
            c.close();
            assertEquals(0, ds.getHikariPoolMXBean().getActiveConnections());
            assertEquals(1, ds.getHikariPoolMXBean().getIdleConnections());
        }
    }

    @Test
    void theJdbcStateThePoolKnowsAboutIsResetOnReturn() throws SQLException {
        try (HikariDataSource ds = Payments.pool(1, 1_000)) {
            try (Connection first = ds.getConnection()) {
                first.setAutoCommit(false);
                first.setReadOnly(true);
            }
            try (Connection second = ds.getConnection()) {
                assertTrue(second.getAutoCommit());
                assertFalse(second.isReadOnly());
            }
        }
    }

    @Test
    void stateThePoolCannotSeeLeaksToTheNextBorrower() throws SQLException {
        try (HikariDataSource ds = Payments.pool(1, 1_000)) {
            try (Connection a = ds.getConnection(); Statement s = a.createStatement()) {
                s.execute("set @card_holder = 'Ada Lovelace'");
            }
            try (Connection b = ds.getConnection(); Statement s = b.createStatement(); ResultSet rs = s.executeQuery("select @card_holder")) {
                rs.next();
                assertEquals("Ada Lovelace", rs.getString(1));
            }
        }
    }

    @Test
    void anExhaustedPoolTimesOutWithAReadableMessageBecauseATimeoutIsAlreadyConfigured() throws SQLException {
        try (HikariDataSource ds = Payments.pool(2, 300)) {
            List<Connection> leaked = new ArrayList<>();
            leaked.add(ds.getConnection());
            leaked.add(ds.getConnection());
            SQLTransientConnectionException e = assertThrows(SQLTransientConnectionException.class, ds::getConnection);
            assertTrue(e.getMessage().contains("total=2, active=2, idle=0"), e.getMessage());
            for (Connection c : leaked) {
                c.close();
            }
        }
    }

    @Test
    void aWarmPoolOfFiftyOpensFiftyConnectionsWhateverIsUsed() {
        try (HikariDataSource ds = Payments.pool(50, 5_000, true)) {
            Payments.awaitFilled(ds, 50);
            assertEquals(50, ds.getHikariPoolMXBean().getTotalConnections());
            assertEquals(50, ds.getHikariPoolMXBean().getIdleConnections());
        }
    }
}
