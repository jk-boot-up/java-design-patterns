package com.jk.explore.visitor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/** The four reports, and whether each of them is actually right. */
class ReportVisitorTest {

    private static Category tree() {
        return Catalog.demoTree();
    }

    @Nested
    @DisplayName("inventory value")
    class InventoryValue {

        @Test
        @DisplayName("a product is worth its price times its stock")
        void productValue() {
            InventoryValueVisitor visitor = new InventoryValueVisitor();
            new Product("P", "Case", Money.pounds(19.99), 10).accept(visitor);
            assertEquals(Money.pounds(199.90), visitor.total());
        }

        @Test
        @DisplayName("a bundle is worth its kit price, not the sum of its parts")
        void bundleValueIsTheKitPrice() {
            Bundle kit = new Bundle("K", "Kit", Money.pounds(100), 2)
                    .containing(new Product("A", "Phone", Money.pounds(80), 5))
                    .containing(new Product("B", "Case", Money.pounds(40), 5));

            InventoryValueVisitor visitor = new InventoryValueVisitor();
            kit.accept(visitor);

            // £200, not £240. Two visit methods is the whole reason this
            // can be stated once and not guarded by an instanceof.
            assertEquals(Money.pounds(200), visitor.total());
        }

        @Test
        @DisplayName("the saving against the parts is the bundle's own business")
        void bundleKnowsItsSaving() {
            Bundle kit = new Bundle("K", "Kit", Money.pounds(100), 2)
                    .containing(new Product("A", "Phone", Money.pounds(80), 5))
                    .containing(new Product("B", "Case", Money.pounds(40), 5));
            assertEquals(Money.pounds(20), kit.savingAgainstParts());
        }

        @Test
        @DisplayName("a category holds no value of its own")
        void categoriesAddNothing() {
            InventoryValueVisitor bare = new InventoryValueVisitor();
            new Category("Clearance").accept(bare);
            assertEquals(Money.zero(), bare.total());
            assertEquals(0, bare.lines());
        }

        @Test
        @DisplayName("nesting does not change the total")
        void nestingIsIrrelevant() {
            Product case1 = new Product("A", "Case", Money.pounds(10), 3);
            Product cable = new Product("B", "Cable", Money.pounds(5), 4);

            InventoryValueVisitor flat = new InventoryValueVisitor();
            new Category("Flat").add(case1).add(cable).accept(flat);

            InventoryValueVisitor deep = new InventoryValueVisitor();
            new Category("Deep").add(case1)
                    .add(new Category("Inner").add(new Category("Inner2").add(cable)))
                    .accept(deep);

            assertEquals(flat.total(), deep.total());
        }

        @Test
        @DisplayName("the demo catalog totals £78,609.86")
        void demoTreeTotal() {
            InventoryValueVisitor visitor = new InventoryValueVisitor();
            tree().accept(visitor);
            assertEquals(Money.parse("78609.86"), visitor.total());
            assertEquals(7, visitor.lines());
            assertEquals(1229, visitor.units());
        }

        @Test
        @DisplayName("the bundle's contents are not counted a second time")
        void noDoubleCounting() {
            InventoryValueVisitor visitor = new InventoryValueVisitor();
            tree().accept(visitor);
            // Seven lines: six products and one bundle. The three products
            // inside the kit are already among the six.
            assertEquals(7, visitor.lines());
        }
    }

    @Nested
    @DisplayName("count by category")
    class CountByCategory {

        @Test
        @DisplayName("direct counts are what sits immediately in the category")
        void directCounts() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree().accept(visitor);
            Map<String, Integer> direct = visitor.directCounts();

            assertEquals(1, direct.get("Electronics"));
            assertEquals(4, direct.get("Electronics/Accessories"));
            assertEquals(1, direct.get("Electronics/Accessories/Cables"));
            assertEquals(1, direct.get("Electronics/Kits"));
        }

        @Test
        @DisplayName("total counts include everything beneath")
        void totalCounts() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree().accept(visitor);
            Map<String, Integer> total = visitor.totalCounts();

            assertEquals(7, total.get("Electronics"));
            assertEquals(5, total.get("Electronics/Accessories"));
            assertEquals(1, total.get("Electronics/Accessories/Cables"));
        }

        @Test
        @DisplayName("an empty category appears in the report as a zero")
        void emptyCategoryIsReported() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree().accept(visitor);
            // The category is registered on the way in, so it exists in the
            // report whether or not anything is in it. A report built by
            // asking products which category they are in cannot do this.
            assertEquals(0, visitor.directCounts().get("Electronics/Clearance"));
            assertEquals(0, visitor.totalCounts().get("Electronics/Clearance"));
        }

        @Test
        @DisplayName("the paths are full paths, so two categories can share a name")
        void pathsDisambiguate() {
            Category tree = new Category("Shop")
                    .add(new Category("Audio").add(new Product("A", "Earbuds", Money.pounds(1), 1)))
                    .add(new Category("Clearance")
                            .add(new Category("Audio")
                                    .add(new Product("B", "Old Earbuds", Money.pounds(1), 1))));

            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree.accept(visitor);

            assertEquals(1, visitor.directCounts().get("Shop/Audio"));
            assertEquals(1, visitor.directCounts().get("Shop/Clearance/Audio"));
        }

        @Test
        @DisplayName("categories come out in tree order")
        void treeOrder() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree().accept(visitor);
            assertEquals(List.of("Electronics", "Electronics/Accessories",
                            "Electronics/Accessories/Cables", "Electronics/Kits",
                            "Electronics/Clearance"),
                    List.copyOf(visitor.directCounts().keySet()));
        }

        @Test
        @DisplayName("bundles count as one line, like products")
        void bundlesCountAsOne() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            new Category("Kits")
                    .add(new Bundle("K", "Kit", Money.pounds(1), 1)
                            .containing(new Product("A", "Phone", Money.pounds(1), 1))
                            .containing(new Product("B", "Case", Money.pounds(1), 1)))
                    .accept(visitor);
            assertEquals(1, visitor.directCounts().get("Kits"));
        }

        @Test
        @DisplayName("five categories in the demo catalog")
        void categoryCount() {
            CategoryCountVisitor visitor = new CategoryCountVisitor();
            tree().accept(visitor);
            assertEquals(5, visitor.categories());
        }
    }

    @Nested
    @DisplayName("CSV export")
    class CsvExport {

        @Test
        @DisplayName("one row per sellable line, none for categories")
        void rowCount() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            tree().accept(visitor);
            assertEquals(7, visitor.rows().size());
        }

        @Test
        @DisplayName("a name with a comma is quoted")
        void quotesCommas() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            new Product("CLN", "Screen Cleaner, 200ml", Money.pounds(6.50), 5).accept(visitor);
            assertTrue(visitor.rows().get(0).contains("\"Screen Cleaner, 200ml\""));
        }

        @Test
        @DisplayName("a bundle name with a comma is quoted too")
        void quotesBundleNames() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            new Bundle("KIT", "Starter Kit, 3 items", Money.pounds(639), 25).accept(visitor);
            // The bug NaiveBundle has. One quoting rule, in one class,
            // cannot be applied to products and forgotten for bundles.
            assertTrue(visitor.rows().get(0).contains("\"Starter Kit, 3 items\""));
        }

        @Test
        @DisplayName("a quote inside a name is doubled")
        void doublesQuotes() {
            assertEquals("\"6\"\" Screen\"", CsvExportVisitor.quote("6\" Screen"));
        }

        @Test
        @DisplayName("a field with nothing special is left alone")
        void leavesPlainFieldsAlone() {
            assertEquals("Charger", CsvExportVisitor.quote("Charger"));
        }

        @Test
        @DisplayName("every row has the same number of columns as the header")
        void columnsLineUp() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            tree().accept(visitor);

            int expected = fields(CsvExportVisitor.HEADER);
            for (String row : visitor.rows()) {
                assertEquals(expected, fields(row), "misaligned row: " + row);
            }
        }

        @Test
        @DisplayName("the row carries the full category path")
        void rowsCarryTheirPath() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            tree().accept(visitor);
            assertTrue(visitor.rows().stream()
                    .anyMatch(row -> row.startsWith("Electronics/Accessories/Cables,CBL-001,")));
        }

        @Test
        @DisplayName("the file starts with the header")
        void fileHasAHeader() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            tree().accept(visitor);
            assertTrue(visitor.csv().startsWith(CsvExportVisitor.HEADER + "\n"));
            assertEquals(8, visitor.csv().split("\n").length);
        }

        @Test
        @DisplayName("prices are written with two decimal places")
        void pricesAreFormatted() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            new Product("P", "Cable", Money.pounds(9.99), 1).accept(visitor);
            assertTrue(visitor.rows().get(0).contains(",9.99,"));
        }

        private int fields(String row) {
            int count = 1;
            boolean quoted = false;
            for (char c : row.toCharArray()) {
                if (c == '"') {
                    quoted = !quoted;
                } else if (c == ',' && !quoted) {
                    count++;
                }
            }
            return count;
        }
    }

    @Nested
    @DisplayName("compliance audit")
    class ComplianceAudit {

        @Test
        @DisplayName("an unrestricted product produces no finding")
        void plainProductIsClear() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            new Product("P", "Case", Money.pounds(19.99), 5).accept(visitor);
            assertEquals(List.of(), visitor.findings());
            assertEquals(1, visitor.itemsChecked());
        }

        @Test
        @DisplayName("a restricted product produces one finding with its obligation")
        void restrictedProductIsReported() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            new Product("BAT", "Spare Battery Pack", Money.pounds(34.99), 5,
                    Restriction.LITHIUM_BATTERY).accept(visitor);

            assertEquals(1, visitor.findings().size());
            assertTrue(visitor.findings().get(0).contains("UN3481"));
        }

        @Test
        @DisplayName("a bundle is restricted by what is in the box")
        void bundleInheritsFromItsContents() {
            Bundle kit = new Bundle("KIT", "Kit", Money.pounds(639), 25)
                    .containing(new Product("PHN", "Phone", Money.pounds(599.99), 1))
                    .containing(new Product("BAT", "Battery", Money.pounds(34.99), 1,
                            Restriction.LITHIUM_BATTERY));

            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            kit.accept(visitor);

            // The bug NaiveBundle has, asserted the right way round.
            assertEquals(1, visitor.findings().size());
            assertTrue(visitor.findings().get(0).contains("from Battery in the box"));
        }

        @Test
        @DisplayName("a bundle of clear items is clear")
        void plainBundleIsClear() {
            Bundle kit = new Bundle("KIT", "Kit", Money.pounds(50), 1)
                    .containing(new Product("A", "Case", Money.pounds(19.99), 1));

            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            kit.accept(visitor);
            assertEquals(List.of(), visitor.findings());
        }

        @Test
        @DisplayName("a bundle with two restricted items produces two findings")
        void oneFindingPerRestrictedContent() {
            Bundle kit = new Bundle("KIT", "Kit", Money.pounds(50), 1)
                    .containing(new Product("A", "Battery", Money.pounds(1), 1,
                            Restriction.LITHIUM_BATTERY))
                    .containing(new Product("B", "Cleaner", Money.pounds(1), 1,
                            Restriction.FLAMMABLE));

            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            kit.accept(visitor);
            assertEquals(2, visitor.findings().size());
        }

        @Test
        @DisplayName("the demo catalog has three findings, one of them the kit")
        void demoTreeFindings() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            tree().accept(visitor);

            assertEquals(3, visitor.findings().size());
            assertEquals(7, visitor.itemsChecked());
            assertTrue(visitor.findings().get(2).contains("Starter Kit"));
        }

        @Test
        @DisplayName("a lithium cell anywhere stops the shipment flying")
        void lithiumBlocksAir() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            tree().accept(visitor);
            assertFalse(visitor.clearForAir());
            assertTrue(visitor.obligations().contains(Restriction.LITHIUM_BATTERY));
        }

        @Test
        @DisplayName("a catalog of ordinary things flies")
        void plainCatalogIsClearForAir() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            new Category("Accessories")
                    .add(new Product("A", "Case", Money.pounds(19.99), 1))
                    .accept(visitor);
            assertTrue(visitor.clearForAir());
        }

        @Test
        @DisplayName("the finding says where in the tree the item was")
        void findingsCarryThePath() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            tree().accept(visitor);
            assertTrue(visitor.findings().get(0)
                    .startsWith("Electronics/Accessories/Spare Battery Pack"));
        }

        @Test
        @DisplayName("distinct obligations are collected once each")
        void obligationsAreDistinct() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            tree().accept(visitor);
            // Three findings, two obligations -- the battery appears twice,
            // once on its own and once inside the kit.
            assertEquals(2, visitor.obligations().size());
        }
    }

    @Nested
    @DisplayName("the dispatch trace")
    class Trace {

        @Test
        @DisplayName("counts each node type")
        void countsByType() {
            DispatchTraceVisitor visitor = new DispatchTraceVisitor();
            tree().accept(visitor);
            assertEquals(6, visitor.products());
            assertEquals(1, visitor.bundles());
            assertEquals(5, visitor.categories());
        }

        @Test
        @DisplayName("one line per call, entering and leaving")
        void oneLinePerCall() {
            DispatchTraceVisitor visitor = new DispatchTraceVisitor();
            tree().accept(visitor);
            // 6 products + 1 bundle + 5 categories entered + 5 left.
            assertEquals(17, visitor.trace().size());
        }

        @Test
        @DisplayName("the trace names the method that ran")
        void namesTheMethod() {
            DispatchTraceVisitor visitor = new DispatchTraceVisitor();
            tree().accept(visitor);
            assertTrue(visitor.trace().get(1).startsWith("visit(Product)"));
            assertTrue(visitor.trace().get(visitor.trace().size() - 1)
                    .startsWith("leave(Category)"));
        }
    }
}
