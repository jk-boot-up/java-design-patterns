# Routing Slip with Apache Camel Pattern — Video Narration Script

## 1. Routing Slip with Apache Camel

Hello, and welcome. This video explains the Routing Slip pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A routing slip is a list of steps, written once, that travels with a message. Each step does its job, and passes the message to the next step on the list. Apache Camel is an open-source library for moving messages, and it follows slips for you. Think of a hospital treatment card. Reception writes down the departments this patient must visit. Each department does its part, and sends the patient to the next name on the card. In this video, the domain is an online shop's order processing. By the end, you will hear how Camel follows each order's slip. How to add a step with one rule. And what to use when the next step must be decided on the way.

## 2. The Scenario

Here is the scenario. The shop has six steps. Validate, age check, customs, charge, gift wrap, and pack. Every order visited all six. Four orders made twenty-four visits. Only fifteen did any work.

## 3. Act One — One fixed pipeline

First demo: one fixed pipeline for every order. Every order visits all six steps. Four orders, twenty-four visits. Only fifteen of them did any work. The rest were steps checking whether they applied, and finding they did not.

## 4. Act Two — The slip

Second demo: the slip. As each order sets off, the slip writer lists the steps it needs. Order one needs validate, charge and pack. Order two is a gift, so it adds gift wrap. Order three is age restricted, so it adds an age check. Order four goes abroad, so it adds customs. The list travels with the order, in a header.

## 5. Act Three — Camel follows the slip

Third demo: Camel follows the slip. The routing slip step reads the header, and sends the order to each step in turn. Fifteen visits in all. Every one doing work. And no step knows which step comes after it.

## 6. Act Four — A new step

Fourth demo: a new step. Orders over five hundred pounds need a fraud check. One rule is added, where slips are written. Order four now goes through the fraud check, before it is charged. No route, and no other step, changed.

## 7. Act Five — The bill, and a dynamic router

Fifth demo: the bill. Order five's customer is too young. The age check fails. The slip just stops. Charge and pack are still on it. A slip cannot change course, because it was written at the start. Camel has a relative, the dynamic router. It decides each next step as it goes. It sends order five to a step that tells the customer why.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. Write each order's steps into a header. The routing slip step follows them, one by one. And when the next step depends on what just happened, the dynamic router decides it on the way.

## 9. Who Does What

Here is who does what. The slip writer lists each order's steps, once. Shop routes holds the routing slip, and the dynamic router. The steps do the work. And the order's details decide which steps it needs.

## 10. Where You Have Seen It

You have probably met this already. Camel's routing slip. Hospital treatment cards, and the job travellers that follow parts through a factory. And documents that carry their own chain of approvers.

## 11. When To Use It

So, when should you use it? When different messages need different steps, known at the start. When the next step depends on what just happened, use the dynamic router, or a process manager, instead.

## 12. Thanks for Watching

That's the Routing Slip, with Apache Camel. If you remember one sentence, make it this one. Write the route once, and let the message carry it. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a loyalty points step, for registered customers. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
