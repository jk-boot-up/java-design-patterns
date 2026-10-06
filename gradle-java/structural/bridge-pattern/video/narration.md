# The Bridge Pattern Pattern — Video Narration Script

## 1. The Bridge Pattern

Hello, and welcome. This video explains the Bridge pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Bridge pattern splits one tangled family of classes into two separate families. One for what something does, and one for how it gets done. The two are joined by a simple reference, not by inheritance. So each side can grow without multiplying the other. Think of a T V remote and a television. The remote knows what you want. The television knows how to do it. In our online store, notifications are sent by email, text message, and push notification. By the end, you will know why what a message says, and how it is delivered, should never live in the same class. And how to write the split yourself.

## 2. The Scenario

Here is the scenario. The store sends several kinds of notification. Order confirmations, shipping updates, and password resets. And there are several channels to send them on. Email, text message, and push notification. The rule is: every kind of notification must work on every channel.

## 3. Two Very Different Things, Tangled Together

There are two very different jobs here. First, what a notification says: its subject, and its body. Second, how it is delivered. Email sends it unchanged. A text message must cut long messages short. A push notification drops the body, and shows only the subject. Done naively, one class does both jobs, for every combination of notification and channel.

## 4. The Naive Approach — One Class Per (Notification, Channel)

Here is the naive approach. One class handles order confirmations sent by text message. It writes its own subject and body. Then it cuts the text at a hundred and forty characters, the text message limit. And here is the problem. Separate classes for order confirmation by email, shipping update by email, and shipping update by text message all repeat the same shape. And the hundred-and-forty-character rule is copied into every text message class.

## 5. Why That Hurts

That does real damage as the system grows. Three kinds of notification, times three channels, means nine classes. Add a new channel, and you write one class for every kind of notification. Add a new kind of notification, and you write one for every channel. The text message rule is copied into every text message class. Fix a bug in it, and you must find every copy. What a message says, and how it is sent, are welded together. Neither can change without touching the other.

## 6. The Bridge Pattern

The Bridge pattern fixes exactly this. The classic book on design patterns, by the authors known as the Gang of Four, describes it like this. Separate an abstraction from its implementation, so the two can vary independently. In plain words: two small families of classes, connected by one field. Not by inheritance, and not by one giant class doing everything.

## 7. Remember It With a TV Remote

Here is how to remember it. Think of a T V remote, and a television. The remote knows the high-level actions: volume up, next channel, power. The television knows how to actually change its own volume, on its own hardware. Any remote works with any television that understands the same signal. And a maker can redesign the television completely, without changing what a single button means. Two families, one connection, and each can change on its own.

## 8. The Four Roles

Every bridge has four roles. The abstraction: a notification. It knows what to say, and holds a reference to a channel. The implementor: the message channel, a shared interface every channel follows. Refined abstractions, like the order confirmation notification. They add content, but never delivery logic. And concrete implementors, like the email channel and the text message channel. They add delivery logic, but never know what content they carry. Here is the most important idea in this video. A notification holds its channel as a plain field. Not through inheritance. That one field is the whole bridge.

## 9. The Abstraction — Notification Holds, and Delegates

Here is the abstraction: the notification class. It holds a message channel, set once when it is created. Its send method is fixed. No kind of notification can change how sending works. Send asks the notification for its subject and body. Then it hands both straight to the channel. It never checks whether the channel is email, text message, or push. It does not need to.

## 10. A Concrete Implementor — SmsChannel Owns Its Own Rule

Here is one concrete implementor: the text message channel. The hundred-and-forty-character rule is written exactly once, right here. Every kind of notification sent by text message gets that rule for free. Because they all use this one channel. Fix the limit here, and every kind of notification gets the fix automatically.

## 11. A Refined Abstraction — Content, Never Delivery

Here is a refined abstraction: the order confirmation notification. It writes the subject and the body of the message. Nothing here mentions email, text messages, or push. Adding a new kind of notification, like a back-in-stock alert, costs exactly one new class like this. And it works with every channel that already exists.

## 12. The Client — Mix and Match, Freely

Here is the code that ties it all together. The same order confirmation goes out through three different channels. Just by passing a different channel when it is created. And the last line is the best part. A password reset, a brand new kind of notification, already works with the same email channel. No new channel code needed. That is the whole payoff.

## 13. Running It

Let's run the project. The same order confirmation goes out over three channels. Email and push both deliver it. And so does the text message, because this message is short enough. Then a longer shipping update. By email, it arrives unchanged. By text message, it is cut off, right at the hundred-and-forty-character mark. The same content, two different results, decided entirely by the channel.

## 14. Wrap Up

So, to recap. Use a bridge when two things vary independently. And you do not want a class for every combination. Keep the notification side unaware of each channel's quirks. If a kind of notification ever needs to know a channel's details to do its job, the bridge is leaking. And one comparison worth knowing. The Adapter pattern fixes two interfaces that already exist, and disagree. A bridge designs two families from the start, so they only ever meet at one point.

## 15. Thanks for Watching

That's the Bridge pattern. If you remember one sentence, make it this one. Split what something does from how it is done, and join them with one field, so each side can grow on its own. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a back-in-stock alert. And check that it works on all three channels, with no other change. If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
