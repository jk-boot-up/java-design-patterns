package com.jk.explore.modularmonolith;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import com.jk.explore.modularmonolith.catalog.CatalogApi;
import com.jk.explore.modularmonolith.orders.OrdersApi;
import com.jk.explore.modularmonolith.payments.PaymentsApi;
import java.util.List;
import org.junit.jupiter.api.Test;

class ModulesTest {

    @Test
    void theRealSourceHasNoBoundaryViolations() {
        assertEquals(List.of(), BoundaryCheck.scan(ModularMonolithDemo.SOURCES));
    }

    @Test
    void importingAnotherModulesInsidesIsCaught() {
        String src = "import com.jk.explore.modularmonolith.catalog.internal.CatalogModule;";
        assertEquals(List.of("X.java imports catalog.internal"), BoundaryCheck.check("orders", "X.java", src));
    }

    @Test
    void importingYourOwnInsidesIsFine() {
        String src = "import com.jk.explore.modularmonolith.orders.internal.OrdersModule;";
        assertEquals(List.of(), BoundaryCheck.check("orders", "OrdersApi.java", src));
    }

    @Test
    void catalogueRefusesToGoBelowZero() {
        CatalogApi catalog = CatalogApi.create();
        OrdersApi orders = OrdersApi.create(catalog, PaymentsApi.create());
        orders.placeOrder("a", "kettle", 1, 100);
        assertTrue(orders.placeOrder("b", "kettle", 1, 100).contains("refused"));
        assertEquals(0, catalog.stock("kettle"));
    }

    @Test
    void refusedOrderIsNotCharged() {
        PaymentsApi payments = PaymentsApi.create();
        OrdersApi.create(CatalogApi.create(), payments).placeOrder("a", "kettle", 5, 100);
        assertEquals(0, payments.takenFor("a"));
    }
}
