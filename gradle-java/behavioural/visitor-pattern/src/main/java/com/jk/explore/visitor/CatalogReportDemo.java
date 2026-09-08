package com.jk.explore.visitor;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Runnable entry point: five sections, in the order the argument is made.
 *
 * <p>Section 1 asks the naive catalog for its four reports and shows two of
 * them answering wrongly. Section 2 asks the same four questions of the same
 * tree through visitors. Section 3 makes the dispatch visible, because the
 * mechanism is the part nobody believes on first reading. Section 4 writes a
 * fifth report inside this file, to show that "no change to the model" is a
 * property of the design and not a claim about the four that shipped with
 * it. Section 5 says what the pattern cost.
 */
public final class CatalogReportDemo {

    public static void main(String[] args) {
        trap();
        pattern();
        dispatch();
        fifthReport();
        cost();
    }

    // ---------------------------------------------------------------- 1

    private static void trap() {
        System.out.println("=== 1. The trap: four reports, written on the model ===\n");

        NaiveCategory tree = Catalog.naiveDemoTree();

        System.out.println("  Report 1 - inventory value: " + tree.inventoryValue());
        System.out.println("  Report 2 - lines in Electronics/Accessories: "
                + countsOf(tree).get("Electronics/Accessories"));
        System.out.println("  Both correct. Two methods on three classes, and nobody minded.\n");

        StringBuilder csv = new StringBuilder();
        tree.appendCsvTo(csv, "");
        System.out.println("  Report 3 - the CSV export, two rows of it:");
        for (String row : csv.toString().split("\n")) {
            if (row.contains("CLN-003") || row.contains("KIT-01")) {
                System.out.println("    " + row + "   (" + fields(row) + " fields)");
            }
        }
        System.out.println("  NaiveProduct quotes its fields. NaiveBundle was copied");
        System.out.println("  from it and the quoting was dropped, because on that day");
        System.out.println("  no kit had a comma in its name. Marketing added one.\n");

        List<String> findings = new ArrayList<>();
        tree.auditInto(findings, "");
        System.out.println("  Report 4 - the compliance audit, " + findings.size() + " findings:");
        for (String finding : findings) {
            System.out.println("    " + finding);
        }
        System.out.println("  The Starter Kit has a lithium cell in the box and is not");
        System.out.println("  on the list. NaiveBundle.auditInto reads a restriction");
        System.out.println("  field it copied from NaiveProduct and never sets. The");
        System.out.println("  shipment is filed as clear for air freight.\n");
    }

    // ---------------------------------------------------------------- 2

    private static void pattern() {
        System.out.println("=== 2. The pattern: the same four reports, as visitors ===\n");

        Category tree = Catalog.demoTree();

        InventoryValueVisitor value = new InventoryValueVisitor();
        tree.accept(value);
        System.out.printf("  Report 1 - inventory value: %s across %d lines, %d units%n%n",
                value.total(), value.lines(), value.units());

        CategoryCountVisitor counts = new CategoryCountVisitor();
        tree.accept(counts);
        System.out.println("  Report 2 - lines by category:");
        Map<String, Integer> direct = counts.directCounts();
        for (Map.Entry<String, Integer> entry : counts.totalCounts().entrySet()) {
            System.out.printf("    %-30s %2d here %3d in total%n",
                    entry.getKey(), direct.get(entry.getKey()), entry.getValue());
        }
        System.out.println("  Clearance is empty and still on the report, because the");
        System.out.println("  category is registered on the way in rather than by a");
        System.out.println("  product mentioning it.\n");

        CsvExportVisitor csv = new CsvExportVisitor();
        tree.accept(csv);
        System.out.println("  Report 3 - the CSV export, the same two rows:");
        for (String row : csv.rows()) {
            if (row.contains("CLN-003") || row.contains("KIT-01")) {
                System.out.println("    " + row + "   (" + fields(row) + " fields)");
            }
        }
        System.out.println("  One quoting rule, in one class, applied to every node.\n");

        ComplianceAuditVisitor audit = new ComplianceAuditVisitor();
        tree.accept(audit);
        System.out.println("  Report 4 - the compliance audit, " + audit.findings().size()
                + " findings from " + audit.itemsChecked() + " lines:");
        for (String finding : audit.findings()) {
            System.out.println("    " + finding);
        }
        System.out.println("  clear for air freight: " + audit.clearForAir());
        System.out.println("  The kit is on the list. visit(Bundle) is a different");
        System.out.println("  method from visit(Product), so the rule that a bundle");
        System.out.println("  inherits what is in the box had somewhere to be written.\n");

        System.out.println("  Four reports. Product.java, Bundle.java and Category.java");
        System.out.println("  have one method between them about reporting, and it is");
        System.out.println("  the same method on all three: accept.\n");
    }

    // ---------------------------------------------------------------- 3

    private static void dispatch() {
        System.out.println("=== 3. How each node found its method ===\n");

        DispatchTraceVisitor trace = new DispatchTraceVisitor();
        Catalog.demoTree().accept(trace);
        for (String line : trace.trace()) {
            System.out.println("  " + line);
        }
        System.out.printf("%n  %d categories, %d products, %d bundle, and no instanceof.%n",
                trace.categories(), trace.products(), trace.bundles());
        System.out.println("  Each node called visitor.visit(this) from inside its own");
        System.out.println("  class, where the compiler knows what this is. That bounce");
        System.out.println("  through accept is the double dispatch, and it is the price");
        System.out.println("  of the type test never being written.\n");
        System.out.println("  The order came from Category.accept, once, and every");
        System.out.println("  report above walked the tree in exactly this order.\n");
    }

    // ---------------------------------------------------------------- 4

    /**
     * The fifth report, and the point of the section: it is declared here,
     * in the demo file, below {@code main}. No file in the model was opened
     * to add it.
     */
    private static final class LowStockVisitor implements CatalogVisitor {

        private final int threshold;
        private final List<String> shortages = new ArrayList<>();
        private Money atRisk = Money.zero();

        private LowStockVisitor(int threshold) {
            this.threshold = threshold;
        }

        @Override
        public void visit(Product product) {
            consider(product.name(), product.stockOnHand(), product.price());
        }

        @Override
        public void visit(Bundle bundle) {
            // A kit is short if the kit is short. Its contents are counted
            // as their own lines elsewhere in the tree.
            consider(bundle.name(), bundle.stockOnHand(), bundle.price());
        }

        @Override
        public void visit(Category category) {
        }

        private void consider(String name, int stock, Money price) {
            if (stock < threshold) {
                shortages.add(String.format("%-22s %3d left, %s a unit", name, stock, price));
                atRisk = atRisk.plus(price.times(threshold - stock));
            }
        }
    }

    private static void fifthReport() {
        System.out.println("=== 4. A fifth report, asked for this morning ===\n");

        LowStockVisitor lowStock = new LowStockVisitor(100);
        Catalog.demoTree().accept(lowStock);
        for (String line : lowStock.shortages) {
            System.out.println("    " + line);
        }
        System.out.printf("%n  %s of cover to buy back to 100 units.%n%n", lowStock.atRisk);
        System.out.println("  LowStockVisitor is a private class inside this demo file.");
        System.out.println("  Adding it changed no interface, no node type and no other");
        System.out.println("  report. In the naive design it is a fifth method on");
        System.out.println("  NaiveCatalogNode and three more implementations of it.\n");
    }

    // ---------------------------------------------------------------- 5

    private static void cost() {
        System.out.println("=== 5. What it cost ===\n");

        List<CatalogVisitor> written = List.of(
                new InventoryValueVisitor(), new CategoryCountVisitor(),
                new CsvExportVisitor(), new ComplianceAuditVisitor(),
                new DispatchTraceVisitor(), new LowStockVisitor(100));

        System.out.println("  Add one node type -- a gift card, say -- and CatalogVisitor");
        System.out.println("  gains a method. These stop compiling until it is written:");
        for (CatalogVisitor visitor : written) {
            System.out.println("    " + visitor.getClass().getSimpleName());
        }
        System.out.println("  Six today, and the list only ever grows. The naive design");
        System.out.println("  takes a new node type in its stride: one new class, and");
        System.out.println("  nothing else recompiles. That is the trade, and it is not");
        System.out.println("  a small one.\n");

        Category empty = new Category("Clearance");
        InventoryValueVisitor value = new InventoryValueVisitor();
        empty.accept(value);
        System.out.println("  A visitor cannot stop early: " + value.lines()
                + " lines from an empty category,");
        System.out.println("  but a report wanting only Accessories still walks all of");
        System.out.println("  Electronics. The traversal lives in Category.accept, which");
        System.out.println("  is what stops six reports each getting it slightly wrong,");
        System.out.println("  and it is also what takes pruning away from them.\n");

        System.out.println("  And node.accept(v) calling v.visit(node) straight back is");
        System.out.println("  not obvious code. Two calls to reach one method, and the");
        System.out.println("  reason is a fact about how Java picks overloads.\n");

        System.out.println("  Use this when the node types are settled and the reports");
        System.out.println("  are not. In a catalog that is true. Reach for it in a");
        System.out.println("  hierarchy that is still growing types and you will spend");
        System.out.println("  every sprint editing every visitor.");
    }

    // ---------------------------------------------------------------- util

    private static Map<String, Integer> countsOf(NaiveCategory tree) {
        Map<String, Integer> counts = new LinkedHashMap<>();
        tree.countInto(counts, "");
        return counts;
    }

    /** How many columns a spreadsheet would read in this row. */
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
}
