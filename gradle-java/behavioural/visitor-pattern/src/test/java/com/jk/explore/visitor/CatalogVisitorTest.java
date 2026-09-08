package com.jk.explore.visitor;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;

/**
 * The mechanism, not the reports.
 *
 * <p>Every test here would still pass against a catalog whose reports were
 * written as methods on the nodes — except that most of them could not be
 * written at all. That is the point of the class: it asserts the things
 * only Visitor gives you. A test that checks an inventory total proves
 * nothing about the pattern, and lives in {@link ReportVisitorTest}.
 */
class CatalogVisitorTest {

    /** Records every call, so a test can assert what ran and in what order. */
    private static final class RecordingVisitor implements CatalogVisitor {

        private final List<String> calls = new ArrayList<>();

        @Override
        public void visit(Product product) {
            calls.add("product:" + product.name());
        }

        @Override
        public void visit(Bundle bundle) {
            calls.add("bundle:" + bundle.name());
        }

        @Override
        public void visit(Category category) {
            calls.add("enter:" + category.name());
        }

        @Override
        public void leave(Category category) {
            calls.add("leave:" + category.name());
        }
    }

    private static Product product(String name) {
        return new Product("SKU-" + name, name, Money.pounds(10), 1);
    }

    @Nested
    @DisplayName("double dispatch")
    class DoubleDispatch {

        @Test
        @DisplayName("a product reaches visit(Product), not visit(Category)")
        void productDispatchesToProduct() {
            RecordingVisitor visitor = new RecordingVisitor();
            product("Case").accept(visitor);
            assertEquals(List.of("product:Case"), visitor.calls);
        }

        @Test
        @DisplayName("a bundle reaches visit(Bundle), not visit(Product)")
        void bundleDispatchesToBundle() {
            RecordingVisitor visitor = new RecordingVisitor();
            new Bundle("KIT", "Kit", Money.pounds(50), 3).accept(visitor);
            assertEquals(List.of("bundle:Kit"), visitor.calls);
        }

        @Test
        @DisplayName("a category reaches visit(Category)")
        void categoryDispatchesToCategory() {
            RecordingVisitor visitor = new RecordingVisitor();
            new Category("Cables").accept(visitor);
            assertEquals(List.of("enter:Cables", "leave:Cables"), visitor.calls);
        }

        @Test
        @DisplayName("dispatch is by runtime type through a CatalogComponent reference")
        void dispatchesThroughTheInterface() {
            // The compiler cannot pick the overload here: the static type is
            // CatalogComponent. accept() is what makes it work anyway, and
            // this is the test that says so.
            List<CatalogComponent> nodes = List.of(
                    product("Case"),
                    new Bundle("KIT", "Kit", Money.pounds(50), 3),
                    new Category("Cables"));

            RecordingVisitor visitor = new RecordingVisitor();
            for (CatalogComponent node : nodes) {
                node.accept(visitor);
            }

            assertEquals(List.of("product:Case", "bundle:Kit", "enter:Cables", "leave:Cables"),
                    visitor.calls);
        }

        @Test
        @DisplayName("a bundle's contents are not visited as nodes")
        void bundleContentsAreNotNodes() {
            Bundle kit = new Bundle("KIT", "Kit", Money.pounds(50), 3)
                    .containing(product("Phone"))
                    .containing(product("Case"));

            RecordingVisitor visitor = new RecordingVisitor();
            kit.accept(visitor);

            // One call, not three. If the box were walked, every report
            // that adds stock up would count the phone twice.
            assertEquals(List.of("bundle:Kit"), visitor.calls);
        }
    }

    @Nested
    @DisplayName("traversal")
    class Traversal {

        @Test
        @DisplayName("depth first, parent before children")
        void parentBeforeChildren() {
            Category tree = new Category("Electronics")
                    .add(product("Phone"))
                    .add(new Category("Cables").add(product("USB-C")));

            RecordingVisitor visitor = new RecordingVisitor();
            tree.accept(visitor);

            assertEquals(List.of("enter:Electronics", "product:Phone",
                    "enter:Cables", "product:USB-C", "leave:Cables",
                    "leave:Electronics"), visitor.calls);
        }

        @Test
        @DisplayName("siblings in insertion order")
        void siblingsInInsertionOrder() {
            Category tree = new Category("Accessories")
                    .add(product("Case"))
                    .add(product("Charger"))
                    .add(product("Cable"));

            RecordingVisitor visitor = new RecordingVisitor();
            tree.accept(visitor);

            assertEquals(List.of("enter:Accessories", "product:Case",
                    "product:Charger", "product:Cable", "leave:Accessories"),
                    visitor.calls);
        }

        @Test
        @DisplayName("every enter has a matching leave, innermost first")
        void entersAndLeavesAreBalanced() {
            RecordingVisitor visitor = new RecordingVisitor();
            Catalog.demoTree().accept(visitor);

            int depth = 0;
            for (String call : visitor.calls) {
                if (call.startsWith("enter:")) {
                    depth++;
                } else if (call.startsWith("leave:")) {
                    depth--;
                }
                assertTrue(depth >= 0, "leave without a matching enter: " + call);
            }
            assertEquals(0, depth, "the walk ended inside a category");
        }

        @Test
        @DisplayName("the order is the same on every walk")
        void orderIsStable() {
            RecordingVisitor first = new RecordingVisitor();
            RecordingVisitor second = new RecordingVisitor();
            Category tree = Catalog.demoTree();

            tree.accept(first);
            tree.accept(second);

            // A CSV export that reorders itself between runs cannot be
            // diffed, so this is a requirement and not an accident.
            assertEquals(first.calls, second.calls);
        }

        @Test
        @DisplayName("an empty category is still entered and left")
        void emptyCategoryIsStillVisited() {
            RecordingVisitor visitor = new RecordingVisitor();
            new Category("Clearance").accept(visitor);
            assertEquals(List.of("enter:Clearance", "leave:Clearance"), visitor.calls);
        }

        @Test
        @DisplayName("no visitor writes traversal code")
        void traversalIsNotInTheVisitor() {
            // The recording visitor above has no loop and no recursion, and
            // it still saw all seventeen calls of the demo tree.
            RecordingVisitor visitor = new RecordingVisitor();
            Catalog.demoTree().accept(visitor);
            assertEquals(17, visitor.calls.size());
        }

        @Test
        @DisplayName("leave is optional")
        void leaveIsADefaultMethod() {
            // A visitor that implements only the three visit methods still
            // compiles and still walks the whole tree.
            class ValueOnly implements CatalogVisitor {
                int seen;

                @Override
                public void visit(Product product) {
                    seen++;
                }

                @Override
                public void visit(Bundle bundle) {
                    seen++;
                }

                @Override
                public void visit(Category category) {
                }
            }

            ValueOnly visitor = new ValueOnly();
            Catalog.demoTree().accept(visitor);
            assertEquals(7, visitor.seen);
        }
    }

    @Nested
    @DisplayName("extension without modification")
    class Extension {

        @Test
        @DisplayName("a report declared in this test file walks a tree compiled without it")
        void aReportWrittenLaterStillWorks() {
            // The whole claim of the pattern, as one test. This class did
            // not exist when Product, Bundle and Category were compiled.
            class LongestNameVisitor implements CatalogVisitor {
                String longest = "";

                @Override
                public void visit(Product product) {
                    consider(product.name());
                }

                @Override
                public void visit(Bundle bundle) {
                    consider(bundle.name());
                }

                @Override
                public void visit(Category category) {
                    consider(category.name());
                }

                private void consider(String name) {
                    if (name.length() > longest.length()) {
                        longest = name;
                    }
                }
            }

            LongestNameVisitor visitor = new LongestNameVisitor();
            Catalog.demoTree().accept(visitor);

            assertEquals("Screen Cleaner, 200ml", visitor.longest);
        }

        @Test
        @DisplayName("the model carries no report methods")
        void theModelHasNoReportingMethods() {
            // Named for what it is: a guard. If a future report is added by
            // putting a method on Product because that was quicker, this
            // fails and says why.
            List<String> allowed = List.of("name", "sku", "price", "stockOnHand",
                    "restriction", "accept", "toString", "equals", "hashCode");

            for (Method method : Product.class.getDeclaredMethods()) {
                if (method.isSynthetic()) {
                    continue;
                }
                assertTrue(allowed.contains(method.getName()),
                        "Product grew a method that is not about being a product: "
                                + method.getName());
            }
        }

        @Test
        @DisplayName("adding a report changes no existing report")
        void reportsDoNotSeeEachOther() {
            Category tree = Catalog.demoTree();

            InventoryValueVisitor before = new InventoryValueVisitor();
            tree.accept(before);

            DispatchTraceVisitor other = new DispatchTraceVisitor();
            tree.accept(other);

            InventoryValueVisitor after = new InventoryValueVisitor();
            tree.accept(after);

            assertEquals(before.total(), after.total());
        }

        @Test
        @DisplayName("the same visitor instance can walk two trees, accumulating")
        void aVisitorAccumulatesAcrossTrees() {
            InventoryValueVisitor visitor = new InventoryValueVisitor();
            Category one = new Category("A").add(new Product("P1", "Case", Money.pounds(10), 2));
            Category two = new Category("B").add(new Product("P2", "Charger", Money.pounds(5), 4));

            one.accept(visitor);
            two.accept(visitor);

            assertEquals(Money.pounds(40), visitor.total());
        }
    }

    @Nested
    @DisplayName("the cost, asserted rather than claimed")
    class Cost {

        @Test
        @DisplayName("one visit method per node type, and nothing else")
        void theInterfaceHasOneMethodPerNodeType() {
            List<String> visits = new ArrayList<>();
            for (Method method : CatalogVisitor.class.getDeclaredMethods()) {
                if (method.getName().equals("visit")) {
                    visits.add(method.getParameterTypes()[0].getSimpleName());
                }
            }

            // Three node types, three methods. A fourth node type means a
            // fourth method here, and that is the cost the README states:
            // every implementation stops compiling until it is written.
            assertEquals(3, visits.size());
            assertTrue(visits.contains("Product"));
            assertTrue(visits.contains("Bundle"));
            assertTrue(visits.contains("Category"));
        }

        @Test
        @DisplayName("a visitor cannot prune the walk")
        void aVisitorSeesTheWholeTree() {
            class AccessoriesOnly extends CategoryPathVisitor {
                int visitedAnywhere;
                int visitedUnderAccessories;

                @Override
                public void visit(Product product) {
                    visitedAnywhere++;
                    if (path().contains("Accessories")) {
                        visitedUnderAccessories++;
                    }
                }

                @Override
                public void visit(Bundle bundle) {
                    visitedAnywhere++;
                }
            }

            AccessoriesOnly visitor = new AccessoriesOnly();
            Catalog.demoTree().accept(visitor);

            // It wanted five nodes and was handed seven. Filtering is the
            // only option, because the traversal is not its to control.
            assertEquals(7, visitor.visitedAnywhere);
            assertEquals(5, visitor.visitedUnderAccessories);
            assertFalse(visitor.visitedAnywhere == visitor.visitedUnderAccessories);
        }
    }
}
