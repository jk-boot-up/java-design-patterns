# Message Translator with Apache Camel Pattern — Video Narration Script

## 1. Message Translator with Apache Camel

Hello, and welcome. This video explains the Message Translator pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A message translator turns a message from one format into another. So a receiver only ever sees the one format it understands. Apache Camel is an open-source library for moving messages, and it has translators built in. Think of an international post room. A desk sees which language each letter is in, and passes it to that language's translator. Every translator writes the same standard form, for the office upstairs. In this video, the domain is an online shop's warehouse, taking orders from its web form and from marketplaces. By the end, you will hear how Camel refuses a foreign format. How each format becomes a route. How a normalizer picks the right one. And what the framework costs.

## 2. The Scenario

Here is the scenario. The shop's web form sends key and value text. Marketplace A sends CSV. Marketplace B sends JSON. And later, marketplace C sends XML. The warehouse must only ever see one standard order.

## 3. Act One — Straight to the warehouse

First demo: send a marketplace's order straight to the warehouse. In Camel, a route is a written description of where messages go. The warehouse route starts by converting each message into the shop's standard order. A raw JSON order cannot be converted. So Camel refuses it, before the warehouse ever sees it.

## 4. Act Two — A translator route per format

Second demo: one translator route per format. Camel has ready-made readers, called data formats. The CSV route uses Camel's CSV reader. Two mugs, for order A seventy-seven. The JSON route uses Camel's JSON reader. One teapot, for order B nine. The web form route splits the text itself. One kettle, for order W one.

## 5. Act Three — The normalizer

Third demo: the normalizer. Every order now arrives at one inbox. The normalizer looks at the text, and decides the format. Curly bracket means JSON. Angle bracket means XML. An equals sign means the web form. Anything else is CSV. It then sends the order to the translator route with that name. All three orders come out as standard picks. Five routes are running.

## 6. Act Four — A new format, a new route

Fourth demo: a new marketplace sends XML. The normalizer recognises it, and sends it on. But no translator route exists yet. Camel says so. No consumers available. One new route is added, while the others keep running. It reads the XML. Now the order is picked. One kettle, for order C five. The normalizer and the warehouse did not change.

## 7. Act Five — The bill

Fifth demo: the bill. The gift note from marketplace B is still lost. The standard order has no room for it. And the program now carries more than twenty library files. The plain version needs none. Plus a new route language, to learn.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. Each translator is a route. A data format reads the text into Java objects. And a normalizer route sends each message to the translator whose name matches its format.

## 9. Who Does What

Here is who does what. Shop routes holds every route, the normalizer, the translators, and the warehouse. The translators class maps each format's fields to the standard names. Order message is the standard order. And the warehouse receives nothing else.

## 10. Where You Have Seen It

You have probably met this already. Camel routes run inside many Spring Boot and Quarkus services. Spring Integration calls translators, transformers. And MuleSoft's DataWeave is the same idea, in another tool.

## 11. When To Use It

So, when should you use Camel for this? When there are many formats and transports, and translators arrive over time. For a few formats that rarely change, the plain Java version is simpler, and easier to debug.

## 12. Thanks for Watching

That's the Message Translator, with Apache Camel. If you remember one sentence, make it this one. Each format gets its own route, and the receiver only ever sees one shape. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Send orders in an unknown format to a dead-letter route. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
