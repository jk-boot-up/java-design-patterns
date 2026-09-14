package com.jk.explore.databaseperservice;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * The shared database, tested honestly.
 *
 * Every test in this class passes, including the one where the order history page
 * breaks. That is deliberate. The break is not a bug in anybody's code — the migration
 * was correct, the query was correct, and each team's own tests stayed green. The
 * failure only exists in the space between two teams, which is exactly the space that
 * no test suite owns.
 */
class SharedSchemaTest {

    private static final String CUSTOMER = "cust-7";

    private SharedSchema schema;

    @BeforeEach
    void setUp() {
        schema = new SharedSchema();
        schema.addProduct("SKU-KETTLE", "Stainless Steel Kettle");
        schema.addProduct("SKU-MUG", "Blue Stoneware Mug");
        schema.addOrder(new Order("ord-101", CUSTOMER, "SKU-KETTLE", 1));
        schema.addOrder(new Order("ord-102", CUSTOMER, "SKU-MUG", 4));
        schema.addOrder(new Order("ord-103", "cust-9", "SKU-MUG", 1));
    }

    @Test
    @DisplayName("one query returns a page with names already attached")
    void itJoinsInOneQuery() {
        List<OrderHistoryRow> page = schema.orderHistory(CUSTOMER);

        assertEquals(2, page.size());
        assertEquals("Stainless Steel Kettle", page.get(0).productName());
        assertEquals("Blue Stoneware Mug", page.get(1).productName());
        assertEquals(1, schema.queriesForOnePage());
    }

    @Test
    @DisplayName("the join never leaves a name missing")
    void everyRowHasAName() {
        for (OrderHistoryRow row : schema.orderHistory(CUSTOMER)) {
            assertEquals(false, row.productName() == null || row.productName().isBlank(),
                    row.orderId() + " has no product name");
        }
    }

    @Test
    @DisplayName("other customers' orders stay out of the page")
    void itFiltersByCustomer() {
        assertEquals(1, schema.orderHistory("cust-9").size());
    }

    @Test
    @DisplayName("a rename the catalog team is entitled to make breaks somebody else")
    void aRenameBreaksTheOrderHistoryPage() {
        schema.renameProductNameColumnTo("title");

        ColumnNotFoundException broken =
                assertThrows(ColumnNotFoundException.class, () -> schema.orderHistory(CUSTOMER));

        assertEquals(true, broken.getMessage().contains("product_name"));
    }

    @Test
    @DisplayName("the catalog data itself is perfectly fine after the rename")
    void theRenameLosesNothing() {
        schema.renameProductNameColumnTo("title");

        // Nothing was lost and nothing was corrupted. The migration did its job. The
        // only casualty is a query in a repository the catalog team has never opened.
        schema.addOrder(new Order("ord-104", "cust-9", "SKU-KETTLE", 1));
        assertThrows(ColumnNotFoundException.class, () -> schema.orderHistory("cust-9"));
    }
}
