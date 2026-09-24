package com.jk.explore.idempotentconsumerkafka;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

/**
 * Keeps the handled ids in the database, which outlives the process, but writes the id in a
 * second step after the email is queued. A crash between the two steps keeps the email and
 * loses the id.
 */
public class RecordIdAfterwards implements Handler {

    private final Database database;
    private final boolean dieBetweenTheTwoSteps;

    public RecordIdAfterwards(Database database, boolean dieBetweenTheTwoSteps) {
        this.database = database;
        this.dieBetweenTheTwoSteps = dieBetweenTheTwoSteps;
    }

    @Override
    public boolean handle(OrderPlaced order) {
        try (Connection c = database.connect()) {
            if (RecordIdInSameTransaction.alreadyHandled(c, order)) {
                return false;
            }
            JustSend.queueConfirmation(c, order);
            if (dieBetweenTheTwoSteps) {
                throw new ProcessDied("after queueing the email, before writing the id");
            }
            try (PreparedStatement s = c.prepareStatement("insert into handled_messages (message_id, order_placed_at) values (?, ?)")) {
                s.setString(1, order.messageId());
                s.setTimestamp(2, java.sql.Timestamp.from(order.placedAt()));
                s.executeUpdate();
            }
            return true;
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }
}
