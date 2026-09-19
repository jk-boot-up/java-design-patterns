package com.jk.explore.repository;

import com.jk.explore.repository.domain.Shop;
import com.jk.explore.repository.naive.SqlInTheService;
import com.jk.explore.repository.toydb.Database;
import com.jk.explore.repository.toydb.Row;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

class SqlInTheServiceTest {

    @Test
    void theSameQuestionGivesThreeAnswersAndOneIsWrong() {
        SqlInTheService s = new SqlInTheService(Shop.seeded());
        assertEquals(List.of("Ada", "Grace"), s.marketingList());
        assertEquals(List.of("Ada", "Grace", "Ken"), s.supportList());
        assertEquals(List.of("Ada", "Grace"), s.reportList());
        assertNotEquals(s.marketingList(), s.supportList());
    }

    @Test
    void renamingAColumnSilentlyEmptiesEveryList() {
        Database db = Shop.seeded();
        for (Row row : db.table("customers").selectAll()) {
            db.table("customers").update(row.number("id"),
                    Row.of("id", row.number("id"), "name", row.text("name"), "town", row.text("city")));
        }
        SqlInTheService s = new SqlInTheService(db);
        assertEquals(List.of(), s.marketingList());
        assertEquals(List.of(), s.supportList());
        assertEquals(List.of(), s.reportList());
    }
}
