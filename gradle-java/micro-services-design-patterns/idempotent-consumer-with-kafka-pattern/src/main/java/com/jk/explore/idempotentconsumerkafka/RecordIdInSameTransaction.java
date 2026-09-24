package com.jk.explore.idempotentconsumerkafka;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;

/**
 * The pattern. The message's id and the confirmation email are written in one database
 * transaction, so they are kept together or thrown away together.
 *
 * <p>The id is written first, with {@code on conflict do nothing}: if the id is already in
 * the table, Postgres writes nothing and says it wrote zero rows, and that zero is the
 * signal to skip. If another copy has written the same id and not yet committed, Postgres
 * makes this copy wait until the other one finishes, and then gives the same answer.
 */
public class RecordIdInSameTransaction implements Handler {

    private final Database database;

    public RecordIdInSameTransaction(Database database) {
        this.database = database;
    }

    @Override
    public boolean handle(OrderPlaced order) {
        Open open = begin(order);
        open.commit();
        return open.queued();
    }

    /**
     * Does the whole of the work inside a transaction and stops just short of the commit.
     * The demo uses this to hold a copy still at that instant, or to kill it there.
     */
    public Open begin(OrderPlaced order) {
        try {
            Connection c = database.connect();
            c.setAutoCommit(false);
            boolean first;
            try (PreparedStatement s = c.prepareStatement(
                    "insert into handled_messages (message_id, order_placed_at) values (?, ?) on conflict (message_id) do nothing")) {
                s.setString(1, order.messageId());
                s.setTimestamp(2, Timestamp.from(order.placedAt()));
                first = s.executeUpdate() == 1;
            }
            if (first) {
                JustSend.queueConfirmation(c, order);
            }
            return new Open(c, first);
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    /** A transaction that has done its work and is waiting to be committed, or to die. */
    public static final class Open {

        private final Connection connection;
        private final boolean queued;

        Open(Connection connection, boolean queued) {
            this.connection = connection;
            this.queued = queued;
        }

        /** True when this copy wrote the id, and so queued the email. */
        public boolean queued() {
            return queued;
        }

        public void commit() {
            try (connection) {
                connection.commit();
            } catch (SQLException e) {
                throw new IllegalStateException(e);
            }
        }

        /** The process dies here. The connection drops, and Postgres throws the whole transaction away. */
        public void die() {
            try {
                connection.close();
            } catch (SQLException e) {
                throw new IllegalStateException(e);
            }
        }
    }

    static boolean alreadyHandled(Connection c, OrderPlaced order) throws SQLException {
        try (PreparedStatement s = c.prepareStatement("select 1 from handled_messages where message_id = ?")) {
            s.setString(1, order.messageId());
            try (ResultSet r = s.executeQuery()) {
                return r.next();
            }
        }
    }
}
