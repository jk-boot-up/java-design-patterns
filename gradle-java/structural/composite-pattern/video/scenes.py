"""Scene definitions for the Composite pattern teaching video.

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
        title="The Composite Pattern",
        body=None,
        narration=(
            "Hello, and welcome. This video explains the Composite pattern in "
            "Java, and it is written and presented by Jayasekhar Konduru. [[slnc "
            "300]] Let's start with the simple definition. The composite pattern "
            "lets you treat a single object and a whole group of objects in "
            "exactly the same way. Both implement one interface, so a caller can "
            "put a question to any node in a tree without knowing, or asking, "
            "whether it is a leaf or a branch. [[slnc 350]] That's the idea in a "
            "sentence, and it applies to anything shaped like a tree. The rest of "
            "the video does it properly, by building a real working Java project: "
            "an e-commerce catalog made of categories and products. [[slnc 250]] "
            "By the end you'll know why a leaf and a branch of the same tree need "
            "to answer to the exact same interface, and how to write one "
            "yourself."
        ),
    ),
    dict(
        key="02-scenario",
        kind="bullets",
        title="The Scenario",
        body=[
            "An online store organizes its catalog as a tree:",
            "",
            "  Electronics",
            "    Phone",
            "    Accessories",
            "      Case, Charger",
            "      Cables",
            "        USB-C Cable",
            "",
            "We need a total price and a product count — at any depth.",
        ],
        narration=(
            "So, imagine an online store's catalog, organised as a tree. "
            "[[slnc 250]] Electronics contains a Phone, and a nested category "
            "called Accessories. Accessories contains a Case and a Charger, "
            "plus another nested category, Cables. And Cables contains one "
            "more product, a USB-C cable. [[slnc 300]] Now we need two "
            "numbers. The total price of everything in the tree, and how many "
            "products it contains. And critically, the tree can be as deep as "
            "it wants."
        ),
    ),
    dict(
        key="03-anatomy",
        kind="bullets",
        title="Two Very Different Kinds of Node",
        body=[
            "Product         — a leaf. No children. Just a name and a price.",
            "Category        — a branch. Holds a list of children,",
            "                  each of which might be a Product",
            "                  or another Category.",
            "",
            "A client asking for the total shouldn't care which one it has.",
        ],
        narration=(
            "Look at the two kinds of node in this tree. A Product is a leaf. "
            "It has no children, just a name and a price. [[slnc 250]] A "
            "Category is a branch. It holds a list of children, and each of "
            "those children might be a Product, or it might be another "
            "Category, nested one level deeper. [[slnc 300]] And here's the "
            "goal. Whatever is asking for the total price of a node shouldn't "
            "have to care which of the two kinds it actually has."
        ),
    ),
    dict(
        key="04-problem",
        kind="code",
        title="The Naive Approach — instanceof, Repeated Per Operation",
        body="""public static BigDecimal totalPrice(Object item) {
    if (item instanceof NaiveProduct p) {
        return p.getPrice();
    } else if (item instanceof NaiveCategory c) {
        BigDecimal sum = BigDecimal.ZERO;
        for (Object child : c.children()) {
            sum = sum.add(totalPrice(child));   // recurse, still checking types
        }
        return sum;
    }
    throw new IllegalArgumentException("Unknown catalog item: " + item);
}

//  productCount(Object) and print(Object, String) repeat this exact
//  same instanceof chain, independently, one method at a time.""",
        narration=(
            "So here's the naive approach. [[slnc 250]] totalPrice takes a "
            "plain Object, because NaiveProduct and NaiveCategory share no "
            "common type. So it has to ask, with instanceof, which one it "
            "actually got, before it can do anything. [[slnc 300]] And here's "
            "the problem. productCount and print need the exact same "
            "question answered, so they each repeat this exact same "
            "instanceof chain, completely independently, one method at a "
            "time."
        ),
    ),
    dict(
        key="05-why-hurts",
        kind="bullets",
        title="Why That Hurts",
        body=[
            "✗   Every operation repeats the same instanceof chain",
            "✗   Add a fourth operation? Write the chain a fourth time",
            "✗   Add a new catalog item type? Touch every method that exists",
            "✗   NaiveCategory can't even declare List<NaiveProduct> —",
            "     it has to fall back to List<Object>",
        ],
        narration=(
            "And that does real damage as the code grows. [[slnc 250]] Every "
            "new operation — export to J-son, say — means writing that same "
            "instanceof chain a fourth time. [[slnc 300]] Add a new catalog "
            "item type, a Bundle, say, and now you have to go back and touch "
            "every single method that ever asked this question. [[slnc 250]] "
            "And notice NaiveCategory can't even declare a properly typed "
            "list of its children — with no shared supertype, it has to fall "
            "back to a raw List of Object."
        ),
    ),
    dict(
        key="06-pattern",
        kind="quote",
        title="The Composite Pattern",
        body=[
            "“Composes objects into tree structures to represent",
            "part-whole hierarchies. Composite lets clients treat",
            "individual objects and compositions of objects",
            "uniformly.”",
            "",
            "—  Gang of Four, Design Patterns",
            "",
            "In plain language:",
            "a leaf and a branch answer to the same questions.",
        ],
        narration=(
            "The composite pattern fixes exactly this. [[slnc 250]] In Gang "
            "of Four terms, composite composes objects into tree structures "
            "to represent part-whole hierarchies, and it lets clients treat "
            "individual objects and compositions of objects uniformly. "
            "[[slnc 300]] In plain language? A leaf and a branch answer to "
            "the same questions, so whoever is asking never has to check "
            "which one they've got."
        ),
    ),
    dict(
        key="07-orgchart",
        kind="bullets",
        title="Remember It With an Org Chart",
        body=[
            "Ask any employee: \"how many people do you manage,",
            "including everyone below you?\"",
            "",
            "An intern answers directly: zero.",
            "A manager asks each of their reports the same question,",
            "and adds up the answers.",
            "",
            "Same question. Same interface. Different computation.",
        ],
        narration=(
            "Here's how to remember it forever. Think about an org chart. "
            "[[slnc 250]] Ask any employee, how many people do you manage, "
            "including everyone below you? [[slnc 300]] An intern answers "
            "directly. Zero. A manager asks each of their direct reports the "
            "exact same question, and adds up the answers. [[slnc 250]] Same "
            "question, same interface, both times. Only the computation "
            "behind the answer is different."
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            "Every composite setup has three roles. [[slnc 200]] The "
            "component, CatalogComponent, the shared interface both other "
            "roles implement. The leaf, Product, which has no children and "
            "answers about itself alone. And the composite, Category, which "
            "holds children and answers by asking each of them, then "
            "combining the results. [[slnc 350]] Here's the single most "
            "important idea in this whole video. Category's children are "
            "typed as CatalogComponent, not as Product or Category "
            "specifically — so a Category can hold more categories, nested "
            "as deep as you like, without a single line of code caring."
        ),
    ),
    dict(
        key="09-component",
        kind="code",
        title="The Component — One Interface, Both Roles Implement It",
        body="""public interface CatalogComponent {

    String name();

    BigDecimal totalPrice();

    int productCount();

    void print(String indent);
}

//  Product implements this directly.
//  Category implements this too — and also holds a List<CatalogComponent>.""",
        narration=(
            "This is the component, CatalogComponent. [[slnc 250]] It "
            "declares every question the tree can answer: its name, its "
            "total price, how many products it contains, and how to print "
            "itself. [[slnc 300]] Product implements this directly, as a "
            "leaf. Category implements the exact same interface, but it also "
            "holds a list of these — CatalogComponent children, not Product "
            "children, not Category children. Just CatalogComponent."
        ),
    ),
    dict(
        key="10-leaf",
        kind="code",
        title="The Leaf — Product Answers About Itself Alone",
        body="""public final class Product implements CatalogComponent {

    private final String name;
    private final BigDecimal price;

    @Override
    public BigDecimal totalPrice() {
        return price;                 // the base case of the recursion
    }

    @Override
    public int productCount() {
        return 1;                     // always exactly one, wherever it sits
    }
}""",
        narration=(
            "And this is the leaf, Product. [[slnc 250]] totalPrice just "
            "returns its own price. No loop, no children to ask. This is the "
            "base case of the recursion. [[slnc 300]] productCount always "
            "returns exactly one, no matter how deep in the tree this "
            "particular Product happens to sit. It doesn't know, and it "
            "doesn't need to."
        ),
    ),
    dict(
        key="11-composite",
        kind="code",
        title="The Composite — Category Delegates and Combines",
        body="""public final class Category implements CatalogComponent {

    private final List<CatalogComponent> children = new ArrayList<>();

    @Override
    public BigDecimal totalPrice() {
        BigDecimal sum = BigDecimal.ZERO;
        for (CatalogComponent child : children) {
            sum = sum.add(child.totalPrice());   // no instanceof — just ask
        }
        return sum;
    }

    public Category add(CatalogComponent child) {
        children.add(child);
        return this;
    }
}""",
        narration=(
            "This is the heart of the pattern, Category dot totalPrice. "
            "[[slnc 250]] It loops over its children and calls totalPrice on "
            "each one. It never checks whether a child is a Product or "
            "another Category. It doesn't need to — both answer to exactly "
            "the same method. [[slnc 300]] If that child happens to be "
            "another Category, calling totalPrice on it triggers this exact "
            "same loop, one level further down. The recursion is happening. "
            "It's just hidden inside one polymorphic call."
        ),
    ),
    dict(
        key="12-client",
        kind="code",
        title="The Client — No instanceof Anywhere",
        body="""Category electronics = new Category("Electronics")
        .add(new Product("Phone", new BigDecimal("599.99")))
        .add(accessories);

electronics.print("");
System.out.println("Total price:  $" + electronics.totalPrice());
System.out.println("Product count: " + electronics.productCount());

for (CatalogComponent child : electronics.children()) {
    System.out.println(child.name() + " -> $" + child.totalPrice());
}
//  child could be a Product or a Category — this loop never asks which.""",
        narration=(
            "And here's the client, CatalogDemo, that ties it together. "
            "[[slnc 250]] It builds the tree with a few chained add calls, "
            "then makes exactly one call each for the total price and the "
            "product count, at the root. [[slnc 300]] Look at the last loop. "
            "It walks electronics' direct children and asks each one for its "
            "total price. Some of those children are products, some are "
            "nested categories — and this loop never asks which. That's the "
            "whole payoff."
        ),
    ),
    dict(
        key="13-output",
        kind="console",
        title="Running It",
        body="""$ ./gradlew run

== Printing the whole catalog tree ==
+ Electronics/
  - Phone ($599.99)
  + Accessories/
    - Case ($19.99)
    - Charger ($29.99)
    + Cables/
      - USB-C Cable ($9.99)

== Totals, computed uniformly over leaves and composites ==
Total price:  $659.96
Product count: 4

== Uniform treatment: no instanceof anywhere above ==
Phone -> $599.99 across 1 product(s)
Accessories -> $59.97 across 3 product(s)""",
        narration=(
            "When we run the project, the printed tree and the totals are "
            "right there in the output. [[slnc 250]] Six hundred fifty nine "
            "dollars and ninety six cents, across four products, computed by "
            "one call at the root that quietly recursed through three levels "
            "of nesting. [[slnc 300]] And look at the last two lines. "
            "Accessories, a Category, answers totalPrice and productCount in "
            "exactly the same shape as Phone, a Product, does one line "
            "above. Same call, same client code, completely different "
            "computation underneath."
        ),
    ),
    dict(
        key="14-wrapup",
        kind="bullets",
        title="Wrap Up",
        body=[
            "Use composite when data is naturally tree-shaped",
            "and you want to treat leaves and branches alike.",
            "",
            "Keep child-management methods (add) off the shared interface —",
            "a leaf has no good way to implement them.",
            "Watch for cycles: a tree that loops recurses forever.",
            "",
            "Remember one sentence:",
            "Decorator wraps one thing in one more layer.",
            "Composite lets one thing be many things, arranged in a tree.",
        ],
        narration=(
            "So, to recap. Use composite when your data is naturally "
            "tree-shaped, and you want client code to treat leaves and "
            "branches the same way. [[slnc 300]] Keep child-management "
            "methods like add off the shared interface — a leaf has no good "
            "way to implement them, and that's a deliberate trade-off, not an "
            "oversight. And watch for cycles: a tree that loops turns "
            "recursion into a stack overflow. [[slnc 350]] And if you "
            "remember one sentence from today, make it this one. Decorator "
            "wraps one thing in one more layer. Composite lets one thing be "
            "many things, arranged in a tree."
        ),
    ),
    dict(
        key="15-outro",
        kind="outro",
        title="Thanks for Watching",
        body=[
            "If this helped, a thumbs up and a subscribe go a long way",
            "towards keeping more videos like it coming.",
            "",
            "Full source code, notes and an animation are in the repository.",
        ],
        narration=(
            "And that's the composite pattern. [[slnc 300]] If you got "
            "something out of this, do give it a thumbs up, and subscribe. It "
            "genuinely helps the channel, and it's what makes more of these "
            "possible. [[slnc 250]] And if there's a pattern you'd like me to "
            "cover next, drop it in the comments. I read every one. [[slnc "
            "250]] All the source code, the written notes and an interactive "
            "animation are in the repository. Thanks for watching, and I'll "
            "see you in the next one."
        ),
    ),
]
