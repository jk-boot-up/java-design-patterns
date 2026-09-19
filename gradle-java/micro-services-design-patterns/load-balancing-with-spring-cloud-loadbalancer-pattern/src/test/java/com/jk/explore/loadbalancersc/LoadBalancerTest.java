package com.jk.explore.loadbalancersc;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class LoadBalancerTest {

    private static void send(CatalogueApplication.Cluster c, String service, int n) {
        for (int i = 0; i < n; i++) {
            c.client.get(service, "/products/MUG-BLUE");
        }
    }

    @Test
    void roundRobinSpreadsTwelveRequestsEvenlyButWorkUnevenly() {
        try (CatalogueApplication.Cluster c = new CatalogueApplication.Cluster()) {
            send(c, "catalogue", 12);
            assertEquals("[4, 4, 4]", c.hits());
            assertEquals("[4, 4, 24]", c.work());
        }
    }

    @Test
    void leastWorkBalancerIsRegisteredForOneNameOnly() {
        try (CatalogueApplication.Cluster c = new CatalogueApplication.Cluster()) {
            send(c, "catalogue-fast", 12);
            assertEquals("[6, 5, 1]", c.hits());
            assertEquals("[6, 5, 6]", c.work());
        }
    }

    @Test
    void aStoppedCopyStillReceivesAThirdOfTheRequests() {
        try (CatalogueApplication.Cluster c = new CatalogueApplication.Cluster()) {
            c.copies.get(1).goDown();
            int failures = 0;
            for (int i = 0; i < 12; i++) {
                try {
                    c.client.get("catalogue", "/x");
                } catch (RuntimeException e) {
                    failures++;
                }
            }
            assertEquals(4, failures);
        }
    }

    @Test
    void aRetryFindsAnotherCopy() {
        try (CatalogueApplication.Cluster c = new CatalogueApplication.Cluster()) {
            c.copies.get(1).goDown();
            for (int i = 0; i < 12; i++) {
                boolean ok = false;
                for (int a = 0; a < 2 && !ok; a++) {
                    try {
                        c.client.get("catalogue", "/x");
                        ok = true;
                    } catch (RuntimeException e) {
                        // next copy
                    }
                }
                assertTrue(ok);
            }
        }
    }

    @Test
    void onlyLogicalNamesAreAccepted() {
        try (CatalogueApplication.Cluster c = new CatalogueApplication.Cluster()) {
            assertThrows(IllegalStateException.class, () -> c.client.get("checkout", "/health"));
            assertThrows(IllegalStateException.class, () -> c.client.get("127.0.0.1:" + c.copies.get(0).port(), "/x"));
        }
    }
}
