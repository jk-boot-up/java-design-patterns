package com.jk.explore.stijpa;

import java.util.List;
import java.util.concurrent.CopyOnWriteArrayList;
import org.hibernate.resource.jdbc.spi.StatementInspector;

/**
 * Hibernate hands every SQL statement it is about to send to this class first, so the demo can show
 * exactly what JPA's annotations turned into.
 */
public class SqlLog implements StatementInspector {

    static final List<String> STATEMENTS = new CopyOnWriteArrayList<>();

    @Override
    public String inspect(String sql) {
        STATEMENTS.add(sql.toLowerCase());
        return sql;
    }
}
