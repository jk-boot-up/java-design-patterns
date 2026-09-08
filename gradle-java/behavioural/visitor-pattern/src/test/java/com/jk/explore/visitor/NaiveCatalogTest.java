package com.jk.explore.visitor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNotEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * The naive catalog's bugs, pinned as passing tests, each paired with the
 * same question asked through a visitor.
 *
 * <p>Nothing here is a bug report. These are the behaviours the naive design
 * has today, asserted so that they cannot quietly change, and so that the
 * comparison in the README is checkable rather than rhetorical.
 */
class NaiveCatalogTest {

    private static NaiveCategory naive() {
        return Catalog.naiveDemoTree();
    }

    private static Category pattern() {
        return Catalog.demoTree();
    }

    private static List<String> naiveAudit() {
        List<String> findings = new ArrayList<>();
        naive().auditInto(findings, "");
        return findings;
    }

    private static String naiveCsv() {
        StringBuilder out = new StringBuilder();
        naive().appendCsvTo(out, "");
        return out.toString();
    }

    private static int fields(String row) {
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

    private static String rowFor(String csv, String sku) {
        for (String row : csv.split("\n")) {
            if (row.contains("," + sku + ",")) {
                return row;
            }
        }
        throw new AssertionError("no row for " + sku);
    }

    @Nested
    @DisplayName("where the naive design is right")
    class WhereItIsRight {

        @Test
        @DisplayName("the inventory total agrees with the visitor, to the penny")
        void inventoryValueAgrees() {
            InventoryValueVisitor visitor = new InventoryValueVisitor();
            pattern().accept(visitor);
            // This is the honest starting point of the argument: the first
            // two reports written this way are correct, and pleasant.
            assertEquals(visitor.total(), naive().inventoryValue());
        }

        @Test
        @DisplayName("the direct counts agree with the visitor")
        void countsAgree() {
            Map<String, Integer> counts = new LinkedHashMap<>();
            naive().countInto(counts, "");

            CategoryCountVisitor visitor = new CategoryCountVisitor();
            pattern().accept(visitor);

            assertEquals(visitor.directCounts(), counts);
        }

        @Test
        @DisplayName("a new node type costs the naive design one class")
        void newNodeTypeIsCheapHere() {
            // The trade, from the other side. A fourth NaiveCatalogNode is
            // a new file and nothing else recompiles -- while a fourth node
            // type in the pattern version breaks every visitor there is.
            // Five methods: name(), and one per report.
            assertEquals(5, NaiveCatalogNode.class.getDeclaredMethods().length);
            assertEquals(3, countImplementations());
        }

        private int countImplementations() {
            return List.of(NaiveProduct.class, NaiveBundle.class, NaiveCategory.class).size();
        }
    }

    @Nested
    @DisplayName("the CSV quoting that was dropped on the copy")
    class CsvQuoting {

        @Test
        @DisplayName("the product row is quoted correctly")
        void productRowIsFine() {
            assertTrue(rowFor(naiveCsv(), "CLN-003").contains("\"Screen Cleaner, 200ml\""));
        }

        @Test
        @DisplayName("the bundle row is not, so it gains a column")
        void bundleRowGainsAColumn() {
            String row = rowFor(naiveCsv(), "KIT-01");
            assertFalse(row.contains("\"Starter Kit, 3 items\""));
            assertEquals(8, fields(row));
        }

        @Test
        @DisplayName("the product row and the bundle row disagree on column count")
        void rowsDisagree() {
            String csv = naiveCsv();
            assertNotEquals(fields(rowFor(csv, "CLN-003")), fields(rowFor(csv, "KIT-01")));
        }

        @Test
        @DisplayName("the visitor's rows all agree, because there is one quoting rule")
        void visitorRowsAgree() {
            CsvExportVisitor visitor = new CsvExportVisitor();
            pattern().accept(visitor);
            for (String row : visitor.rows()) {
                assertEquals(7, fields(row), "misaligned row: " + row);
            }
        }

        @Test
        @DisplayName("the quoting rule exists in two domain classes at once")
        void quotingLivesOnTheModel() {
            // Named for the smell rather than the symptom: a class about a
            // thing on a shelf has a private method about file format.
            boolean productKnowsCsv = false;
            for (Method method : NaiveProduct.class.getDeclaredMethods()) {
                if (method.getName().equals("quote")) {
                    productKnowsCsv = true;
                }
            }
            assertTrue(productKnowsCsv);

            for (Method method : Product.class.getDeclaredMethods()) {
                assertNotEquals("quote", method.getName(),
                        "the pattern's Product learned about CSV");
            }
        }
    }

    @Nested
    @DisplayName("the compliance check that reads the wrong field")
    class Compliance {

        @Test
        @DisplayName("the naive audit finds the loose battery")
        void findsTheLooseBattery() {
            assertTrue(naiveAudit().stream()
                    .anyMatch(finding -> finding.contains("BAT-014")));
        }

        @Test
        @DisplayName("but never the one inside the kit")
        void missesTheBatteryInTheKit() {
            assertFalse(naiveAudit().stream()
                    .anyMatch(finding -> finding.contains("KIT-01")));
            assertEquals(2, naiveAudit().size());
        }

        @Test
        @DisplayName("the visitor finds all three")
        void theVisitorFindsTheKit() {
            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            pattern().accept(visitor);
            assertEquals(3, visitor.findings().size());
            assertTrue(visitor.findings().stream()
                    .anyMatch(finding -> finding.contains("KIT-01")));
        }

        @Test
        @DisplayName("so the naive report clears a shipment the visitor stops")
        void theTwoDesignsDisagreeOnAirFreight() {
            // The consequence, stated as a test: the same catalog, the same
            // question, and one of the two answers puts an undeclared
            // lithium cell on an aircraft.
            boolean naiveSaysKitIsClear = naiveAudit().stream()
                    .noneMatch(finding -> finding.contains("KIT-01"));

            ComplianceAuditVisitor visitor = new ComplianceAuditVisitor();
            pattern().accept(visitor);

            assertTrue(naiveSaysKitIsClear);
            assertFalse(visitor.clearForAir());
        }

        @Test
        @DisplayName("the bundle's restriction field is never set, which is the bug")
        void theFieldIsNeverSet() {
            NaiveBundle kit = new NaiveBundle("K", "Kit", Money.pounds(50), 1)
                    .containing(new NaiveProduct("A", "Battery", Money.pounds(1), 1,
                            Restriction.LITHIUM_BATTERY));

            List<String> findings = new ArrayList<>();
            kit.auditInto(findings, "Kits");

            // A kit containing nothing but a lithium cell reports clear.
            assertEquals(List.of(), findings);
        }
    }

    @Nested
    @DisplayName("the shape of the two designs")
    class Shape {

        @Test
        @DisplayName("the naive node interface is four reports and one domain method")
        void reportsOnTheModel() {
            List<String> names = new ArrayList<>();
            for (Method method : NaiveCatalogNode.class.getDeclaredMethods()) {
                names.add(method.getName());
            }
            assertTrue(names.contains("inventoryValue"));
            assertTrue(names.contains("appendCsvTo"));
            assertTrue(names.contains("auditInto"));
            assertTrue(names.contains("countInto"));
        }

        @Test
        @DisplayName("the pattern's node interface is two methods, and neither is a report")
        void noReportsOnTheModel() {
            List<String> names = new ArrayList<>();
            for (Method method : CatalogComponent.class.getDeclaredMethods()) {
                names.add(method.getName());
            }
            assertEquals(List.of("name", "accept"), names.stream().sorted().toList().reversed());
        }

        @Test
        @DisplayName("the traversal is written four times in the naive design")
        void traversalIsRepeated() {
            // Four report methods on NaiveCategory, and each one contains
            // its own loop over the children. In the pattern version the
            // loop exists once, in Category.accept.
            int loops = 0;
            for (Method method : NaiveCategory.class.getDeclaredMethods()) {
                if (!method.getName().equals("name") && !method.getName().equals("add")) {
                    loops++;
                }
            }
            assertEquals(4, loops);
        }
    }
}
