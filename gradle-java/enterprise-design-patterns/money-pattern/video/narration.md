# Money Pattern — Video Narration Script

## 1. Money

Hello, and welcome. This video explains the Money pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. The Money pattern keeps a price as a whole number of the smallest coin, such as pence, together with its currency. Never as a number with a decimal point. So every sum is exact, pounds are never added to dollars, and nothing is rounded unless you ask. Think of the cash drawer in a shop. It does not hold nineteen point nine nine of anything. It holds coins: one thousand nine hundred and ninety-nine pence, all of them pounds. You can count coins exactly, and share them out exactly. In this video, the domain is an online shop. It adds up baskets, charges VAT, gives discounts, and sells in pounds, dollars and yen. By the end, you will hear why ten pence plus twenty pence is not thirty pence in a double. How the Money class fixes it. Why rounding is a decision. And how to split ten pounds three ways without losing a penny.

## 2. The Scenario

Here is the scenario. The online shop adds up baskets. It charges VAT, which is a tax added to the price. It spreads a basket discount across the lines. And it sells in pounds, dollars and yen. The first version kept every price in a double. A double is Java's ordinary number type for values with a decimal point. Every test passed. So what could go wrong?

## 3. Act One — Prices as Doubles

First demo: prices as doubles. A ten pence sticker plus a twenty pence sticker. The total prints as zero point three, followed by fifteen zeros and a four. Is it equal to zero point three? No. Next, a thousand items at ten pence, added one by one. The total is ninety-nine point nine nine nine, and some more nines. Turn that into pence by cutting off the fraction, as a lot of code does, and you get nine thousand nine hundred and ninety-nine pence. A penny short. And ten dollars plus ten pounds is simply twenty. Nobody asked which currency.

## 4. Why A Double Gets It Wrong

Why does this happen? A double stores numbers in binary: ones and zeros. Some fractions cannot be written exactly in binary. One tenth is one of them. You already know this problem from ordinary numbers. One third, written as a decimal, is zero point three three three, going on forever. You have to stop somewhere, so it is never quite exact. In the same way, a double stores ten pence as very, very nearly ten pence. Add enough of them, and the tiny errors add up to a missing penny.

## 5. The Pattern

Now, the pattern. Store the amount as a whole number of the smallest coin. Nineteen pounds ninety-nine becomes one thousand nine hundred and ninety-nine pence. Whole numbers add and multiply exactly. Keep the currency with the amount, in the same object. And only round when someone says how. That object is called Money.

## 6. Act Two — Prices as Money

Second demo: prices as Money. Ten pence plus twenty pence is exactly thirty pence. Equal to thirty pence? Yes. A thousand items at ten pence is exactly one hundred pounds, stored as ten thousand pence. And a real basket. Three mugs at nine pounds forty-nine. A teapot at twenty-four ninety-nine. Two coasters at four ninety-nine. The total is sixty-three pounds forty-four, with no rounding anywhere.

## 7. Act Three — Currencies

Third demo: currencies. Every Money carries its currency. So ten pounds plus ten dollars is refused, with a clear message: cannot combine pounds with dollars. The currency also knows how many digits it has after the point. Pounds have two. Japanese yen have none. So fifteen hundred yen prints as fifteen hundred, with no pennies. And a price like nine pounds nine hundred and ninety-nine thousandths is refused at the door. Instead of being quietly rounded somewhere later.

## 8. Act Four — Rounding Is A Choice

Fourth demo: rounding. Some sums really do fall between two pennies. Twenty percent VAT on ninety-nine pence is nineteen point eight pence. Money will not round that by itself. The code must say how. And where you round matters. Ten items at ninety-nine pence. Round the VAT on each line, and it comes to two pounds. Round once, on the total, and it comes to one pound ninety-eight. Neither is wrong. But they differ by two pence. A shop must choose one rule, and use it everywhere. Money makes that choice visible.

## 9. Act Five — Splitting

Fifth demo: splitting. Three friends share a ten pound bill. Divide by three, and each pays three pounds thirty-three. But three of those is nine pounds ninety-nine. A penny has vanished. Money has a method called allocate. It rounds each share down, then hands out the leftover pennies one at a time. So the shares are three thirty-four, three thirty-three and three thirty-three. Exactly ten pounds. The cart uses the same method to spread a five pound discount across its lines, by value. Two twenty-five, one ninety-seven, and seventy-eight pence. Exactly five pounds.

## 10. The Pieces

Let's name the pieces. Money holds two things: a whole number of the smallest coin, and a currency. Currency knows its symbol, and how many digits it has. Cart holds lines, each priced in Money. And the naive cart, with its doubles, is kept only so you can compare. One more detail. A Money never changes. Adding two amounts gives you a new Money, and leaves both originals alone. So a price can be shared safely, anywhere.

## 11. Act Six — The Bill

Finally, the bill. A price is now a class, not a plain number. So every database, message and screen has to convert it. Nineteen ninety-nine is stored as one thousand nine hundred and ninety-nine, plus the letters G B P. And Money does not convert currencies. Turning pounds into dollars needs an exchange rate, and a date. That is a separate job. Both costs are small, compared with a shop whose totals are a penny out.

## 12. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a class named Money, Amount or Price, holding an amount and a currency. Look for fields like price in pence, or amount in cents, stored as whole numbers. Or Java's big decimal type with a rounding rule, and never a double, anywhere near a price. Payment services like Stripe work the same way. They take nineteen ninety-nine as one thousand nine hundred and ninety-nine, plus a currency.

## 13. The Verdict

So, here is the verdict. Use Money for every price, fee and balance. Store whole units, plus a currency. Round only at a decided point, with a named rule. And split amounts with allocate, so no penny is ever lost. In a real system, use a tested library, such as Moneta, from the Java Money standard. But write your own once, like this, to understand it.

## 14. Thanks for Watching

That's the Money pattern. If you remember one sentence, make it this one. A price is a whole number of the smallest coin, plus its currency, and it only rounds when you decide. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add euros as a fourth currency. And notice how few lines have to change. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
