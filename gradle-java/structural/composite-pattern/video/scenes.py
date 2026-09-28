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
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Composite pattern, in Java. [[slnc 300]] This video is '
            'presented by Jayasekhar Konduru. [[slnc 600]] First, a '
            'simple definition. [[slnc 300]] The Composite pattern lets '
            'you treat a single item, and a whole group of items, in '
            'exactly the same way. [[slnc 300]] Both follow one shared '
            'interface. [[slnc 300]] So you can ask any part of a tree a '
            'question, without checking whether it is a single item or a '
            "group. [[slnc 600]] Think of a company's organisation chart. "
            '[[slnc 300]] Ask anyone how many people are below them, and '
            'each can answer, whether they are an intern or a manager. '
            '[[slnc 700]] In our online store, the catalog is a tree of '
            'categories and products. [[slnc 500]] By the end, you will '
            'know why a single item and a group must answer the same '
            'questions, and how to build one yourself.'
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
            "Here is the scenario. [[slnc 400]] The store's catalog is "
            'arranged as a tree. [[slnc 500]] The electronics category '
            'contains a phone. [[slnc 300]] It also contains a smaller '
            'category, called accessories. [[slnc 300]] Accessories '
            'contains a phone case and a charger. [[slnc 300]] And inside '
            'accessories is another category, called cables. [[slnc 300]] '
            'Cables contains one product: a U S B C cable. [[slnc 600]] '
            'We need two numbers. [[slnc 300]] The total price of '
            'everything in the tree. [[slnc 300]] And how many products '
            'it contains. [[slnc 300]] And the tree can be as deep as it '
            'likes.'
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
            'There are two kinds of item in this tree. [[slnc 500]] A '
            'product is a leaf. [[slnc 300]] It has no children, just a '
            'name and a price. [[slnc 500]] A category is a branch. '
            '[[slnc 300]] It holds a list of children. [[slnc 300]] Each '
            'child might be a product, or another category, one level '
            'deeper. [[slnc 600]] Here is the goal. [[slnc 300]] Whatever '
            'asks for a total price should not need to care which kind of '
            'item it has.'
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
            'Here is the naive approach. [[slnc 400]] Products and '
            'categories share no common type. [[slnc 300]] So the method '
            'that totals prices has to check which kind of item it was '
            'given, before doing anything. [[slnc 300]] If it is a '
            'product, return its price. [[slnc 300]] If it is a category, '
            'add up its children. [[slnc 600]] And here is the problem. '
            '[[slnc 300]] Counting products needs the same check. [[slnc '
            '300]] So does printing the tree. [[slnc 300]] So each method '
            'repeats the same type check, separately.'
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
            'That does real damage as the code grows. [[slnc 500]] Every '
            'new operation, like exporting the catalog, means writing the '
            'same type check again. [[slnc 500]] Add a new kind of '
            'catalog item, like a bundle, and you must revisit every '
            'method that asks the question. [[slnc 500]] And because '
            'there is no shared type, a category cannot even say what its '
            'children are. [[slnc 300]] It has to hold a list of anything '
            'at all.'
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
            'The Composite pattern fixes exactly this. [[slnc 400]] The '
            'classic book on design patterns, by the authors known as the '
            'Gang of Four, describes it like this. [[slnc 300]] Arrange '
            'objects into tree structures, to represent parts and wholes. '
            '[[slnc 300]] And let clients treat single objects, and '
            'groups of objects, the same way. [[slnc 600]] In plain '
            'words: a leaf and a branch answer the same questions. [[slnc '
            '300]] So whoever asks never has to check which one they '
            'have.'
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
            'Here is how to remember it. [[slnc 300]] Think about an '
            'organisation chart. [[slnc 500]] Ask anyone: how many people '
            'do you manage, including everyone below you? [[slnc 500]] An '
            'intern answers straight away: zero. [[slnc 300]] A manager '
            'asks each of their team the same question, and adds up the '
            'answers. [[slnc 600]] Same question, both times. [[slnc '
            '300]] Only the work behind the answer is different.'
        ),
    ),
    dict(
        key="08-roles",
        kind="diagram",
        title="The Three Roles",
        body=None,
        narration=(
            'Every composite has three roles. [[slnc 500]] The component: '
            'the shared interface that both other roles follow. [[slnc '
            '300]] Here, it is called catalog component. [[slnc 400]] The '
            'leaf: a product. [[slnc 300]] It has no children, and '
            'answers about itself alone. [[slnc 400]] And the composite: '
            'a category. [[slnc 300]] It holds children, and answers by '
            'asking each of them, then combining the results. [[slnc '
            '600]] Here is the most important idea in this video. [[slnc '
            "300]] A category's children are all just catalog components. "
            '[[slnc 300]] Not specifically products, or categories. '
            '[[slnc 300]] So a category can hold other categories, nested '
            'as deep as you like.'
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
            'Here is the component, the catalog component interface. '
            '[[slnc 400]] It lists every question the tree can answer. '
            '[[slnc 300]] Its name. [[slnc 200]] Its total price. [[slnc '
            '200]] How many products it contains. [[slnc 200]] And how to '
            'print itself. [[slnc 600]] A product follows this interface '
            'directly, as a leaf. [[slnc 300]] A category follows the '
            'same interface. [[slnc 300]] But it also holds a list of '
            'catalog components, as its children.'
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
            'Here is the leaf: a product. [[slnc 400]] Asked for its '
            'total price, it simply returns its own price. [[slnc 300]] '
            'No loop, and no children to ask. [[slnc 300]] This is where '
            'the recursion stops. [[slnc 600]] Asked how many products it '
            'contains, it always says one. [[slnc 300]] However deep in '
            'the tree it sits. [[slnc 300]] It does not know, and does '
            'not need to.'
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
            "Here is the heart of the pattern: a category's total price. "
            '[[slnc 400]] It goes through its children, and asks each one '
            'for its total price. [[slnc 300]] It never checks whether a '
            'child is a product, or another category. [[slnc 300]] It '
            'does not need to, because both answer the same question. '
            '[[slnc 600]] If a child is another category, that child does '
            'exactly the same thing, one level further down. [[slnc 300]] '
            'The recursion is happening. [[slnc 300]] It is just hidden '
            'inside one simple call.'
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
            'Here is the code that ties it together. [[slnc 400]] It '
            'builds the tree with a few add calls. [[slnc 300]] Then it '
            'asks the top of the tree, once, for the total price. [[slnc '
            '300]] And once for the product count. [[slnc 600]] Then it '
            'goes through the direct children of electronics, and asks '
            'each for its total price. [[slnc 300]] Some are products. '
            '[[slnc 300]] Some are categories. [[slnc 300]] And the code '
            'never asks which. [[slnc 300]] That is the whole payoff.'
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
            "Let's run the project. [[slnc 400]] The tree is printed, "
            'level by level. [[slnc 500]] The total price is six hundred '
            'and fifty-nine dollars ninety-six. [[slnc 300]] Across four '
            'products. [[slnc 300]] Worked out by one call at the top, '
            'which quietly reached through three levels of nesting. '
            '[[slnc 600]] Then, accessories, a category, answers the '
            'price question in exactly the same way as the phone, a '
            'product. [[slnc 300]] Same question, same code. [[slnc 300]] '
            'Completely different work underneath.'
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
            'So, to recap. [[slnc 400]] Use a composite when your data is '
            'shaped like a tree. [[slnc 300]] And you want code to treat '
            'single items and groups the same way. [[slnc 600]] Keep '
            'methods for adding children off the shared interface. [[slnc '
            '300]] A product has no sensible way to accept children. '
            '[[slnc 300]] That is a deliberate choice. [[slnc 500]] And '
            'watch out for loops. [[slnc 300]] A tree that loops back on '
            'itself will recurse forever, and crash. [[slnc 600]] And one '
            'comparison worth knowing. [[slnc 300]] The Decorator pattern '
            'wraps one thing in one extra layer. [[slnc 300]] A composite '
            'lets one thing contain many things, arranged in a tree.'
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
            "That's the Composite pattern. [[slnc 400]] If you remember "
            'one sentence, make it this one. [[slnc 300]] Make single '
            'items and groups answer the same questions, so nothing that '
            'asks ever needs to check which it has. [[slnc 500]] The full '
            'source code, written notes, diagrams, and an animated '
            'walkthrough are all in the repository. [[slnc 300]] It runs '
            'offline, with nothing installed except a Java development '
            'kit. [[slnc 500]] Here is one exercise to try. [[slnc 300]] '
            'Add a new question to the tree, like the most expensive '
            'product. [[slnc 300]] And notice that the code asking the '
            'question stays simple. [[slnc 500]] If this helped, a like '
            'really does help other people find it. [[slnc 300]] And '
            "subscribe, if you'd like the rest of the series. [[slnc "
            '400]] Thanks for watching.'
        ),
    ),
]
