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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Visitor pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Visitor pattern lets you '
            'add a new operation to a set of objects, without changing '
            'those objects. [[slnc 400]] You write the operation as its '
            'own class, called a visitor. [[slnc 300]] You hand it to '
            'each object in turn. [[slnc 300]] And each object calls back '
            'the one method on the visitor that fits its own type. [[slnc '
            '600]] Think of inspectors visiting a building. [[slnc 300]] '
            'A fire officer, a valuer, and a census taker each walk the '
            'same rooms. [[slnc 300]] But each one does a completely '
            "different job. [[slnc 700]] In this video, an online shop's "
            'catalog is a tree of categories, products, and bundles. '
            '[[slnc 300]] The business keeps asking new questions about '
            'it. [[slnc 300]] Each question becomes a visitor. [[slnc '
            '500]] By the end, you will know what double dispatch means. '
            '[[slnc 300]] And, more usefully, when this pattern is the '
            'wrong answer.'
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
            "Here is the scenario: the shop's catalog. [[slnc 400]] It is "
            'a tree. [[slnc 300]] Categories hold products, and other '
            'categories. [[slnc 300]] And it has looked like that since '
            'the shop opened. [[slnc 500]] What changes is not the tree. '
            '[[slnc 300]] It is the questions the business asks about it. '
            '[[slnc 400]] Finance wants the value of the stock, and a '
            'spreadsheet every Monday. [[slnc 300]] Merchandising wants a '
            'count of items in each category. [[slnc 300]] Shipping wants '
            'to know which items cannot simply be boxed and posted. '
            '[[slnc 500]] Four questions, one structure. [[slnc 300]] And '
            'next month there will be a fifth. [[slnc 300]] That shape is '
            'the only situation where this pattern is worth its cost.'
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
            "Before the design, let's compare two kinds of item, because "
            'everything depends on their difference. [[slnc 500]] A '
            'product is one item on the shelf. [[slnc 300]] It has a '
            'price, a stock level, and maybe a restriction. [[slnc 300]] '
            'For example, a lithium battery needs a dangerous goods '
            'declaration if it flies. [[slnc 400]] A bundle is a kit sold '
            'as one thing. [[slnc 300]] The starter kit is a phone, a '
            'case, and a spare battery, for six hundred and thirty-nine '
            'pounds. [[slnc 500]] Now ask both of them two questions. '
            '[[slnc 300]] First: what are you worth? [[slnc 300]] A '
            'product is its price times its stock. [[slnc 300]] A bundle '
            'is its kit price times its stock, not the sum of its parts. '
            '[[slnc 400]] Second: are you restricted? [[slnc 300]] A '
            'product either is, or is not. [[slnc 300]] A bundle has no '
            'restriction of its own. [[slnc 300]] It is restricted by '
            'what is inside the box.'
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
            'The obvious approach is to add each report as a method on '
            'the catalog items. [[slnc 500]] After four reports, the '
            'shared interface has methods for value, counting, '
            'spreadsheet export, and the compliance audit. [[slnc 400]] '
            'Is spreadsheet export really about a product? [[slnc 300]] '
            'No. [[slnc 300]] It is a rule from a file format. [[slnc '
            '300]] A field containing a comma must be wrapped in quotes. '
            '[[slnc 300]] Yet that rule now lives inside a class that '
            'describes a thing on a shelf. [[slnc 500]] To be fair, this '
            'design is not foolish. [[slnc 300]] Each method is the '
            'shortest correct answer to its question. [[slnc 300]] And '
            'the naive stock value matches the visitor version, to the '
            'penny. [[slnc 400]] The trouble arrives with the fourth '
            'report, in the third year.'
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
            'Here is what goes wrong, in order. [[slnc 500]] One. [[slnc '
            '200]] Every new report changes the catalog classes '
            'themselves. [[slnc 300]] The quoting rule now lives in two '
            'item classes. [[slnc 500]] Two. [[slnc 200]] Knowing '
            'something twice is how it comes to be known differently. '
            '[[slnc 300]] The bundle class was written later, by copying '
            'the product class, and the copy dropped the quoting. [[slnc '
            '300]] Then marketing renamed the kit to, Starter Kit, comma, '
            'three items. [[slnc 300]] And one row of the finance '
            'spreadsheet quietly gained an extra column. [[slnc 500]] '
            'Three, and this one really matters. [[slnc 300]] The '
            'compliance check was copied too. [[slnc 300]] The bundle '
            "version reads the bundle's own restriction, which is never "
            'set. [[slnc 300]] So the starter kit, with a lithium battery '
            'inside, is missing from the dangerous goods report. [[slnc '
            '300]] And a shipment goes out marked as safe for air '
            'freight. [[slnc 500]] Nobody wrote that bug on purpose. '
            '[[slnc 300]] And every new report means another method, in '
            'every item class.'
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
            "Here is the pattern's definition, from the famous Gang of "
            'Four book. [[slnc 400]] Represent an operation to be '
            'performed on the elements of an object structure. [[slnc '
            '300]] Visitor lets you define a new operation, without '
            'changing the classes of the elements it works on. [[slnc '
            '500]] That second sentence is a promise about change. [[slnc '
            '300]] This is not a way of walking a tree. [[slnc 300]] It '
            'is a way of choosing which kind of change will be cheap. '
            '[[slnc 500]] And notice what the definition does not say. '
            '[[slnc 300]] It says nothing about adding new kinds of '
            'element. [[slnc 300]] That silence is the whole cost of the '
            'pattern.'
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
            'Here is an analogy: a building, and the people who inspect '
            'it. [[slnc 500]] The fire officer checks the exits. [[slnc '
            '300]] The valuer estimates what it is worth. [[slnc 300]] '
            'The census taker counts the people. [[slnc 300]] Three '
            'completely different jobs. [[slnc 500]] The caretaker walks '
            'each inspector along the same route, through the same doors, '
            'in the same order. [[slnc 300]] The caretaker does not care '
            'what they are looking for. [[slnc 300]] And the inspectors '
            'do not need to know the layout. [[slnc 500]] Now a new kind '
            'of inspector arrives, an accessibility auditor. [[slnc 300]] '
            'They join the walk, and nothing in the building changes. '
            '[[slnc 300]] That is the benefit. [[slnc 500]] But add a new '
            'kind of room, like a server room. [[slnc 300]] Now every '
            'single inspector must be told what to do in it. [[slnc 300]] '
            'That is the cost, and it arrives every time the building '
            'changes shape.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Roles",
        body=None,
        narration=(
            'Here are the pieces, and the shape to remember is two '
            'families side by side. [[slnc 500]] On one side, the '
            'catalog, with three item types: product, bundle, and '
            'category. [[slnc 300]] That family is finished, and has been '
            'for years. [[slnc 500]] On the other side, the reports. '
            '[[slnc 300]] A Catalog Visitor interface, and six visitors '
            'below it. [[slnc 300]] Stock value, category count, '
            'spreadsheet export, compliance audit, a trace, and a low '
            'stock report. [[slnc 300]] That family grows every month. '
            '[[slnc 500]] The catalog only depends on the visitor '
            'interface. [[slnc 300]] No item knows that any particular '
            'report exists. [[slnc 500]] Count them: three item types, '
            'six visitors. [[slnc 300]] Adding a visitor is free. [[slnc '
            '300]] Adding an item type means editing all six visitors. '
            '[[slnc 300]] Those two numbers are the whole argument, for '
            'and against this pattern.'
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
            'Here is the whole pattern, and it is smaller than its '
            'reputation. [[slnc 500]] Every catalog item has a method '
            'called accept, which receives a visitor. [[slnc 300]] That '
            'is the last method the item interface will ever need. [[slnc '
            '500]] The visitor interface has one visit method for each '
            'item type. [[slnc 300]] Visit a product, visit a bundle, and '
            'visit a category. [[slnc 300]] They share the same name, and '
            'differ only by the type they receive. [[slnc 400]] There is '
            'also a leave method, called on the way back out of a '
            'category. [[slnc 300]] So a report can keep track of which '
            'category it is in. [[slnc 500]] And inside each item class, '
            "accept is just one line. [[slnc 300]] It calls the visitor's "
            'visit method, passing itself. [[slnc 300]] The same line, in '
            'all three classes. [[slnc 300]] So why not write it once, in '
            'one place? [[slnc 300]] That is the next question, and the '
            'only truly hard idea here.'
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
            'Imagine you have a catalog item, but your variable only says '
            'it is a catalog component. [[slnc 300]] Try calling the '
            "visitor's visit method with it directly. [[slnc 300]] It "
            'will not compile. [[slnc 500]] Java chooses between '
            'same-named methods using the type the compiler can see, at '
            'that line. [[slnc 300]] All it can see is a catalog '
            'component. [[slnc 300]] And there is no visit method for '
            'that. [[slnc 300]] It does not matter that the object really '
            'is a product. [[slnc 500]] Now move the same call inside the '
            'product class. [[slnc 300]] There, the compiler knows it is '
            'a product. [[slnc 300]] So it picks visit product. [[slnc '
            '600]] So there are two hops. [[slnc 300]] The first hop, '
            'calling accept, finds which item we are on, at run time. '
            '[[slnc 300]] The second hop, calling visit, picks which '
            'report method runs. [[slnc 300]] Together, they choose a '
            'method based on two types at once. [[slnc 300]] That is '
            'called double dispatch. [[slnc 500]] Is it awkward to read? '
            "[[slnc 300]] Yes. [[slnc 300]] That is a fact about Java's "
            'rules, not about catalogs.'
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
            'Now three pieces of real code. [[slnc 500]] First, the walk, '
            'inside the category class. [[slnc 300]] The category visits '
            'itself, then passes the visitor to each child, and then says '
            'it is leaving. [[slnc 300]] Always in the same order, so '
            "today's spreadsheet can be compared with yesterday's. [[slnc "
            '300]] That walk is written once, and every report gets it '
            'for free. [[slnc 600]] Second, the stock value report. '
            '[[slnc 300]] A product is worth its price times its stock. '
            '[[slnc 300]] A bundle is worth its kit price times its '
            'stock. [[slnc 300]] Two plain rules, with no if statements, '
            'and no type checks. [[slnc 600]] Third, the compliance rule '
            'the naive version lost. [[slnc 300]] A bundle is restricted '
            'by what is inside it. [[slnc 300]] So the visitor loops over '
            "the bundle's contents. [[slnc 300]] And that loop lives in "
            'the one report that needs it.'
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
            'Two tests are worth describing. [[slnc 300]] A test that '
            'checks the stock total proves nothing about the pattern, '
            'because the naive version passes it too. [[slnc 500]] The '
            "first test proves the pattern's promise. [[slnc 300]] A "
            'brand new report is written inside the test file. [[slnc '
            '300]] It walks a catalog whose classes were written long '
            'before it existed. [[slnc 300]] No catalog file was opened, '
            'and it works. [[slnc 600]] The second test deliberately '
            'shows a cost. [[slnc 300]] A report that only cares about '
            'accessories is offered seven items, and only wants five. '
            '[[slnc 300]] It cannot skip the rest. [[slnc 300]] The walk '
            'belongs to the catalog, so the report must filter, and still '
            'do the whole tour.'
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
            "Let's run the demo. [[slnc 500]] First, the naive design. "
            "[[slnc 300]] The bundle's spreadsheet row has eight fields, "
            'where every other row has seven. [[slnc 300]] And the '
            'compliance report has two findings, but the starter kit is '
            'not one of them. [[slnc 600]] Now the same catalog and the '
            "same four questions, as visitors. [[slnc 300]] The bundle's "
            'name is quoted correctly, because one quoting rule, in one '
            'class, handles every item. [[slnc 300]] And the audit now '
            'has three findings. [[slnc 300]] The starter kit is on the '
            'list, because of the spare battery in the box. [[slnc 300]] '
            'It is no longer marked safe for air freight. [[slnc 600]] '
            'Finally, the part not to skip. [[slnc 300]] Add one new item '
            'type, such as a gift card. [[slnc 300]] Every one of the six '
            'visitors stops compiling, until a method is written for it. '
            '[[slnc 300]] The naive design would have needed only one new '
            'class.'
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
            'So, what should you remember? [[slnc 500]] Accept exists '
            'because Java chooses methods by the type the compiler can '
            'see. [[slnc 300]] Two hops to reach one method, and it is '
            'never obvious to a new reader. [[slnc 600]] The trade is '
            'this. [[slnc 300]] A new operation costs one new file, and '
            'zero edits. [[slnc 300]] A new item type costs one method, '
            'in every visitor you have ever written. [[slnc 500]] So '
            'before you choose, count two numbers in your own code. '
            '[[slnc 300]] How many item types, and how many operations on '
            'them. [[slnc 300]] Which one grew last year? [[slnc 300]] '
            'Whichever is growing must be the cheap one. [[slnc 500]] For '
            'a shop catalog, operations grow, so Visitor fits. [[slnc '
            '300]] For something still gaining new kinds of item, it is '
            'the other way round. [[slnc 500]] And with only two '
            'operations, on a tree that never changes? [[slnc 300]] Just '
            'write the two methods, on the items.'
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
            "That's the Visitor pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] Visitor makes new '
            'operations cheap, and new item types expensive, so use it '
            'only when operations are what keep growing. [[slnc 500]] The '
            'full source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 500]] Here is '
            'one exercise to try, and it is the uncomfortable one. [[slnc '
            '300]] Add a gift card item type. [[slnc 300]] Then fix every '
            'visitor the compiler complains about. [[slnc 300]] And count '
            'how many needed a real rule, and how many just got an empty '
            'method. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
