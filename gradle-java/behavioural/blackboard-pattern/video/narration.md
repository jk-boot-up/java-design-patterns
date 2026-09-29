# Blackboard Pattern — Video Narration Script

## 1. Blackboard

Hello, and welcome. This video explains the Blackboard pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In the blackboard pattern, several independent experts share one board of facts. Each expert adds what it knows, as soon as it has what it needs. And a controller decides who goes next, and stops as soon as the answer is clear. Think of an incident room in a detective story. A board on the wall holds every clue so far. Whoever can add something steps up. And the lead detective closes the case the moment there is enough to go on. In this video, the domain is an online shop. Before it accepts an order, it checks for fraud. Where the card is from, where the shopper is, how many orders they placed recently, and more. By the end, you will hear why one method that runs every check wastes time. How experts on a shared board fix it. How the controller stops early. And what the pattern costs.

## 2. The Scenario

Here is the scenario. Before accepting an order, the shop runs six fraud checks. Where is the card from? Where is the shopper? Do those match? How many orders did this account place in the last hour? How big is the order? And is the device a real phone? That last check is slow: eight hundred milliseconds. Each check adds risk points. Sixty or more, and the order is rejected.

## 3. Act One — Every check, every time

First demo: one method runs every check, in a fixed order. Card country. Shopper's country. Do they match. Orders in the last hour. Order value. And a device check that takes eight hundred milliseconds. A risky order comes in. After the five cheap checks, the answer is already clear: reject. But the slow device check runs anyway. Nine hundred and two milliseconds in total. And adding a new check means editing this one method, and getting the order right by hand.

## 4. Act Two — The blackboard

Second demo: the blackboard. Each check is now an independent expert. It only says two things. What facts it needs, and what it adds. A good order goes on the board. A controller looks for experts that are ready, and lets the cheapest go first. Order value is ready straight away. Then card country, and I P country. The moment both countries are on the board, the comparison becomes ready. Nobody had to write that order down. Six checks, and a risk score of zero. Approved.

## 5. Act Three — Stopping early

Third demo: the controller stops as soon as it can decide. The risky order has a British card, but the shopper is in Russia. Forty risk points. The account placed five orders in the last hour. Thirty more. The score is seventy. Anything over sixty is rejected. So the controller stops. Five checks, one hundred and two milliseconds. The slow device check never runs.

## 6. Act Four — A new expert

Fourth demo: a new expert joins. Fraudsters start buying gift cards. So a new check is written. Over two hundred pounds of gift cards adds sixty risk points. It is simply added to the list of experts. No other check changes, and neither does the controller. Six gift cards, three hundred pounds. Rejected. Without the new expert, it would have been approved.

## 7. Act Five — The bill

Fifth demo: the bill. Nobody wrote down the order of events. It is chosen while the program runs. So when someone asks why an order was rejected, the log is the only story. And the board is shared. Every expert can read every fact on it. Including the card number.

## 8. The Pattern

Let's name the pattern. There are three parts. The blackboard holds the facts, shared by everyone. The experts, called knowledge sources, each say which facts they need, and what they add. They never call each other. And the controller asks who is ready, picks who goes next, and decides when to stop.

## 9. Who Does What

Here is who does what. The blackboard holds the facts, the risk score, and a log of every contribution. Knowledge source is the interface every expert follows. Are you ready? Then contribute. The checks class holds the six fraud experts, and later the gift card one. The controller runs the cheapest ready expert, and stops at sixty. And fraud check all is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Fraud and risk engines combine many independent signals into one score. Rule engines such as Drools fire a rule when the facts it needs are present. The pattern was born in early speech recognition systems. And today, AI agents that post findings to a shared memory are using it again.

## 11. When To Use It

So, when should you use it? When many independent pieces of knowledge combine into one decision. When their order depends on what is already known. And when new pieces arrive often. Keep each expert small. Log every contribution. And decide carefully what the board may show to each expert. When the steps are always the same, a plain method is simpler.

## 12. Thanks for Watching

That's the Blackboard pattern. If you remember one sentence, make it this one. Let experts share one board, and stop as soon as the answer is known. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Hide the card number from every check, except the one that needs it. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
