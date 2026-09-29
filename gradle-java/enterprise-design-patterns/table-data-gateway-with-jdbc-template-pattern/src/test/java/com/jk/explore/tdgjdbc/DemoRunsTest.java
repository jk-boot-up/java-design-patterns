package com.jk.explore.tdgjdbc;

import static org.junit.jupiter.api.Assertions.assertTrue;

import org.junit.jupiter.api.Test;

/** The whole demo, with Spring's JdbcTemplate and an in-memory H2 database. */
class DemoRunsTest {

    @Test
    void acts() {
        String all = String.join("\n", JdbcTemplateGatewayDemo.run());
        assertTrue(all.contains("third page: FAILED after 0.25 s, the pool of 2 connections is empty"), all);
        assertTrue(all.contains("asked 4 times on a pool of 2: steel kettle, 4 in stock"), all);
        assertTrue(all.contains("stock report: 1 product out of stock"), all);
        assertTrue(all.contains("cheaper than £10: [mug, tea towel]"), all);
        assertTrue(all.contains("behind the gateway's back: BadSqlGrammarException"), all);
        assertTrue(all.contains("a second MUG-1: DuplicateKeyException"), all);
        assertTrue(all.contains("4 customers try for 2 desk lamps: 2 taken, stock now 0"), all);
    }
}
