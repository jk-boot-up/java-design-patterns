# Multiton Pattern — Video Narration Script

## 1. Multiton

Hello, and welcome. This video explains the Multiton pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. A multiton is like a singleton, but with a key. It keeps exactly one instance for each key. And it hands back that same instance every time the key is asked for. Think of a hotel's key cabinet. There is exactly one hook for each room number. Ask for room twelve, and you always get the same key. In our online store, there is one warehouse for each region. And every part of the shop must agree about which warehouse is which. In this video, two copies of one warehouse disagree. Then there is one warehouse per region, and everyone agrees. We will hear unknown regions refused, a race between two threads, and then the cost.

## 2. The Scenario

Here is the scenario. The shop has a warehouse in the UK, one in the EU, and one in the US. Many parts of the shop reserve stock. And all of them must see the same stock for a region. So here is the question. How do they share each warehouse?

## 3. A New One Each Time

First, the naive way: a new warehouse object each time. Two callers each create a UK warehouse. They are not the same object. One has a stock of ninety. The other has a stock of one hundred. The shop now believes two different things about one real warehouse.

## 4. The Pattern

Now, the pattern. The warehouse class has a private constructor. So nobody outside can create one. It keeps a map, from each region to its one warehouse. Ask for a region, and you get the one warehouse for it. It is created the first time that region is asked for.

## 5. One Per Region

Second demo: one warehouse per region. Ask for the UK twice, and you get the same object. Ask for the EU, and you get a different one. Warehouses created so far: two.

## 6. Shared, So They Agree

Third demo: shared, so everyone agrees. One part of the shop reserves ten items in the UK. Another part asks for the UK warehouse, and sees a stock of ninety. And the EU warehouse still has one hundred.

## 7. A Fixed Set Of Keys

Fourth demo: a fixed set of keys. Someone asks for a warehouse on Mars. It is refused: there is no warehouse in Mars. Warehouses held: three.

## 8. Two Threads, One Region

Fifth demo: two threads, one region. First, the careless way. Look in the map first, and create second, with no lock. Both threads look before either one creates. So two warehouses are created, and they are not the same object. Now the careful way: an atomic, create if absent. Eight threads ask at once. They all get the same object. And exactly one is created.

## 9. The Bill

Finally, the cost. One test reserves thirty items. The next test starts, and asks for the UK warehouse. Its stock is seventy, not one hundred. State leaks from one test into the next. The warehouses live as long as the program does. Nothing ever lets one go. And any code, anywhere, can reach any warehouse. So finding out who changed the stock is hard.

## 10. How To Recognise It

How can you spot this pattern in code someone else wrote? Look for a static map of instances, and a get instance method that takes a key. Look for a concurrent map's compute if absent, used to create on demand. In Java itself, look at Currency get instance, and Charset for name. And enums, which are a multiton built into the language.

## 11. The Verdict

So, here is the verdict. Use a multiton when there must be exactly one object, for each of a small, fixed set of keys. Create the objects with an atomic, create if absent. Give tests a way to reset. And when you can, prefer passing the object in. So that the sharing is visible.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? If an enum can name the fixed set, use an enum. If the object can be passed in, pass it in. A multiton is global state, with a key.

## 14. Thanks for Watching

That's the Multiton pattern. If you remember one sentence, make it this one. A multiton gives exactly one instance for each key, and the price is global state that outlives every test. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Add a fourth region. And confirm that nothing else in the shop has to change. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
