# Acyclic Visitor Pattern — Video Narration Script

## 1. Acyclic Visitor

Hello, and welcome. This video explains the Acyclic Visitor pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A visitor is an operation, such as working out tax, kept outside the classes it works on. In the acyclic version, each type gets its own tiny visitor interface. Each visitor handles only the types it chooses. So a new type changes nothing that already exists. Think of a hotel where staff wear a badge for each language they speak. A guest looks for the right badge. Nobody has to speak every language. And a new language only needs a new badge. In this video, the domain is an online shop. Its catalogue has books, food, and electronics, and later, gift cards. Visitors work out VAT, and customs forms. By the end, you will hear what goes wrong with the classic visitor. How the acyclic version fixes it. How a new product type changes nothing old. And what it costs.

## 2. The Scenario

Here is the scenario. The shop sells books, food, and electronics. Two operations visit every product. One works out VAT, a sales tax. The other writes customs forms, for items sent abroad. Each operation was a classic visitor. It had one method for every product type, whether it cared about that type or not. Then the shop started selling gift cards.

## 3. Act One — The classic visitor

First demo: the classic visitor. One visitor interface, with one method for every product type. Book, food, and electronics. The VAT visitor works on a book, some tea, and a kettle. Six pounds of VAT, all on the kettle. The customs visitor only cares about electronics. But it must still write two empty methods, one for books and one for food. Then the shop starts selling gift cards. The visitor interface has no method for them. Adding one means changing the interface, and every visitor.

## 4. Act Two — The acyclic visitor

Second demo: the acyclic visitor. The root visitor interface is now empty. It names no product type at all. Each product type gets its own tiny interface, with one method. A book visitor. A food visitor. An electronics visitor. A product checks whether the visitor wears its interface, like a guest looking for the right language badge. If it does, the product lets it visit. The VAT visitor wears three badges: book, food, and electronics. The VAT is still six pounds.

## 5. Act Three — A new product type

Third demo: a new product type, and nothing old changes. Gift cards arrive, with their own small interface: gift card visitor. A new visitor activates gift cards. It wears only the gift card badge. It handles gift card one. The VAT visitor does not wear that badge. So it simply skips the gift card, and the VAT stays six pounds. The VAT and customs classes were not touched at all.

## 6. Act Four — A visitor for one type

Fourth demo: a visitor for exactly the types it cares about. Customs forms are only needed for electronics. So the customs visitor wears one badge: electronics. Across four products, it handles one: the kettle. One form, twelve hundred grams. No empty methods anywhere.

## 7. Act Five — The bill

Fifth demo: the bill. Suppose a VAT visitor forgets the food badge. It still compiles. When the program runs, the tea is simply skipped. Nobody is told. The classic visitor would have caught that before the program ever ran. And there is now one extra interface, for every product type.

## 8. The Pattern

Let's name the pattern. Start with an empty root visitor interface. It names no product type at all. Give each product type its own tiny interface, with one method. Book visitor, food visitor, and so on. Each visitor implements only the interfaces for the types it handles. And each product checks for its own interface before letting a visitor in.

## 9. Who Does What

Here is who does what. Product visitor is the empty root. Book visitor, food visitor, electronics visitor, and gift card visitor are the badges. One method each. Each product checks for its badge in its accept method. And the visitors are VAT, customs, and gift card activation. Each wears only the badges it needs.

## 10. Where You Have Seen It

You have probably met this pattern already. Event listeners often implement only the listener interfaces for the events they care about. Plug-in systems let each plug-in say which file types it can handle. And the pattern itself was described by Robert C. Martin, as a way to break the dependency cycle in the classic visitor.

## 11. When To Use It

So, when should you use it? When new types keep arriving, and most operations only care about a few of them. Log or test the skipped cases, because the compiler no longer checks them. And when the list of types is fixed, prefer the classic visitor, or a sealed interface with a switch. Then the compiler checks everything for you.

## 12. Thanks for Watching

That's the Acyclic Visitor pattern. If you remember one sentence, make it this one. Give each type its own small visitor interface, and let each visitor handle only what it knows. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add clothing as a new product type, and a size label visitor that handles only clothing. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
