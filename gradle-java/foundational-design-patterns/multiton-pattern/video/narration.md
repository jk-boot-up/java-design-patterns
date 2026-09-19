# Multiton Pattern — Video Narration Script

## 1. Multiton

Hello, and welcome. This video explains the Multiton pattern in Java, and it is written and presented by Jayasekhar Konduru. The plain definition: a multiton is a singleton with a key. It keeps exactly one instance for each key, and hands back that same instance every time the key is asked for. This is another project in the foundational category, whose subject is how an object gets hold of another, and how small idioms shape everyday Java. In our online store, there is one warehouse for each region, and every part of the shop must agree about which warehouse is which. By the end you will see two copies of one warehouse disagree, see one warehouse per region, see the parts of the shop agree, see unknown regions refused, see two threads make two warehouses without a lock and one with an atomic create, and see the bill, which is leaked state and instances that live forever.

## 2. The Scenario

Here is the scenario. The shop has a warehouse in the UK, one in the EU, and one in the US. Many parts of the shop reserve stock, and all of them must see the same stock for a region. The question: how do they share it?

## 3. A New One Each Time

First, a new one each time. Two callers each made a UK warehouse. They are not the same object. One has stock ninety, the other a hundred. The shop now believes two different things about one warehouse.

## 4. The Pattern

The pattern. A private constructor. A map from key to instance. Ask for a key, and you get the one instance for it, made the first time it is asked for.

## 5. One Per Region

Second, one per region. Asked for the UK twice, it is the same object. Asked for the EU, it is a different one. Created so far: two.

## 6. Shared, So They Agree

Third, shared, so they agree. One part of the shop reserved ten in the UK. Another part, asking for the UK, sees stock ninety. The EU warehouse has a hundred.

## 7. A Fixed Set Of Keys

Fourth, a fixed set of keys. Asked for Mars, it is refused: no warehouse in Mars. Instances held: three.

## 8. Two Threads, One Region

Fifth, two threads, one region. Look first, create second, with no lock: both threads looked before either created. Not the same object, and two were created. With an atomic create if absent, eight threads at once get the same object, and one is created.

## 9. The Bill

Last, the bill. One test reserved thirty. The next test starts, and asks for the UK: stock seventy, not a hundred. State leaks from one test to the next. The instances live as long as the program does, and nothing ever lets one go. And any code can reach any warehouse from anywhere, so who changed the stock is hard to say.

## 10. How To Recognise It

How do you recognise this in code you did not write? A static Map of instances and a getInstance(key) method. ConcurrentHashMap.computeIfAbsent used to create on demand. Currency.getInstance(code), Locale constants and Charset.forName. Enums, which are a multiton the language provides.

## 11. The Verdict

Here is my verdict, plainly. Use a multiton when there must be exactly one object for each of a small fixed set of keys. Create with an atomic create-if-absent. Give tests a way to reset. And prefer passing the object in, when you can, so that the sharing is visible.

## 12. What Is Real Here

The same honest admission as everywhere in this course. Everything is plain Java. Every number quoted comes from this program's own output. Nothing depends on a clock, so every run is the same.

## 13. When This Is Too Much

So when is it too much? If an enum can name the fixed set, use an enum. If the object can be passed in, pass it in. A multiton is global state with a key.

## 14. Thanks for Watching

That's Multiton. If you take one sentence away, take this one: a multiton gives exactly one instance for each key, and the price is global state that outlives every test. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository, running offline with nothing installed but a Java development kit. If you try one exercise, add a fourth region, and confirm that nothing else changes. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
