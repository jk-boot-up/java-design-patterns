# Double-Checked Locking Pattern — Video Narration Script

## 1. Double-Checked Locking

Hello, and welcome. This video explains the Double-Checked Locking pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Double-checked locking creates a shared object only when it is first needed. It checks for the object first, without a lock. Only if the object looks missing does it take the lock, and check again. Think of the last person leaving an office. You glance at the lights on the way out. Only if they look on, do you walk back and check properly before switching them off. In our online store, the price list is expensive to build. In this video, two threads will build it twice. We will try locking every time, then checking twice. We will hear why one field must be volatile, and the simplest correct way to do it. And then the cost.

## 2. The Scenario

Here is the scenario. The shop's price list is expensive to build. So the shop builds it the first time anyone asks for it. Many threads ask for it. And the first few may ask at exactly the same moment. So here is the question. How do we build it exactly once?

## 3. Check, Then Create

First, the naive way: check, then create. Two threads ask for the price list at the same moment, before it exists. Both see that it is missing. So both build one. Two price lists were built. And each thread holds a different one. One is thrown away, and the expensive work was done twice.

## 4. The Pattern

Now, the pattern. First, look for the object, without a lock. If it is missing, take the lock. Then look again, in case another thread built it while you were waiting. Only then, build it. Once it exists, nobody takes the lock again.

## 5. Lock Every Time

Second demo: lock every time. The same two threads, but now every call takes the lock. Only one price list is built. That is correct. But then a thousand calls arrive, long after the price list exists. And the lock is taken a thousand times. Every caller waits its turn, just to be told something that never changes.

## 6. Check, Lock, Check Again

Third demo: check, lock, and check again. The same race builds just one price list. The second thread waited for the lock. Then it looked again, and found the list already built. And a thousand calls take the lock only once. After that, no call waits for anyone.

## 7. Why It Must Be Volatile

Fourth: why the field must be marked volatile. In this project, it is. Without volatile, Java's memory rules allow a strange thing. One thread could see the reference to the price list, before the price list is fully built. That failure cannot be produced on demand. It depends on the processor and the compiler. So it is not demonstrated here. Instead, a test checks that the field stays volatile.

## 8. The Simplest Correct Way

Fifth demo: the simplest correct way, called the holder idiom. Before anyone asks, nothing is built. After two calls, one is built, and both callers got the same one. How? Java builds a class's static data once, when the class is first used. So the price list sits in a small holder class, and Java does the rest. There is no lock to write, and no volatile to forget.

## 9. The Bill

Finally, the cost. The double-checked version is twenty-nine lines. The holder version is ten. Double-checked locking is ceremony, with one way to be quietly wrong. It only earns its place where the holder cannot be used. For example, when building the object needs an argument. And remember, a lock that nobody else is holding is cheap. Measure before deciding that locking on every call is a problem.

## 10. How To Recognise It

How can you spot this in code someone else wrote? Look for a volatile static field, an if statement checking for null, a synchronized block, and then the same null check again. Look for a small private static class called Holder, with one field. Look for helpers like Lazy, or memoize, in libraries. And look for a comment explaining why the field is volatile.

## 11. The Verdict

So, here is the verdict. For a shared object built on first use, prefer the holder idiom, or an enum. If building the object needs an argument, or can fail and be retried, use double-checked locking. With a volatile field, a local variable, and a test that guards the volatile. And if you have not measured the lock as a problem, simply take the lock on every call.

## 12. What Is Real Here

A quick, honest note about this demo. Everything is plain Java. Every number you heard comes from the program's own output. And nothing depends on the clock, so every run gives the same result.

## 13. When This Is Too Much

So, when is this too much? Nearly always. Most objects built on first use can use a holder, an eagerly built static, or a lock on every call. And a wrong double check causes a bug you cannot reproduce.

## 14. Thanks for Watching

That's Double-Checked Locking. If you remember one sentence, make it this one. Double-checked locking saves the lock after the object is built, and costs a rule you can break without ever seeing it fail. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Remove the volatile keyword. Then explain why no test can fail, and what that means for your code. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
