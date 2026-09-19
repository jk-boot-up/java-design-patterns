package com.jk.explore.acl;

import com.jk.explore.acl.adapter.LegacyInventoryAdapter;
import com.jk.explore.acl.adapter.UntranslatableLegacyData;
import com.jk.explore.acl.domain.Availability;
import com.jk.explore.acl.domain.StockLevel;
import com.jk.explore.acl.legacy.LegacyInventorySystem;
import com.jk.explore.acl.naive.NaiveShop;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.stream.Stream;

import static org.junit.jupiter.api.Assertions.*;

class AclTest {

    private final LegacyInventorySystem legacy = new LegacyInventorySystem();
    private final LegacyInventoryAdapter gateway = new LegacyInventoryAdapter(legacy);

    @Test
    void translatesCodesIntoTheShopsTerms() {
        assertEquals(new StockLevel("MUG-BLUE", 12, Availability.IN_STOCK), gateway.stockOf("MUG-BLUE"));
        assertEquals(Availability.DISCONTINUED, gateway.stockOf("MUG-OLD").availability());
        assertTrue(gateway.stockOf("TEA-050").canBeBought());
        assertFalse(gateway.stockOf("MUG-OLD").canBeBought());
    }

    @Test
    void aNewStatusIsOneDecisionInTheAdapter() {
        legacy.putOnHold("TEA-050");
        StockLevel level = gateway.stockOf("TEA-050");
        assertEquals(Availability.ON_HOLD, level.availability());
        assertFalse(level.canBeBought());
    }

    @Test
    void theShortcutMakesFourPrivateGuessesAboutAnUnknownStatus() {
        legacy.putOnHold("TEA-050");
        var row = legacy.fetch("TEA-050");
        assertEquals("in stock", NaiveShop.productPageLabel(row));
        assertTrue(NaiveShop.canAddToBasket(row));
        assertEquals(0, NaiveShop.reorderQuantity(row));
        assertEquals(4, NaiveShop.placesThatKnowTheCodes());
    }

    @Test
    void badDataIsRefusedWithTheSkuNamed() {
        legacy.corrupt("MUG-BLUE");
        UntranslatableLegacyData e = assertThrows(UntranslatableLegacyData.class, () -> gateway.stockOf("MUG-BLUE"));
        assertTrue(e.getMessage().contains("MUG-BLUE"));
        assertThrows(NumberFormatException.class, () -> NaiveShop.reportLine(legacy.fetch("MUG-BLUE")));
    }

    @Test
    void anUnknownItemIsRefused() {
        assertThrows(UntranslatableLegacyData.class, () -> gateway.stockOf("NOPE"));
    }

    @Test
    void theFieldsTheShopDoesNotUseAreListed() {
        assertEquals(List.of("LST_CNT_DT", "WHSE_CD", "UOM"), LegacyInventoryAdapter.fieldsDropped());
    }

    /** The rule that makes it a layer: nothing but the adapter, the naive contrast and the legacy package itself imports the legacy types. */
    @Test
    void onlyTheAdapterImportsTheLegacyPackage() throws IOException {
        try (Stream<Path> files = Files.walk(Path.of("src/main/java"))) {
            List<String> importers = files.filter(f -> f.toString().endsWith(".java"))
                    .filter(f -> !f.toString().contains("/legacy/") && !f.toString().contains("/naive/") && !f.toString().endsWith("AclDemo.java"))
                    .filter(f -> {
                        try {
                            return Files.readString(f).contains("import com.jk.explore.acl.legacy");
                        } catch (IOException e) {
                            throw new IllegalStateException(e);
                        }
                    }).map(f -> f.getFileName().toString()).toList();
            assertEquals(List.of("LegacyInventoryAdapter.java"), importers);
        }
    }
}
