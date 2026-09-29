# Modular Monolith Pattern — Video Narration Script

## 1. Modular Monolith

Hello, and welcome. This video explains the Modular Monolith pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A monolith is a program that is built and deployed as one piece. A modular monolith is still one piece. But inside, it is split into modules. Each module owns its own data, and the others may only use its front door. Think of a department store. One building, one entrance. But the shoe department has its own staff and its own stockroom. Other departments do not walk in and take boxes. They ask at the counter. In this video, the domain is an online shop. It is one Java program, with a catalogue that holds the stock, orders, and payments. By the end, you will hear how open tables let a shop sell one kettle twice. How modules with front doors stop it. How to check the walls automatically. And how a module can later become its own service.

## 2. The Scenario

Here is the scenario. The shop is one Java program. Inside it: checkout, the catalogue, and payments. Every table is open to every class. A table here is just a map of data, such as how many kettles are in stock. The catalogue has a rule. Stock never goes below zero. But does everyone follow it?

## 3. Act One — Every table open

First demo: one program, with every table open to everyone. There is one kettle in stock. The catalogue has a rule. Stock never goes below zero. But checkout does not ask the catalogue. It writes to the stock table itself. Two customers order the kettle. Checkout takes one from stock, twice. Stock is now minus one. Two customers have paid, for one kettle.

## 4. Act Two — Modules with front doors

Second demo: modules, each with a front door. The shop is now three modules. Catalogue, orders, and payments. Each module owns its own data. And each offers a small front door, called an API: a short list of things other modules may ask for. Orders cannot touch the stock table. It must ask the catalogue to reserve a kettle. Order one: placed, and paid. Order two: refused, only zero kettles left. And it is never charged. Stock stays at zero. The rule holds, because only the catalogue can change stock.

## 5. Act Three — Boundaries checked

Third demo: the boundaries are checked, not hoped for. Java cannot stop one module using another module's insides. So a small check reads every source file, and looks at what it imports. This project's source: zero modules reaching inside another. Now someone takes a shortcut. Inside orders, they import the payments module's internal class. The check reports it: orders module imports payments internal. And the build fails, before the shortcut can be merged.

## 6. Act Four — Moving a module out

Fourth demo: moving payments out, into its own service. Payments has grown, and its team wants to deploy it separately. Orders has only ever used the payments front door. So a new class, remote payments, offers the same front door, but answers over the network. Plug it in. Order three is placed, with one network call to payments. Lines changed in the orders module: zero.

## 7. Act Five — The bill

Fifth demo: the bill. It is still one program. Three modules, one build, one deployment. A fix to payments redeploys the catalogue too. One process. A crash in any module stops them all. And they can only be scaled together. And the walls last only as long as the check runs, on every build.

## 8. The Pattern

Let's name the pattern. Split the program by business area. Catalogue, orders, payments. Each module owns its own data, and its own rules. Each offers a small front door. Other modules may use that front door, and nothing else. Check those walls automatically, on every build. It is still one program. But inside, it has walls.

## 9. Who Does What

Here is who does what. Catalog A P I, orders A P I, and payments A P I are the front doors. Each is a short Java interface. Each module keeps its real classes in a package called internal. Nobody outside may use them. The boundary check reads the source, and fails the build if anyone does. And remote payments is the payments front door, answered over the network, for the day payments moves out.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's own module system lets each module say which packages it exports. Arch Unit is a test library that fails the build when one package uses another it should not. Spring Modulith does the same for Spring Boot. And some of the largest web applications, such as Shopify and GitHub, are monoliths split into modules like this.

## 11. When To Use It

So, when should you use it? Start most new systems as a modular monolith. Split by business area. Keep each module's data private, and give it a front door. Fail the build on any shortcut. And move a module out into its own service only when it truly needs its own deployment, its own scaling, or its own team.

## 12. Thanks for Watching

That's the Modular Monolith pattern. If you remember one sentence, make it this one. One program, with walls inside, and a check that keeps them up. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a shipping module, with its own front door. Then decide which module should call it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
