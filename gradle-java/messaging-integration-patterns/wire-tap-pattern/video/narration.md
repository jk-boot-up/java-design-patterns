# Wire Tap Pattern — Video Narration Script

## 1. Wire Tap

Hello, and welcome. This video explains the Wire Tap pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A wire tap is attached to a channel of messages. It sends a copy of every message to a second listener, such as an audit log. The real message carries on to its destination, untouched. Think of the message: calls may be recorded for training purposes. The customer and the agent talk as normal. A recorder quietly keeps a copy. And when a card number is read out, the recording pauses. In this video, the domain is an online shop. Checkout sends payment messages, charges and refunds, to the payment service. By the end, you will hear why typing logging into services goes wrong. How a wire tap fixes it. How taps come and go. And what a tap must never do.

## 2. The Scenario

Here is the scenario. Checkout sends payment messages to the payment service. Charges, and refunds. A customer disputes a refund. Someone needs to see exactly which messages went through.

## 3. Act One — Logging typed in by hand

First demo: logging typed into the payment service, by hand. Four payment messages are sent. Three charges, and one refund. Only three appear in the log. Nobody added logging to the refund code. And the lines that are there show the full card number.

## 4. Act Two — A wire tap

Second demo: a wire tap, on the channel itself. An audit log is attached to the channel. Every message is copied to it, charges and refunds alike. The copies show only the last four digits of each card. The payment service handles all four messages, exactly as before. Neither service was changed.

## 5. Act Three — Attach and detach

Third demo: attach while investigating, detach afterwards. The investigation is over. The tap is detached. Order four flows through, exactly as normal. The audit log still holds its four lines.

## 6. Act Four — A second tap

Fourth demo: a second tap, for a sales dashboard. It adds up the charges, and takes off the refunds. Net takings: fifty-eight pounds forty-two. Again, no service changed.

## 7. Act Five — The bill

Fifth demo: the bill. A tap that takes a tenth of a second per copy slows the real payments. Four payments take over four tenths of a second. Run the same tap on its own thread, and the payments take under five hundredths of a second. And a tap sees everything. Mask card numbers, before anything is copied.

## 8. The Pattern

Let's name the pattern. Attach a tap to the channel itself. Every message is delivered as normal. And a copy goes to the tap. The sender and the receiver are not changed at all. Taps can be attached, and detached, while the shop runs.

## 9. Who Does What

Here is who does what. The channel delivers each message, and hands a copy to every attached tap. The audit log keeps copies, with card numbers masked. The sales meter keeps a running total. Async runs a slow tap on its own thread. And the payment service is the real destination.

## 10. Where You Have Seen It

You have probably met this pattern already. Apache Camel and Spring Integration both have a wire tap. In Kafka, a separate consumer group can read a topic for auditing. Network switches mirror traffic to monitoring tools. And call centres record calls.

## 11. When To Use It

So, when should you use it? For auditing, debugging, and dashboards. Mask sensitive data before anything is copied. Run slow taps on their own thread. And detach the taps you no longer need.

## 12. Thanks for Watching

That's the Wire Tap pattern. If you remember one sentence, make it this one. Watch the traffic from the channel, never from inside the services. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the audit tap write to a file, on its own thread. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
