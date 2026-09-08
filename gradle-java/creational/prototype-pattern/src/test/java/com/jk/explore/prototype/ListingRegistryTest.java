package com.jk.explore.prototype;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.NoSuchElementException;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

@DisplayName("ListingRegistry — clones a named template on every create()")
class ListingRegistryTest {

    private ProductListing template() {
        Map<String, String> attributes = new LinkedHashMap<>();
        attributes.put("color", "Black");

        return new ProductListing(
                "SKU-1", "Wireless Earbuds", "Description",
                "Electronics", "Acme Audio", Money.pounds(59.99),
                List.of("img-1.jpg"), attributes,
                new ShippingProfile("ParcelForce", 180, false), 30, 12);
    }

    @Test
    void createReturnsIndependentInstancesFromTheSameKey() {
        ListingRegistry registry = new ListingRegistry();
        registry.register("earbuds", template());

        ProductListing first = registry.create("earbuds");
        ProductListing second = registry.create("earbuds");

        assertNotSame(first, second);
        assertEquals(first, second);

        first.attributes().put("color", "Blue");

        assertEquals("Blue", first.attributes().get("color"));
        assertEquals("Black", second.attributes().get("color"));
    }

    @Test
    void createThrowsForUnknownKey() {
        ListingRegistry registry = new ListingRegistry();

        assertThrows(NoSuchElementException.class, () -> registry.create("missing"));
    }

    @Test
    void keysReflectsRegisteredTemplates() {
        ListingRegistry registry = new ListingRegistry();
        registry.register("earbuds", template());

        assertTrue(registry.keys().contains("earbuds"));
    }
}
