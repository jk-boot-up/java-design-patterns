# Wire Tap with Apache Camel Pattern — Video Narration Script

## 1. Wire Tap with Apache Camel

Hello, and welcome. This video explains the Wire Tap pattern, built with Apache Camel, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A wire tap sends a copy of every message to a side channel. The sender and the receiver carry on as if nothing were listening. Apache Camel is an open-source library for moving messages, and it has a wire tap built in. Think of a security camera over a shop till. It records every sale, and the cashier does nothing differently. But the camera must only ever see a copy of the receipt, never change the real one. In this video, the domain is an online shop's payments, and the auditors who want a copy of each one. By the end, you will hear how one step taps every payment. A trap where the tap changes the real message. How to fix it. And what a tap on its own thread costs.

## 2. The Scenario

Here is the scenario. Logging had been typed into the payment service by hand. It missed the refunds. And it wrote out full card numbers. Auditors want a masked copy of every payment, without changing checkout, or the payment service.

## 3. Act One — A tap on the route

First demo: a wire tap on the payments route. One step is added to the route. It sends a copy of every message to the audit. All four payments are copied. The refund too. Card numbers are masked in the audit. The payment service handles all four, as before. It was not changed.

## 4. Act Two — Not a copy after all

Second demo: the tap was not handed a copy. Camel gave the audit the very same message object. So when the audit masked the card number, it masked the real one. Checkout's own payment message now shows only the last four digits. A real charge would fail.

## 5. Act Three — onPrepare: a real copy

Third demo: give the tap its own copy. Camel has a step for this, called on prepare. It runs just before the copy is sent. There, the message is copied. The audit still gets four masked lines. And checkout's message keeps its full card number.

## 6. Act Four — The audit stops

Fourth demo: the audit stops. The audit route is switched off, for maintenance. Another order is paid. The copy to the audit fails. But the order is still charged. Checkout and the payment service never hear about it.

## 7. Act Five — The bill

Fifth demo: the bill. The audit is made slow. A tenth of a second, for every copy. Four payments still finish quickly. The tap runs on its own thread. But the audit falls behind, and only catches up later. And copies still waiting are only in memory. If the program stops, they are lost. For a real audit, tap to a durable queue.

## 8. The Pattern, in Camel

Let's name the pattern, in Camel's words. The wire tap step sends a copy to another route, on its own thread. On prepare makes sure it really is a copy. And the main route carries on, without waiting.

## 9. Who Does What

Here is who does what. Shop routes holds the payments route, with its tap. The audit masks each card number, and records a line. The payment service does the real work. And the payment message is what flows through.

## 10. Where You Have Seen It

You have probably met this already. Camel's wire tap, and Spring Integration's. Network switches that mirror a port, so traffic can be watched. And services that read a Kafka topic, only to audit it.

## 11. When To Use It

So, when should you use it? When auditors or a dashboard need a copy of traffic, without touching the sender or receiver. Always make the copy independent. Watch the tap's errors separately. And tap to a durable queue, when no copy may be lost.

## 12. Thanks for Watching

That's the Wire Tap, with Apache Camel. If you remember one sentence, make it this one. Copy every message to the side, and make sure it really is a copy. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the payment message immutable, and see why the trap disappears. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
