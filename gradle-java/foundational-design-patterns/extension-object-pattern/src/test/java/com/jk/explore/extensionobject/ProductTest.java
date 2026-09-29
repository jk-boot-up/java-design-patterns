package com.jk.explore.extensionobject;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.Test;

class ProductTest {

    @Test
    void missingRoleIsEmpty() {
        assertTrue(new Product("M", "mug", 1).extension(Extensions.Warranty.class).isEmpty());
    }

    @Test
    void attachedRoleIsFound() {
        Product p = new Product("K", "kettle", 1).with(Extensions.Warranty.class, new Extensions.Warranty(2));
        assertEquals(2, p.extension(Extensions.Warranty.class).orElseThrow().years());
    }

    @Test
    void aProductCanHaveSeveralRoles() {
        Product p = new Product("S", "software", 1)
                .with(Extensions.Download.class, new Extensions.Download("u", 1))
                .with(Extensions.Warranty.class, new Extensions.Warranty(1));
        assertEquals(2, Checkout.afterPayment(List.of(p)).size());
    }

    @Test
    void fatProductCountsEmptyFields() {
        assertEquals(5, new FatProduct("M", "m", 1L, null, null, null, null, null).emptyFields());
    }
}
