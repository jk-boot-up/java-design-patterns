package com.jk.explore.prototype;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("ProductListing.copy() — independent clones that share only what's immutable")
class ProductListingTest {

    private ProductListing newMaster() {
        Map<String, String> attributes = new LinkedHashMap<>();
        attributes.put("color", "Black");

        return new ProductListing(
                "SKU-1", "Wireless Earbuds", "Description",
                "Electronics", "Acme Audio", Money.pounds(59.99),
                List.of("img-1.jpg"), attributes,
                new ShippingProfile("ParcelForce", 180, false), 30, 12);
    }

    @Test
    void copyIsEqualButNotSame() {
        ProductListing master = newMaster();

        ProductListing copy = master.copy();

        assertNotSame(master, copy);
        assertEquals(master, copy);
    }

    @Test
    void mutatingCopyImagesDoesNotAffectMaster() {
        ProductListing master = newMaster();
        ProductListing copy = master.copy();

        copy.images().add("img-2.jpg");

        assertEquals(1, master.images().size());
        assertEquals(2, copy.images().size());
    }

    @Test
    void mutatingCopyAttributesDoesNotAffectMaster() {
        ProductListing master = newMaster();
        ProductListing copy = master.copy();

        copy.attributes().put("color", "White");

        assertEquals("Black", master.attributes().get("color"));
        assertEquals("White", copy.attributes().get("color"));
    }

    @Test
    void mutatingCopyViaSettersDoesNotAffectMaster() {
        ProductListing master = newMaster();
        ProductListing copy = master.copy();

        copy.setSku("SKU-2");
        copy.setTitle("Wireless Earbuds (White)");
        copy.setPrice(Money.pounds(49.99));

        assertEquals("SKU-1", master.sku());
        assertEquals("Wireless Earbuds", master.title());
        assertEquals(Money.pounds(59.99), master.price());
    }

    @Test
    void shippingProfileIsSharedByReferenceAcrossCopies() {
        ProductListing master = newMaster();
        ProductListing copy = master.copy();

        assertSame(master.shippingProfile(), copy.shippingProfile());
    }
}
