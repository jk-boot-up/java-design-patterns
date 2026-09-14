package com.jk.explore.databaseperservice;

/**
 * A query asked for a column that no longer exists.
 *
 * This is the error the catalog team's harmless little rename produces in somebody
 * else's code, at three in the afternoon, in the middle of checkout.
 */
public class ColumnNotFoundException extends RuntimeException {

    public ColumnNotFoundException(String column, String table) {
        super("no column '" + column + "' in " + table + " -- somebody renamed it");
    }
}
