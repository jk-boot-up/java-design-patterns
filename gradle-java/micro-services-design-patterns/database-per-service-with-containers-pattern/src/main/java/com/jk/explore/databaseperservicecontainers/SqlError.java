package com.jk.explore.databaseperservicecontainers;

import java.sql.SQLException;
import org.postgresql.util.PSQLException;
import org.postgresql.util.ServerErrorMessage;

/**
 * Postgres's own refusal, in one line: its five-character error code and its message.
 *
 * <p>The code is called the SQLSTATE. It is the part a program should check, because it
 * never changes with the server's language settings. 42703 means "no such column",
 * 42P01 "no such table", 23503 "a foreign key would be broken" and 0A000 "not supported".
 */
public final class SqlError {

    private SqlError() {
    }

    public static String describe(SQLException e) {
        String message = e.getMessage();
        if (e instanceof PSQLException postgres) {
            ServerErrorMessage server = postgres.getServerErrorMessage();
            if (server != null && server.getMessage() != null) {
                message = server.getMessage();
            }
        }
        return "ERROR " + e.getSQLState() + ": " + message;
    }
}
