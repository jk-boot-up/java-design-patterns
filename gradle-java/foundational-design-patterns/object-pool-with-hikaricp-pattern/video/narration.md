# Object Pool with HikariCP Pattern — Video Narration Script

## 1. Object Pool with HikariCP

Hello, and welcome. This video explains the Object Pool pattern, in Java, using HikariCP. This video is presented by Jayasekhar Konduru. First, a simple definition. An object pool keeps a few expensive objects, lends them out, and takes them back. Think of the trolleys at a supermarket. You borrow one, use it, and return it to the bay for the next shopper. This is the framework version of the Object Pool video. That one built a pool by hand, and found four costs. HikariCP is the database connection pool inside most Java applications. By the end, you will know which of those costs a real library solves, and which it cannot.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Object Pool video. That one found four costs. A small pooled object is slower than creating it. A returned object carries its old state. A leak hangs the application. And choosing the size is a guess. This video is about database connections, the one thing clearly worth pooling. We will not teach the pattern again.

## 3. Before The First Line

Two things are new in this project. First, HikariCP, a database connection pool. You ask it for a connection, use it, and close it. But closing does not really close it. It gives it back to the pool. Second, H2, a database that runs in memory, so nothing needs installing. And one promise. If you skip this video, you lose none of the pattern. This one is about the tool.

## 4. It Opens What Demand Needs

First demo: it opens only what is needed. Ten payments, one after another. The pool is allowed to hold two connections. How many did it open? Just one. The payments ran one at a time, so one was enough. And closing the connection each time did not close it. It returned it to the pool.

## 5. The Dirty Return

Second demo: the dirty return, from the hand-built video. Ada changes two connection settings: auto commit off, and read only on. Then she returns the connection. Grace borrows the very same connection. Auto commit is back on. And read only is back off. The pool reset the settings it knows about, on the way back in. That is the reset the hand-built video had to write by hand.

## 6. What It Cannot Reset

But not everything is reset. Ada sets a variable inside the database session itself, and returns the connection. Grace borrows it, and reads that variable. It says: Ada Lovelace. The security bug from the hand-built video is still possible. The pool can only reset what it can see. And state inside the database session is invisible to it.

## 7. Exhaustion, With A Timeout

Third demo: running out, with a timeout. Two borrowers take both connections, and never return them. A third caller waits. After about three hundred milliseconds, it receives a clear error. Connection is not available, the request timed out. Total two, active two, idle zero. The timeout was already a setting. But its default is thirty seconds, so set it yourself. There is also a leak detection setting, which logs who never returned a connection.

## 8. Sizing Is Still A Guess

Fourth demo: choosing the size is still a guess. Four payments arrive at once, each needing fifty milliseconds. With a pool of one, they queue, and it takes over two hundred milliseconds. With a pool of four, it takes about fifty. A pool of fifty opens fifty connections, and keeps them idle, for just four payments. HikariCP's own documentation recommends small pools. More is not faster.

## 9. What Pooling Buys

Fifth demo: what pooling actually buys. Opening a new database connection each time: about thirty-eight microseconds. Borrowing one from the pool: about one and a half. And this is H2, in memory, where connections are cheap. A real database, across a network, costs far more. That is why this is the one place the pattern is clearly right. The exact timings vary by machine.

## 10. The Verdict

So, here is the verdict. Pool connections, threads, and handles to the operating system. Use a library that has already solved the hard parts. Never pool ordinary objects. And never write your own connection pool. You have just heard how many things there are to get right.

## 11. Where You Have Met This

Where have you met this before? Every Spring Boot application with a database uses HikariCP. Every data source is a pool. And now you know what happens when you close a connection.

## 12. What Was Used

For the record, here are the versions. HikariCP and H2, at the versions listed by Spring Boot four point one point one. But Spring Boot itself is not used here.

## 13. What Is Real Here

A quick, honest note about this demo. Everything here is real. The pool, its error messages, and its statistics. The only stand-in is the database, H2, in memory. The timings vary by machine, and no test depends on them.

## 14. Thanks for Watching

That's the Object Pool, with HikariCP. If you remember one sentence, make it this one. Use a library that has solved the hard parts, and still reset what it cannot see. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Switch on the leak detection setting. And see what it logs. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
