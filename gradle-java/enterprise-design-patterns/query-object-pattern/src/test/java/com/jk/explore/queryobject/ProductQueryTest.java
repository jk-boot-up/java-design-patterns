package com.jk.explore.queryobject;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class ProductQueryTest {

    @Test
    void emptyQueryHasNoWhere() {
        assertEquals("SELECT * FROM product", ProductQuery.all().toSql());
    }

    @Test
    void criteriaJoinWithAnd() {
        ProductQuery q = ProductQuery.all().and(Criterion.maxPrice(1000)).and(Criterion.inStock());
        assertEquals("SELECT * FROM product WHERE price_pence <= ? AND stock > 0", q.toSql());
        assertEquals(List.of(1000L), q.params());
    }

    @Test
    void textNeverAppearsInSql() {
        ProductQuery q = ProductQuery.all().and(Criterion.nameContains("'; DROP TABLE product; --"));
        assertTrue(!q.toSql().contains("DROP"));
    }

    @Test
    void inMemoryMatchesTheCriteria() {
        List<Product> found = ProductQuery.all().and(Criterion.category("kitchen")).and(Criterion.inStock())
                .runOn(QueryObjectDemo.TABLE);
        assertEquals(3, found.size());
    }

    @Test
    void addingACriterionLeavesTheOriginal() {
        ProductQuery base = ProductQuery.all().and(Criterion.inStock());
        base.and(Criterion.maxPrice(1));
        assertEquals(0, base.params().size());
        assertEquals("SELECT * FROM product WHERE stock > 0", base.toSql());
    }

    @Test
    void stringVersionIsBrokenWithoutCategory() {
        assertTrue(StringSql.build(null, 3000L, null).contains("WHERE  AND"));
    }
}
