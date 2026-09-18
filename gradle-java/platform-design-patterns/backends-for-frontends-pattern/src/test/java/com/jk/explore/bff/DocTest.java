package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class DocTest {

    @Test
    @DisplayName("fields keep the order they were added, so a size never moves between runs")
    void keepsInsertionOrder() {
        Doc doc = Doc.doc().put("b", 1).put("a", 2).put("c", 3);

        assertEquals(List.of("b", "a", "c"), doc.names());
        assertEquals("{\"b\":1,\"a\":2,\"c\":3}", doc.compact());
    }

    @Test
    @DisplayName("bytes is the length of the compact form, which is what goes on the wire")
    void bytesIsTheCompactForm() {
        Doc doc = Doc.doc().put("title", "Coffee");

        assertEquals(doc.compact().length(), doc.bytes());
    }

    @Test
    @DisplayName("nested fields are named the way a client developer would say them")
    void pathsNameNestedFields() {
        Doc doc = Doc.doc()
                .put("title", "Coffee")
                .put("reviews", Doc.doc().put("average", 4.6).put("count", 218));

        assertEquals(List.of("title", "reviews.average", "reviews.count"), doc.paths());
    }

    @Test
    @DisplayName("selecting keeps named fields and drops everything else")
    void selectKeepsOnlyWhatIsNamed() {
        Doc doc = Doc.doc()
                .put("title", "Coffee")
                .put("description", "a very long description")
                .put("reviews", Doc.doc().put("average", 4.6).put("count", 218));

        Doc kept = doc.select(List.of("title", "reviews.average"));

        assertEquals(List.of("title", "reviews.average"), kept.paths());
        assertTrue(kept.bytes() < doc.bytes());
    }

    @Test
    @DisplayName("naming a parent keeps the whole block underneath it")
    void selectingAParentKeepsItsChildren() {
        Doc doc = Doc.doc()
                .put("title", "Coffee")
                .put("reviews", Doc.doc().put("average", 4.6).put("count", 218));

        Doc kept = doc.select(List.of("reviews"));

        assertEquals(List.of("reviews.average", "reviews.count"), kept.paths());
    }

    @Test
    @DisplayName("lists survive both selection and serialisation")
    void serialisesLists() {
        Doc doc = Doc.doc().put("related", List.of("SKU-1", "SKU-2"));

        assertEquals("{\"related\":[\"SKU-1\",\"SKU-2\"]}", doc.compact());
        assertEquals(List.of("related"), doc.select(List.of("related")).paths());
    }
}
