package com.jk.explore.idempotentconsumerkafka;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/** Remembers nothing. Every order it is handed gets a confirmation email, however often it arrives. */
public class JustSend implements Handler {

    private final Database database;

    public JustSend(Database database) {
        this.database = database;
    }

    @Override
    public boolean handle(OrderPlaced order) {
        try (Connection c = database.connect()) {
            queueConfirmation(c, order);
            return true;
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /** Writes one row to the confirmations table: one email waiting to be sent. */
    static void queueConfirmation(Connection c, OrderPlaced order) throws SQLException {
        try (PreparedStatement s = c.prepareStatement("insert into confirmations (order_id, body) values (?, ?)")) {
            s.setString(1, order.orderId());
            s.setString(2, order.confirmation());
            s.executeUpdate();
        }
    }
}
