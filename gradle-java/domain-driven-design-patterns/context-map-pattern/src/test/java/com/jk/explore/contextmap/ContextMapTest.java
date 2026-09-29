package com.jk.explore.contextmap;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.jk.explore.contextmap.before.Separate;
import com.jk.explore.contextmap.kernel.Address;
import com.jk.explore.contextmap.kernel.Money;
import com.jk.explore.contextmap.sales.Sales;
import java.util.List;
import org.junit.jupiter.api.Test;

class ContextMapTest {

    @Test
    void theCodeMatchesTheMap() {
        assertEquals(List.of(), ContextMap.surprises(ContextMapDemo.SOURCES));
    }

    @Test
    void shippingMayNotImportSales() {
        assertEquals(1, ContextMap.check("shipping", "X.java", "import com.jk.explore.contextmap.sales.Sales;").size());
    }

    @Test
    void salesMayImportCatalogAndKernel() {
        assertEquals(List.of(), ContextMap.check("sales", "X.java",
                "import com.jk.explore.contextmap.catalog.Catalog;\nimport com.jk.explore.contextmap.kernel.Money;"));
    }

    @Test
    void converterLosesTheFlat() {
        assertEquals("4 Mill Lane, Leeds",
                Separate.convert(new Separate.SalesAddress("Flat 2", "4 Mill Lane", "Leeds")).label());
    }

    @Test
    void kernelAddressKeepsTheFlat() {
        assertEquals("Flat 2, 4 Mill Lane, Leeds", new Address("Flat 2", "4 Mill Lane", "Leeds").label());
    }

    @Test
    void salesTotalsWithKernelMoney() {
        assertEquals(new Money(3800), Sales.placeOrder("O", null, "KETTLE-1", "MUG-1").total());
    }
}
