# CQRS Pattern — Video Narration Script

## 1. CQRS

Hello, and welcome. This video explains the C Q R S pattern, in Java. C Q R S stands for command query responsibility segregation. This video is presented by Jayasekhar Konduru. First, a simple definition. Changing something and reading something are two different jobs. So stop making them the same code. The side that changes things announces what it did. And the side that answers questions keeps an answer already prepared. Think of a restaurant. The kitchen cooks the food. But the menu board by the door is kept up to date separately, so guests can read it without asking the chef. In our online store, we look at one page: the order history page, where a shopper sees what they have bought. We build that page three ways. The middle way is the answer almost everybody reaches for first. And it is not this pattern. By the end, you will be able to explain the difference without using the word fast.

## 2. The Shop, And One Page

Here is the shop. A shopper opens their order history page. Each line shows an order number, a product code, the product's name, and how many they bought. Where does that information live? The order number and product code live in the orders service, which took the order. The product's name lives in the catalog service, which owns names. So to build one line, someone has to ask two services, and join the answers together. That is normal, and it has its own name: the A P I Composition pattern. Now remember one more thing, because the whole video turns on it. An order is placed once. But the page that shows it is opened by the customer, by the confirmation email, by a support agent, and by the customer again next week. The facts changed once. The page is built a thousand times.

## 3. Composed On Every View

Here is the first version, and it is good code. It asks the orders service for this customer's orders. Then it collects every product code. And it asks the catalog for all the names in one single call, not one call per line. Then it joins the two into finished lines. There is no wasted work. Nobody would object to this in a code review. And that is exactly why it survives for years. Let's run it, and see what it costs.

## 4. Act One — Composing On Every View

The shopper opens the page three times. Underneath, each view asks the orders service, which takes thirty milliseconds. Then asks the catalog, which takes sixty. And the same again, for every view. Three views cost two hundred and seventy milliseconds, and six service calls. Now, ninety milliseconds per page is not slow. Nobody will complain about that. Two other things are wrong, and both are worse. The first is waste. All three pages were identical. Nothing had changed. The shop paid full price, three times, for the same answer. The second is quieter. Every view is a live call to two other services. So if the catalog service is having a bad afternoon, the page cannot be shown at all. The customer's own history depends on somebody else being up.

## 5. So Cache It

So what do we do? The answer almost everybody reaches for is this. The page is the same every time, so keep a copy. Cache it. The first view builds the page, stores it, and hands it over. The second view just hands over what was stored. Add a five-minute expiry, so it does not stay out of date forever. And to be clear, this works. It is a real cache, and the second view really is free. So, is that C Q R S? No. And the reason why is the most useful idea in this video.

## 6. The Cache, Honestly

Here is the cache, and there is very little to it. If there are stored lines for this customer, and they have not expired, hand them back. Otherwise, build the page properly, store it, and hand it back. Now ask one question about those stored lines. How would this cache ever find out that what it holds has become wrong? The answer is: it never would. It stored some lines, but it does not understand them. Nothing in the shop can tell it that the world has moved on. The only thing that will ever correct it is the clock running out. Let's watch that happen.

## 7. Act Four — The Rename

The catalog team renames a product. The Stainless Steel Kettle becomes the Brushed Steel Kettle. That is an ordinary change, and they are entitled to make it. Now there are two fast copies of the page in this shop. We ask both what the kettle is called. The cache says: Stainless Steel Kettle. That is the old name, and it is wrong. The other copy says: Brushed Steel Kettle. That is right. Here is the sentence to take away from this video. A cache is a copy that cannot know it is wrong. That cache will keep showing the old name for the next five minutes. Not because five minutes is a bad number. But because nothing in the shop can tell it otherwise. The other copy was corrected by the same event that made it wrong. The rename arrived, and it updated itself. So the difference is not speed. Both are fast. The difference is whether anybody can tell it.

## 8. A Copy That Is Told

Let's put the two side by side. A cache is a copy that cannot know it is wrong. Its only correction is an expiry. The second copy is called a read model. A read model is a copy that is told. The same event that makes it wrong is the one that corrects it. At once, not sometime in the next five minutes. And no expiry setting can turn the first into the second. Set the expiry short, and you lose the saving you wanted. Set it long, and you are wrong for longer. You can tune that number forever, and never win. So here is the question that leads to this pattern. What would have to be true for the copy to know? It would have to be told. So, who would tell it?

## 9. The Whole Mechanism

Here is the whole mechanism, and it is small. When the write side places an order, it does its work. Then it announces what it did. It publishes a fact, called an event: an order was placed. Something is listening: the read model. When a fact arrives, it updates the lines it holds. An order was placed, so add its lines. A product was renamed, so change that name everywhere. The stock changed, so record the new number. That is all. One side announces. The other side listens, and keeps a prepared answer. One small detail saves real trouble. The list of event types is fixed, and Java knows it. So if someone adds a fourth kind of event, and forgets to teach the listener, the code will not compile. Without that, the read model would quietly ignore new facts, drift away from the truth, and every test would still pass.

## 10. Act Two — The Page Kept Ready

Same customer, same page, same three views. The page itself is identical. A kettle at thirty-four pounds ninety-nine, and four mugs at thirty-five pounds ninety-six. Three views now cost fifteen milliseconds, instead of two hundred and seventy. But the more important number is this one. Zero service calls. Not fewer. Zero. Showing the page touches neither the orders service nor the catalog. One test switches the orders service off completely, and the page still shows. The first version could never do that, at any speed. Now, to be honest, the work did not vanish. The catalog was still called once, when the order was placed. The joining still happened. It just happened when writing, not when reading. That is only a good trade because of the ratio from the start. One order is placed, and the page is shown a thousand times. If something is written constantly and read rarely, this pattern is a loss.

## 11. What You Are Actually Buying

So let's add up the bill. What you bought. Reads that cost one lookup. And a page that still works when other services are down. What you paid. First, the work moved to write time. It is only affordable because you read far more often than you write. Second, you now have a second copy of the data. Somebody has to keep it, and fix it when it breaks. And third, the one that decides whether you can use this pattern at all. There is now a window of time in which that copy is behind. Let's look at that window.

## 12. Act Three — The Window, Shown

This is the most uncomfortable moment in the project, and it is here on purpose. An order is placed. It is paid for. It is final. Three events are still on their way. And the customer's order history page shows no lines at all. The customer has just given this shop money. And they are looking at a page without their order on it. Nothing is broken. No error was raised. The facts are true. They just have not arrived yet. Two things make this acceptable, and you need both. The window is short. And it closes by itself. No operator, no retry button, no overnight job. The events arrive, and the page shows two lines. So decide, page by page, whether you can live with that window. For an order history page, almost certainly yes. For the screen a warehouse worker packs boxes from, that is a much harder question. Ask it before you build, not after.

## 13. Who Does What

Here are all the pieces, in one place. On one side is the design we are replacing. A page built on every single view, asking two services every time. And beside it, the cache: fast, but corrected only by a timer. What matters about the cache is what is missing. Nothing connects it to the events. It does not listen. It only remembers what it was handed. On the other side is the split. The write service first reserves stock from the ledger, the true record of stock. That is where a sale is really decided. Then it announces what it did. The events carry three kinds of fact. An order was placed. A product was renamed. The stock changed. And the read model listens, and holds lines that are already put together. One more comfort. The read model can be rebuilt from the events. If it breaks, you throw it away, and replay the events.

## 14. Act Five — The Last Kettle

There is one kettle left in the shop. Somebody buys it. For a moment, the read model still says one is on the shelf. But the ledger, the true number, says zero. That is the window again. At that moment, a second shopper tries to buy a kettle. The page they see says yes. And the shop is still fine. Because the page did not decide the sale. The sale went to the ledger. And the ledger refused: there are none left. So here is the rule. Show a read model's number. Never decide anything with it. Show the stock level, the balance, or what someone is allowed. But when something is being allowed or refused, a sale, a payment, or access, ask the side that owns the number. And to be honest, nothing enforces that rule. Not the compiler. Only a test, a code review, and people remembering. One real comfort to finish. If the read model is wrong, or broken, you throw it away. Six events are replayed, and the two lines come back.

## 15. What To Remember

Here are five things to remember. One. Commands change things, and queries read things. They are different jobs. Two. A cache is a copy that cannot know it is wrong. A read model is a copy that is told. Three. The work moved to write time. It did not vanish. So if something is rarely read, do not do this. Four. The window where the copy is behind is real. It is only acceptable because it closes by itself. Five. Show a read model's number. Never decide anything with it.

## 16. Thanks for Watching

That's the C Q R S pattern. If you remember one sentence, make it this one. A cache is a copy that cannot know it is wrong, a read model is a copy that is told, and nothing is ever decided from the fast copy. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. There is no message broker and no database, on purpose, so the lesson stays on which copy may decide. Here is one exercise to try. Change the second shopper so it checks the read model's stock number, and sells if it says yes. Watch the test fail. In a real shop, that failure is a customer charged for a kettle that does not exist. And one question to think about. Pick a page in your own system. How many times is it read, for every time its facts change? If that number is small, is a second copy of the data really worth keeping? If you found this useful, a like really helps other people discover it. Kindly subscribe to the channel. It helps the channel grow and bring you more content. Thanks for watching!
