package com.jk.explore.queryobject;

/**
 * Without the pattern: the search page glues SQL together from whichever filters were filled in.
 *
 * <p>It adds " AND " before every filter after the first one it expects, so
 * leaving the first filter empty produces "WHERE AND". And it pastes the
 * customer's text straight into the SQL.
 */
public final class StringSql {

    public static String build(String category, Long maxPence, String nameContains) {
        StringBuilder sql = new StringBuilder("SELECT * FROM product WHERE ");
        if (category != null) {
            sql.append("category = '").append(category).append("'");
        }
        if (maxPence != null) {
            sql.append(" AND price_pence <= ").append(maxPence);
        }
        if (nameContains != null) {
            sql.append(" AND name LIKE '%").append(nameContains).append("%'");
        }
        return sql.toString();
    }

    private StringSql() {
    }
}
