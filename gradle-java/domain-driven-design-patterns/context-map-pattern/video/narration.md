# Context Map and Shared Kernel Pattern — Video Narration Script

## 1. Context Map and Shared Kernel

Hello, and welcome. This video explains the Context Map and Shared Kernel patterns, from domain-driven design, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A big system is split into parts, each with its own model and team. A context map writes down how those parts relate. A shared kernel is a tiny piece of model that two parts share, and change only together. Think of two neighbouring houses with a shared garden wall. Each family runs its own house. But neither can move the wall without asking the other. And a street map shows who shares what with whom. In this video, the domain is an online shop. Sales takes orders. Shipping prints labels. And the catalogue supplies prices. By the end, you will hear how two copies of an address lost a flat number. How a shared kernel fixes it. How to keep a map that is checked. And what sharing costs.

## 2. The Scenario

Here is the scenario. The shop has three parts, called contexts. Sales takes orders. Shipping prints labels. The catalogue supplies prices. Sales and shipping both need addresses. Each kept its own address class. And a converter copied one into the other.

## 3. Act One — Two copies of an address

First demo: sales and shipping each keep their own address. Sales added a flat number to its address. Shipping's address never had one. A converter copies one into the other. Priya types: flat two, four Mill Lane, Leeds. The shipping label says: four Mill Lane, Leeds. The flat number was lost between the two parts of the shop. The parcel waits at the main door.

## 4. Act Two — A shared kernel

Second demo: a shared kernel. A small shared package holds two classes: address, and money. Both teams own it together. Sales places order one, for thirty-eight pounds. Shipping prints the label from the very same address. Flat two, four Mill Lane, Leeds. Insured for thirty-eight pounds. There is no converter to lose anything.

## 5. Act Three — The context map

Third demo: the context map. It writes down who depends on whom, and how. The catalogue supplies sales: sales asks it for prices. Sales and shipping share the kernel: address and money. And shipping does not know that sales exists. It only knows the kernel.

## 6. Act Four — The map, checked

Fourth demo: the map is checked against the code. A small check reads every source file, and looks at what it imports. Imports the map does not allow: zero. Then someone takes a shortcut. In shipping, they import the sales order. The check reports it: shipping imports sales, which the map does not allow.

## 7. Act Five — The bill

Fifth demo: the bill. A shared kernel changes slowly. Adding a postcode to the address needs both teams to agree, test, and release together. So keep the kernel tiny. Here, two classes. Everything else stays inside its own context.

## 8. The Pattern

Let's name the patterns. A context map lists the parts of the system, and how each pair relates. Who supplies whom. Who shares what. A shared kernel is one of those relationships. A tiny model that two parts own together, and change only by agreement. And the map is kept as code, and checked against the imports on every build.

## 9. Who Does What

Here is who does what. The kernel package holds address and money, shared by sales and shipping. Sales, shipping, and catalogue are the contexts, each a package with its own code. The context map class lists the relationships, and checks that the imports agree. And the before package is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met these patterns already. A small shared common library, used by two services, is a shared kernel. Architecture documents often draw context maps, with arrows marked upstream and downstream. And architecture tests that say which packages may import which keep the map honest.

## 11. When To Use It

So, when should you use them? As soon as a system has more than one team, or more than one model, draw a context map. Keep it as code, and check it. Share a kernel only for the few concepts that must match exactly. Keep it tiny, and change it together.

## 12. Thanks for Watching

That's the Context Map and Shared Kernel patterns. If you remember one sentence, make it this one. Draw the borders, check them, and share only a little. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a postcode to the kernel's address, and count which contexts must change. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
