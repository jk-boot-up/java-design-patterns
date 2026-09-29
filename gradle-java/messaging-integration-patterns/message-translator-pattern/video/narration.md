# Message Translator / Normalizer Pattern — Video Narration Script

## 1. Message Translator / Normalizer

Hello, and welcome. This video explains the Message Translator and Normalizer patterns, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A message translator turns a message in one format into the format your system uses. A normalizer recognises which format each message is in, and picks the right translator. So everything inside your system arrives in one standard shape. Think of interpreters at an international meeting. Each delegate speaks their own language. An interpreter for each language turns it into the one working language. When a new country joins, you hire one more interpreter. In this video, the domain is an online shop. It takes orders from its own web form, and from marketplaces that each send orders in their own format. By the end, you will hear what happens when the warehouse reads every format. How translators and a normalizer fix it. How to add a marketplace. And what gets lost in translation.

## 2. The Scenario

Here is the scenario. Orders come from the shop's web form, as key-value text. From marketplace A, as comma-separated values. And from marketplace B, as JSON, with its own names for every field. The warehouse read all three itself.

## 3. Act One — The warehouse reads every format

First demo: the warehouse reads every marketplace's format itself. The web form sends key-value text. Marketplace A sends comma-separated values. Marketplace B sends JSON, with its own names for things. The warehouse understands all three, and picks a kettle, two mugs, and a teapot. Then a new marketplace sends XML. The warehouse cannot read the order. Every new format means changing the warehouse.

## 4. Act Two — Translators

Second demo: a translator for each format. Each translator does one job: turn its format into the shop's one standard order. An order ID, a product, a quantity, and a price. The web form becomes: W 1, one kettle, thirty pounds. The CSV: A 77, two mugs, sixteen pounds. The JSON: B 9, one teapot, twenty-five pounds. Three formats in. One shape out.

## 5. Act Three — The normalizer

Third demo: a normalizer recognises the format, and picks the translator. It holds simple rules. Starts with order equals? The web form. Starts with A and has commas? Marketplace A. Starts with a curly brace? Marketplace B. Each order is translated by the right translator. The warehouse only ever sees the one standard order.

## 6. Act Four — A new marketplace

Fourth demo: a new marketplace. Marketplace C sends XML. It gets one new translator, and one new rule. Its order, C 5, one kettle, reaches the warehouse like every other order. The warehouse was not changed at all.

## 7. Act Five — The bill

Fifth demo: the bill. Marketplace B's order carries a gift note: Happy birthday, Mum. The standard order has no field for gift notes. After translation, the note is gone. Every field someone needs must be added to the standard order, and to every translator.

## 8. The Pattern

Let's name the patterns. Write one small translator for each format. Each turns its format into one canonical message: the shop's standard order. Put a normalizer at the edge. It recognises which format each message is in, and hands it to the right translator. Inside the shop, there is only one kind of order.

## 9. Who Does What

Here is who does what. Order message is the canonical order: ID, product, quantity, and price in pence. The translators turn each format into it. The normalizer recognises the format, and picks the translator. And the warehouse only ever sees order messages.

## 10. Where You Have Seen It

You have probably met these patterns already. Apache Camel and Spring Integration have transformers and data formats for exactly this. Large companies define a canonical data model, one standard shape for each kind of message. And any shop that integrates with several payment or shipping providers has one mapper for each.

## 11. When To Use It

So, when should you use them? Whenever several senders use different formats. Keep one small translator for each format. Design the canonical message carefully. And check what each translation drops. With one sender whose format you control, simply agree on the format.

## 12. Thanks for Watching

That's the Message Translator and Normalizer patterns. If you remember one sentence, make it this one. Translate at the edge, so the inside speaks one language. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a note field to the standard order, and carry the gift note through. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
