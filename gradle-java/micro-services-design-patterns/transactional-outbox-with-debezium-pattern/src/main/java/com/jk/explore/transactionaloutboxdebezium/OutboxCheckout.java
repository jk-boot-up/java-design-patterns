package com.jk.explore.transactionaloutboxdebezium;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * The pattern. The checkout writes the order and an outbox row describing the event in one
 * Postgres transaction, and that is all it does. There is no Kafka code in this class: it
 * never opens a connection to the broker. Debezium, reading Postgres's log, does the sending.
 */
public class OutboxCheckout {

    private final OrdersDatabase database;
    private final boolean deleteRowInSameTransaction;

    /**
     * @param deleteRowInSameTransaction when true, the outbox row is deleted again before the
     *        commit. The table stays empty, and the insert is still in the log for Debezium.
     */
    public OutboxCheckout(OrdersDatabase database, boolean deleteRowInSameTransaction) {
        this.database = database;
        this.deleteRowInSameTransaction = deleteRowInSameTransaction;
    }

    public OutboxCheckout(OrdersDatabase database) {
        this(database, false);
    }

    /** The id of an event, made from the order and what happened to it; it never changes when the event is sent again. */
    public static String eventId(String orderId, String type) {
        return orderId + "/" + type;
    }

    /** Saves the order and its OrderPlaced event in one transaction. */
    public void place(Order order) {
        inOneTransaction(c -> {
            try (PreparedStatement s = c.prepareStatement("insert into orders values (?, ?, ?, 'placed')")) {
                s.setString(1, order.orderId());
                s.setString(2, order.customer());
                s.setLong(3, order.totalPence());
                s.executeUpdate();
            }
            writeEvent(c, order.orderId(), "OrderPlaced", order.asJson());
        }, true);
    }

    /**
     * Writes the order and its event exactly as {@link #place} does, then the card is
     * declined and the whole transaction is rolled back.
     */
    public void placeButCardDeclined(Order order) {
        inOneTransaction(c -> {
            try (PreparedStatement s = c.prepareStatement("insert into orders values (?, ?, ?, 'placed')")) {
                s.setString(1, order.orderId());
                s.setString(2, order.customer());
                s.setLong(3, order.totalPence());
                s.executeUpdate();
            }
            writeEvent(c, order.orderId(), "OrderPlaced", order.asJson());
        }, false);
    }

    /** Moves the order on to a new status, paid or shipped, with its event, in one transaction. */
    public void moveOn(String orderId, String status, String type) {
        inOneTransaction(c -> {
            try (PreparedStatement s = c.prepareStatement("update orders set status = ? where order_id = ?")) {
                s.setString(1, status);
                s.setString(2, orderId);
                s.executeUpdate();
            }
            writeEvent(c, orderId, type, "{\"orderId\":\"" + orderId + "\",\"status\":\"" + status + "\"}");
        }, true);
    }

    private void writeEvent(Connection c, String orderId, String type, String payload) throws SQLException {
        String id = eventId(orderId, type);
        try (PreparedStatement s = c.prepareStatement("insert into outbox values (?, 'order', ?, ?, ?)")) {
            s.setString(1, id);
            s.setString(2, orderId);
            s.setString(3, type);
            s.setString(4, payload);
            s.executeUpdate();
        }
        if (deleteRowInSameTransaction) {
            try (PreparedStatement s = c.prepareStatement("delete from outbox where id = ?")) {
                s.setString(1, id);
                s.executeUpdate();
            }
        }
    }

    private interface Work {
        void on(Connection c) throws SQLException;
    }

    private void inOneTransaction(Work work, boolean commit) {
        try (Connection c = database.connect()) {
            c.setAutoCommit(false);
            work.on(c);
            if (commit) {
                c.commit();
            } else {
                c.rollback();
            }
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }
}
