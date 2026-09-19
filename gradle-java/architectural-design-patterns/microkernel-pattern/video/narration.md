# Microkernel Pattern — Video Narration Script

## 1. Microkernel

Hello, and welcome. This video explains the Microkernel pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a microkernel keeps a small core that only knows how to keep plugins and run them. Every feature lives in a plugin. This is another project in the architecture category, whose subject is how a whole application is arranged, and who may depend on whom. In our online store, the checkout keeps gaining features, and every one means editing the same class. By the end you will see a checkout that has to be edited for every new feature, see a core and plugins, see a plugin added and removed while running, see a broken plugin not stop the others, see the order of plugins change the price, and see the bill, which is a narrow interface and results that depend on what is installed.

## 2. The Scenario

Here is the scenario. The checkout has a member discount and a shipping fee. Now the marketing team wants gift wrap, then loyalty points, then more. The question: must we edit the checkout every time?

## 3. Every Feature Inside

First, every feature inside. Gift wrap is asked for, and the checkout does not support it. The total is unchanged. To add it, we must edit the checkout, test all of it again, and release all of it.

## 4. The Pattern

The pattern. A small core. It knows one interface, called plugin. It keeps plugins, starts and stops them, and runs them. Every feature is a plugin.

## 5. A Core And Plugins

Second, a core and plugins. The core has two plugins: member discount and shipping fee. A total of ten thousand becomes ninety five hundred. The core knows one interface, and nothing about discounts or fees.

## 6. A New Feature, No Change

Third, a new feature, with no change to the core. Gift wrap is registered while the system is running. It is started, and the total is ninety eight hundred. Then it is taken away again, and stopped, and the total goes back to ninety five hundred. The core was not changed.

## 7. A Plugin That Breaks

Fourth, a plugin that breaks. The loyalty points plugin throws an error. The core records it, and carries on. The other plugins still ran, and the total is ninety five hundred.

## 8. Order Matters

Fifth, order matters. Discount then fee gives ninety five hundred. Fee then discount gives ninety four fifty. The same two plugins, and a different price. The core cannot know which is right.

## 9. The Bill

Last, the bill. The interface offers one thing: adjust a total. Plugins want more: the customer's country, and a line on the receipt. If the interface grows, every plugin feels it. If it does not, plugins reach around the core. And a customer's total is now decided by whichever plugins are installed, in some order.

## 10. How To Recognise It

How do you recognise this in code you did not write? A Plugin or Extension interface loaded by name or from a folder. ServiceLoader in Java. IDEs, browsers with extensions, and build tools with plugins. OSGi bundles and the Eclipse platform.

## 11. The Verdict

Here is my verdict, plainly. Use a microkernel when features come and go, and different customers or teams need different sets. Keep the core tiny and the interface stable. Decide the order of plugins on purpose. Isolate a failing plugin. Do not use it for a system whose features never change.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If the features are few and fixed, plain classes are simpler. A plugin system costs an interface, a lifecycle and a way to order things, and pays off only when the set of features truly varies.

## 14. Thanks for Watching

That's Microkernel. If you take one sentence away, take this one: a microkernel puts every feature in a plugin and keeps the core small, and the price is a narrow interface and results that depend on what is installed. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a plugin that rounds the total to the nearest ten cents, and decide where in the order it goes. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
