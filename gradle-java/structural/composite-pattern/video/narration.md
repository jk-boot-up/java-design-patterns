# Video Narration Script

Narration for the Composite pattern teaching video. Each scene below maps to
one slide. The narration is spoken by macOS `Samantha`, a female US English
voice, at 145 words per minute.

Total scenes: 15. Approximate runtime: about 7 minutes.

The first and last scenes carry the channel branding: scene 1 credits
the author out loud over the poster, and the final scene asks for the
thumbs up and the subscribe.

The script is written to be spoken rather than read, and carries `[[slnc NNN]]`
pause markers in [`scenes.py`](scenes.py) that insert NNN milliseconds of
silence. Those are instructions to the synthesiser, not words: they are
stripped from the text below and from the subtitles.

---

## Scene 1 — The Composite Pattern

Hello, and welcome. This video explains the Composite pattern in Java, and it is written and presented by Jayasekhar Konduru. Let's start with the simple definition. The composite pattern lets you treat a single object and a whole group of objects in exactly the same way. Both implement one interface, so a caller can put a question to any node in a tree without knowing, or asking, whether it is a leaf or a branch. That's the idea in a sentence, and it applies to anything shaped like a tree. The rest of the video does it properly, by building a real working Java project: an e-commerce catalog made of categories and products. By the end you'll know why a leaf and a branch of the same tree need to answer to the exact same interface, and how to write one yourself.

## Scene 2 — The Scenario

So, imagine an online store's catalog, organised as a tree. Electronics contains a Phone, and a nested category called Accessories. Accessories contains a Case and a Charger, plus another nested category, Cables. And Cables contains one more product, a USB-C cable. Now we need two numbers. The total price of everything in the tree, and how many products it contains. And critically, the tree can be as deep as it wants.

## Scene 3 — Two Very Different Kinds of Node

Look at the two kinds of node in this tree. A Product is a leaf. It has no children, just a name and a price. A Category is a branch. It holds a list of children, and each of those children might be a Product, or it might be another Category, nested one level deeper. And here's the goal. Whatever is asking for the total price of a node shouldn't have to care which of the two kinds it actually has.

## Scene 4 — The Naive Approach — instanceof, Repeated Per Operation

So here's the naive approach. totalPrice takes a plain Object, because NaiveProduct and NaiveCategory share no common type. So it has to ask, with instanceof, which one it actually got, before it can do anything. And here's the problem. productCount and print need the exact same question answered, so they each repeat this exact same instanceof chain, completely independently, one method at a time.

## Scene 5 — Why That Hurts

And that does real damage as the code grows. Every new operation — export to J-son, say — means writing that same instanceof chain a fourth time. Add a new catalog item type, a Bundle, say, and now you have to go back and touch every single method that ever asked this question. And notice NaiveCategory can't even declare a properly typed list of its children — with no shared supertype, it has to fall back to a raw List of Object.

## Scene 6 — The Composite Pattern

The composite pattern fixes exactly this. In Gang of Four terms, composite composes objects into tree structures to represent part-whole hierarchies, and it lets clients treat individual objects and compositions of objects uniformly. In plain language? A leaf and a branch answer to the same questions, so whoever is asking never has to check which one they've got.

## Scene 7 — Remember It With an Org Chart

Here's how to remember it forever. Think about an org chart. Ask any employee, how many people do you manage, including everyone below you? An intern answers directly. Zero. A manager asks each of their direct reports the exact same question, and adds up the answers. Same question, same interface, both times. Only the computation behind the answer is different.

## Scene 8 — The Three Roles

Every composite setup has three roles. The component, CatalogComponent, the shared interface both other roles implement. The leaf, Product, which has no children and answers about itself alone. And the composite, Category, which holds children and answers by asking each of them, then combining the results. Here's the single most important idea in this whole video. Category's children are typed as CatalogComponent, not as Product or Category specifically — so a Category can hold more categories, nested as deep as you like, without a single line of code caring.

## Scene 9 — The Component — One Interface, Both Roles Implement It

This is the component, CatalogComponent. It declares every question the tree can answer: its name, its total price, how many products it contains, and how to print itself. Product implements this directly, as a leaf. Category implements the exact same interface, but it also holds a list of these — CatalogComponent children, not Product children, not Category children. Just CatalogComponent.

## Scene 10 — The Leaf — Product Answers About Itself Alone

And this is the leaf, Product. totalPrice just returns its own price. No loop, no children to ask. This is the base case of the recursion. productCount always returns exactly one, no matter how deep in the tree this particular Product happens to sit. It doesn't know, and it doesn't need to.

## Scene 11 — The Composite — Category Delegates and Combines

This is the heart of the pattern, Category dot totalPrice. It loops over its children and calls totalPrice on each one. It never checks whether a child is a Product or another Category. It doesn't need to — both answer to exactly the same method. If that child happens to be another Category, calling totalPrice on it triggers this exact same loop, one level further down. The recursion is happening. It's just hidden inside one polymorphic call.

## Scene 12 — The Client — No instanceof Anywhere

And here's the client, CatalogDemo, that ties it together. It builds the tree with a few chained add calls, then makes exactly one call each for the total price and the product count, at the root. Look at the last loop. It walks electronics' direct children and asks each one for its total price. Some of those children are products, some are nested categories — and this loop never asks which. That's the whole payoff.

## Scene 13 — Running It

When we run the project, the printed tree and the totals are right there in the output. Six hundred fifty nine dollars and ninety six cents, across four products, computed by one call at the root that quietly recursed through three levels of nesting. And look at the last two lines. Accessories, a Category, answers totalPrice and productCount in exactly the same shape as Phone, a Product, does one line above. Same call, same client code, completely different computation underneath.

## Scene 14 — Wrap Up

So, to recap. Use composite when your data is naturally tree-shaped, and you want client code to treat leaves and branches the same way. Keep child-management methods like add off the shared interface — a leaf has no good way to implement them, and that's a deliberate trade-off, not an oversight. And watch for cycles: a tree that loops turns recursion into a stack overflow. And if you remember one sentence from today, make it this one. Decorator wraps one thing in one more layer. Composite lets one thing be many things, arranged in a tree.

## Scene 15 — Thanks for Watching

And that's the composite pattern. If you got something out of this, do give it a thumbs up, and subscribe. It genuinely helps the channel, and it's what makes more of these possible. And if there's a pattern you'd like me to cover next, drop it in the comments. I read every one. All the source code, the written notes and an interactive animation are in the repository. Thanks for watching, and I'll see you in the next one.
