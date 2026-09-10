"""Scene definitions for the Visitor teaching video.

Each scene has:
  key        - short id, used for the generated file names
  title      - slide heading
  kind       - "poster" | "bullets" | "code" | "console" | "quote" | "diagram" | "outro"
  body       - content, meaning depends on kind
  narration  - the text spoken by the narrator (see narration.md)
"""

SCENES = [
    # The poster is also the YouTube thumbnail, so it is the first frame of
    # the video and is saved separately as poster.png by build_video.sh.
    dict(
        key="01-poster",
        kind="poster",
        title="Visitor",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Visitor design pattern "
            "in Java, and it is written and presented by Jayasekhar Konduru. "
            "[[slnc 300]] Let's start with the simple definition. Visitor lets "
            "you add a new operation to a set of objects without changing those "
            "objects. You write the operation as a class of its own — a visitor — "
            "and hand it to each object in turn, and each object calls back the "
            "one method on it that fits its own type. The objects stay as they "
            "are; the new behaviour arrives from outside. [[slnc 350]] That's the "
            "idea in a sentence. The rest of the video does it properly, in an "
            "online shop, where the catalog is a tree of categories, products and "
            "bundles and the business keeps asking new questions about it — what "
            "the stock is worth, what sits in each category, a spreadsheet for "
            "finance, and which items can't simply be put in a box and posted. "
            "Each of those questions becomes a visitor. [[slnc 300]] By the end "
            "you'll know what double dispatch is and why Java needs two method "
            "calls to get it, and — more useful — when this pattern is the wrong "
            "answer."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "The catalog is a tree. It has been for years:",
            "",
            "  Electronics/",
            "    Phone                       Accessories/",
            "      Case  Charger  Battery  Cleaner  Cables/",
            "    Kits/  ->  Starter Kit     Clearance/  (empty)",
            "",
            "What changes is what the business asks about it:",
            "",
            "  inventory value    count by category",
            "  CSV export         compliance audit",
        ],
        narration=(
            "So, the catalog. It's a tree: categories hold products and other "
            "categories, and it has looked like that since the shop opened. If "
            "you've done the composite project in this series, this is literally "
            "that tree. [[slnc 300]] What changes is not the tree. It's what the "
            "business wants to know about it. Finance wants the value of the "
            "stock, and a spreadsheet every Monday. Merchandising wants the lines "
            "in each category. Shipping wants to know which items can't simply be "
            "put in a box and posted. [[slnc 300]] Four questions, one structure "
            "— and next month there will be a fifth. Hold on to that shape, "
            "because it's the only condition under which today's pattern is worth "
            "its cost."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Two Kinds of Node, and They Are Not Alike",
        body=[
            "Product      one item on the shelf",
            "             price, stock, restriction",
            "",
            "Bundle       a kit sold as one thing",
            "             its own price, and contents",
            "",
            "Inventory value:",
            "  product  ->  price x stock",
            "  bundle   ->  KIT price x stock, not the sum of the parts",
            "",
            "Compliance:",
            "  product  ->  its own restriction",
            "  bundle   ->  every restriction in the box",
        ],
        narration=(
            "Before any of the design, look at two nodes, because the whole video "
            "turns on the difference between them. [[slnc 250]] A product is one "
            "item on the shelf: a price, a stock level, and possibly a "
            "restriction — a lithium cell, say, which needs a dangerous goods "
            "declaration if it flies. A bundle is a kit sold as one thing: the "
            "starter kit is a phone, a case and a spare battery, at six hundred "
            "and thirty nine pounds. [[slnc 300]] Now ask both the same two "
            "questions. What are you worth? A product is price times stock. A "
            "bundle is its kit price times stock — not the sum of its parts, "
            "because the point of a bundle is that it costs less than the parts. "
            "[[slnc 300]] And: are you restricted? A product is, or it isn't. One "
            "field. A bundle has no restriction of its own — it's restricted by "
            "what's in the box. [[slnc 300]] Two node types, two genuinely "
            "different rules, twice over."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — A Method Per Report",
        body="""public interface NaiveCatalogNode {
    String name();

    Money inventoryValue();
    void  countInto(Map<String, Integer> counts, String path);
    void  appendCsvTo(StringBuilder out, String path);
    void  auditInto(List<String> findings, String path);
}

// NaiveProduct — a class about a thing on a shelf
private static String quote(String field) {
    if (field.indexOf(',') < 0 && field.indexOf('"') < 0) return field;
    return '"' + field.replace("\\"", "\\"\\"") + '"';
}""",
        narration=(
            "Written the obvious way, a report is a method on the node. [[slnc "
            "250]] Here's the interface after four of them. Read the list and ask "
            "which of these is about a catalog. Name, obviously. Inventory value, "
            "arguably. [[slnc 300]] But append C S V to? That's not about a "
            "product. That's a rule from a nineteen nineties file format: a field "
            "containing a comma gets wrapped in quotes, and a quote inside it "
            "gets doubled. And underneath, there it is — a private quote method, "
            "on a class whose job is to describe a thing on a shelf. [[slnc 300]] "
            "I want to be fair to this design, because it isn't stupid. Each "
            "method is the shortest correct way to answer its question, and the "
            "demo proves it: the naive inventory value and the visitor inventory "
            "value agree to the penny. [[slnc 300]] Everything that follows is "
            "about the fourth report, and the third year."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "1. A report is a change to the domain model.",
            "   The quoting rule now lives in two node classes.",
            "",
            "2. Knowing it twice is how it gets known differently.",
            "   NaiveBundle was copied. The quoting was dropped.",
            "   \"Starter Kit, 3 items\"  ->  a row with 8 fields, not 7.",
            "",
            "3. And the copy that matters is the compliance one.",
            "   It reads a restriction field that is never set.",
            "   The kit with a lithium cell: not on the report.",
            "",
            "4. Every report writes the traversal again.",
            "",
            "5. Report five edits three finished classes.",
        ],
        narration=(
            "So here's what goes wrong, and it goes wrong in a particular order. "
            "[[slnc 250]] One. A report is now a change to the domain model — the "
            "quoting rule lives in two node classes, because the bundle needed "
            "one too. [[slnc 300]] Two. Knowing something twice is how it comes "
            "to be known differently. The bundle class was written eighteen "
            "months later, by copying the product class, and the copy dropped the "
            "quoting calls. Nothing failed — no kit had a comma in its name that "
            "year. Then marketing renamed the kit to Starter Kit, comma, three "
            "items, and one row of the finance spreadsheet quietly gained a "
            "column. [[slnc 350]] Three, and this is the one that matters. The "
            "compliance check was copied too. The product version reads the "
            "product's restriction field, so the bundle version reads its own "
            "restriction field — which came across with the copy and is never "
            "set. So the starter kit, with a lithium cell in the box, is not on "
            "the dangerous goods report, and a shipment goes out filed as clear "
            "for air freight. [[slnc 300]] Nobody wrote that bug, and the "
            "interface couldn't have caught it: it says the method exists, and "
            "both classes have one. [[slnc 300]] Four. Every report on the "
            "category class is the same loop with a different body. And five: the "
            "fifth report is a fifth method, and three more implementations of "
            "it."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Visitor Pattern",
        body=[
            "\"Represent an operation to be performed on the",
            " elements of an object structure. Visitor lets you",
            " define a new operation without changing the classes",
            " of the elements on which it operates.\"",
            "",
            "        — Gang of Four, Design Patterns, 1994",
            "",
            "Read the second sentence again. It is a promise",
            "about change — and about one direction of change.",
        ],
        narration=(
            "The Gang of Four define it like this. Represent an operation to be "
            "performed on the elements of an object structure. Visitor lets you "
            "define a new operation without changing the classes of the elements "
            "on which it operates. [[slnc 350]] Read that second sentence again, "
            "because it's a promise about change, not about structure. This isn't "
            "a way of walking a tree — composite already walks the tree. It's a "
            "way of deciding which of your two axes of change is going to be "
            "cheap. [[slnc 300]] And notice what the definition is careful not to "
            "say. It says nothing at all about new element types, and that "
            "silence is the whole cost of the pattern."
        ),
    ),
    dict(
        key="07-analogy",
        kind="bullets",
        title="An Analogy",
        body=[
            "A building, and the people who come to inspect it.",
            "",
            "  the fire officer     checks the exits",
            "  the valuer           estimates what it is worth",
            "  the census taker     counts the occupants",
            "",
            "The caretaker walks each of them the same route,",
            "and opens the same doors, in the same order.",
            "",
            "A new kind of inspector: hire one. Nothing changes.",
            "A new kind of room: every inspector needs training.",
        ],
        narration=(
            "Here's how I'd explain this at a whiteboard. [[slnc 250]] Think "
            "about a building, and the people who come to inspect it. The fire "
            "officer checks the exits. The valuer estimates what it's worth. The "
            "census taker counts the occupants. Three completely different jobs. "
            "[[slnc 300]] And the caretaker walks each of them the same route, "
            "through the same doors, in the same order. The caretaker doesn't "
            "care what they're looking for, and the inspectors don't know the "
            "layout. [[slnc 350]] Now a new kind of inspector turns up. An "
            "accessibility auditor. You hire one, they join the walk, and nothing "
            "in the building changes. That's the benefit, and it's real. [[slnc "
            "300]] But add a new kind of room — a plant room, a server room — and "
            "every single inspector needs to be told what to do standing in it. "
            "Every one. That's the bill, and it arrives every time the building "
            "changes shape."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            "Here are the pieces, and the shape to take away is two hierarchies "
            "side by side. [[slnc 300]] On the left, the catalog: three node "
            "types, product, bundle and category. That hierarchy is finished, and "
            "has been for years. On the right, the reports: a catalog visitor "
            "interface, and under it the four the business asked for, plus a "
            "trace and a low stock report. Six classes, growing every month. "
            "[[slnc 300]] Between them, one arrow, and it points in the direction "
            "that surprises people. The structure depends on the visitor "
            "interface, while no node knows that any concrete report exists. "
            "That's what lets me declare a report inside a test file and have it "
            "walk a tree compiled without it. [[slnc 300]] Count the boxes. Three "
            "and six. Adding to the six is free; adding to the three costs an "
            "edit to all six. Those two numbers are the entire argument for and "
            "against this pattern."
        ),
    ),
    dict(
        key="09-interface",
        kind="code",
        title="The Element and the Visitor",
        body="""public interface CatalogComponent {
    String name();
    void accept(CatalogVisitor visitor);
}

public interface CatalogVisitor {
    void visit(Product product);
    void visit(Bundle bundle);
    void visit(Category category);

    default void leave(Category category) { }
}

// Product.java, Bundle.java, Category.java — the same line, three times
@Override
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);
}""",
        narration=(
            "Here is the whole pattern, and it's smaller than its reputation "
            "suggests. [[slnc 250]] The element interface has two methods. Name, "
            "and accept, which hands the node to a visitor. That's the last "
            "method this interface will ever need. [[slnc 300]] The visitor "
            "interface has one visit method per node type. Three methods with the "
            "same name, distinguished only by their parameter — ordinary Java "
            "overloading, and it's the mechanism the whole pattern runs on. "
            "[[slnc 300]] Leave is a default method, called on the way back out "
            "of a category, because a tree walk has two moments at a branch and a "
            "report that tracks which category it's in needs both. [[slnc 350]] "
            "And at the bottom, accept. One line, the same line in all three node "
            "classes. [[slnc 250]] Which raises the obvious objection: if it's "
            "the same line three times, why isn't it one line in one place? "
            "That's the next slide, and it's the only genuinely hard idea here."
        ),
    ),
    dict(
        key="10-context",
        kind="code",
        title="Why accept Has To Exist",
        body="""CatalogComponent node = new Product("PHN-900", "Phone", ...);

visitor.visit(node);      // does NOT compile
                          // overloads are picked from the STATIC type,
                          // and there is no visit(CatalogComponent)

// inside Product.java — here, `this` is a Product
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);  // compiles, to visit(Product)
}

node.accept(v)   ->  runtime picks the node    (dynamic dispatch)
   v.visit(this) ->  compiler picks the report (overload resolution)""",
        narration=(
            "Take a node, held in a variable of type catalog component, and try "
            "to call visit on it directly. It does not compile. [[slnc 300]] Java "
            "picks between overloaded methods using the static type of the "
            "argument — what the compiler can see at that line — and there, all "
            "it can see is a catalog component. There's no visit that takes one, "
            "and the compiler will not guess. It does not matter that the object "
            "really is a product. [[slnc 350]] Now move the same call inside the "
            "product class. In that file, this is a product. The compiler knows "
            "the type and picks visit of product. [[slnc 300]] So the two hops do "
            "two different jobs. Node dot accept is dynamic dispatch at runtime, "
            "picking which node we're on. Visitor dot visit of this is overload "
            "resolution at compile time, picking which report method runs. "
            "Together they select a method from two types at once, and that is "
            "double dispatch. [[slnc 350]] Is it awkward to read? Yes, and the "
            "reason is a fact about Java's overload rules rather than a fact "
            "about catalogs. That cost is paid on every read, and the only thing "
            "justifying it is the number of reports on the other side of the "
            "ledger."
        ),
    ),
    dict(
        key="11-links",
        kind="code",
        title="The Walk, and Two Reports",
        body="""// Category — the walk, written ONCE, for every report there will ever be
public void accept(CatalogVisitor visitor) {
    visitor.visit(this);
    for (CatalogComponent child : children) child.accept(visitor);
    visitor.leave(this);
}

// InventoryValueVisitor — two node types, two plain sentences
public void visit(Product p) { total = total.plus(p.price().times(p.stockOnHand())); }
public void visit(Bundle  b) { total = total.plus(b.price().times(b.stockOnHand())); }

// ComplianceAuditVisitor — the rule that had nowhere to live
public void visit(Bundle bundle) {
    for (Product content : bundle.contents())
        if (content.restriction().isRestricted()) record(...);
}""",
        narration=(
            "Three pieces of real code. [[slnc 250]] At the top, the walk. The "
            "category visits itself, hands the visitor to each child, then says "
            "it's leaving. Depth first, siblings in the order they were added, "
            "and the same order on every run — because a spreadsheet that "
            "reorders itself between runs can't be compared with yesterday's. "
            "That's written once, and every report gets it free, including the "
            "one you write next year. A test makes the point by counting: a "
            "visitor with no loop and no recursion in it still sees all seventeen "
            "calls. [[slnc 350]] In the middle, the inventory value. A product is "
            "worth price times stock. A bundle is worth its kit price times "
            "stock. Two plain sentences, and — this is the bit I'd point at — no "
            "if statement, and no instance of check. [[slnc 350]] At the bottom, "
            "the compliance rule the naive version lost. A bundle is restricted "
            "by what's in the box, so here's a loop over the contents. Ask where "
            "else that loop could go. There is nowhere."
        ),
    ),
    dict(
        key="12-proof",
        kind="code",
        title="The Tests — Asserting What Only Visitor Gives You",
        body="""@Test
void aReportWrittenLaterStillWorks() {
    // this class did not exist when Product and Category were compiled
    class LongestNameVisitor implements CatalogVisitor { ... }

    LongestNameVisitor visitor = new LongestNameVisitor();
    Catalog.demoTree().accept(visitor);
    assertEquals("Screen Cleaner, 200ml", visitor.longest);
}

@Test
void aVisitorSeesTheWholeTree() {          // the cost, asserted
    AccessoriesOnly visitor = new AccessoriesOnly();
    Catalog.demoTree().accept(visitor);

    assertEquals(7, visitor.visitedAnywhere);        // offered
    assertEquals(5, visitor.visitedUnderAccessories); // wanted
}""",
        narration=(
            "Two tests, because a test that checks an inventory total proves "
            "nothing about the pattern — the naive version passes that one too. "
            "[[slnc 300]] The first is the pattern's whole claim, made checkable. "
            "A report class declared inside the test file, walking a tree whose "
            "classes were compiled long before it existed. No model file was "
            "opened. If that passes, extension without modification isn't a "
            "slogan, it's a property. [[slnc 350]] The second asserts the cost, "
            "and it's deliberately in the suite. A report that only cares about "
            "accessories is offered seven nodes and wants five. It can't prune. "
            "The walk belongs to the structure, so it filters, and does the whole "
            "tour anyway."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

=== 1. The trap: four reports, written on the model ===
  Electronics/Kits,KIT-01,Starter Kit, 3 items,bundle,639.00,25,   (8 fields)
  Report 4 - the compliance audit, 2 findings:
    ... the Starter Kit is not among them

=== 2. The pattern: the same four reports, as visitors ===
  Electronics/Kits,KIT-01,"Starter Kit, 3 items",bundle,639.00,25,  (7 fields)
  Report 4 - the compliance audit, 3 findings from 7 lines:
    Electronics/Kits/Starter Kit  lithium cell  (from Spare Battery Pack)
  clear for air freight: false

=== 5. What it cost ===
  Add one node type -- these stop compiling until it is written:
    InventoryValueVisitor  CategoryCountVisitor  CsvExportVisitor
    ComplianceAuditVisitor  DispatchTraceVisitor  LowStockVisitor""",
        narration=(
            "Run it, and the two halves sit side by side. [[slnc 250]] Section "
            "one is the naive design. The bundle row has eight fields where every "
            "other row has seven, and the compliance report has two findings, and "
            "the starter kit isn't one of them. [[slnc 300]] Section two is the "
            "same catalog and the same four questions, as visitors. The bundle "
            "name is quoted, because there's one quoting rule in one class "
            "applied to every node. And the audit has three findings — the kit is "
            "on the list, with the reason: from the spare battery pack in the "
            "box. Clear for air freight, false. [[slnc 350]] Section five is the "
            "part I'd ask you not to skip. Add one node type — a gift card, say — "
            "and every one of those six classes stops compiling until a method is "
            "written on it. Six today, and that list only grows, because reports "
            "are never deleted. The naive design takes a new node type in its "
            "stride: one new class, and nothing else recompiles."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="What to Remember",
        body=[
            "accept exists because Java picks overloads from the",
            "static type. Two hops, and it is never obvious.",
            "",
            "New operation:  one new file, zero edits.",
            "New node type:  one method x every visitor. Forever.",
            "",
            "Count your own two numbers before you commit:",
            "   node types  vs  operations over them",
            "   whichever is growing is the one that must be cheap.",
            "",
            "A catalog:   3 types, 6 reports.  Use Visitor.",
            "An AST still gaining syntax:      do not.",
            "",
            "Two operations over a stable tree? Write the methods.",
        ],
        narration=(
            "So, what to take away. [[slnc 250]] Accept exists because Java picks "
            "overloads from the static type of the argument. Two hops to reach "
            "one method, and it will never be obvious to a reader who doesn't "
            "already know the pattern. Don't defend it as elegant — defend it "
            "with the ledger. [[slnc 300]] And the ledger is this. A new "
            "operation costs one new file and zero edits. A new node type costs "
            "one method on every visitor you've ever written, every time. [[slnc "
            "350]] So before you commit, count your own two numbers. How many "
            "node types, how many operations over them — and which of those grew "
            "last year? Whichever is growing is the one that has to be cheap. "
            "[[slnc 300]] For a catalog the answer is obvious. For a syntax tree "
            "still gaining features it's the other way round. That's why this "
            "pattern has the reputation it does — not because it's bad, but "
            "because it gets used on the wrong axis. [[slnc 300]] And if you have "
            "two operations over a stable tree? Write the two methods. Put them "
            "on the nodes. This project agrees with you."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "Full source, notes, diagrams and an animated walkthrough",
            "are in the repository — including the exercise that adds",
            "a GiftCard node and makes you fix all six visitors.",
        ],
        narration=(
            "That's visitor. [[slnc 250]] The full source, the written notes, "
            "the diagrams and an animated walkthrough are all in the repository "
            "— including the exercise I'd most recommend, and it's the "
            "unpleasant one. Add a gift card node type, then fix every visitor "
            "the compiler shouts at you about. Count how many needed a real "
            "rule, and how many just got an empty method to make the build go "
            "green. [[slnc 300]] If this helped, a like genuinely helps other "
            "people find it, and subscribe if you'd like the rest of the "
            "behavioural series. [[slnc 250]] Thanks for watching, and I'll see "
            "you in the next one."
        ),
    ),
]
