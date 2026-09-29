# Space-Based Architecture with Hazelcast Pattern — Video Narration Script

## 1. Space-Based Architecture with Hazelcast

Hello, and welcome. This video explains Space-Based Architecture, built with Hazelcast, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. In a space-based design, the data lives in the memory of the processing units themselves. So busy moments never wait for a database. The database is written later, in the background. Hazelcast is an open-source in-memory data grid: several programs that share data as one. Think of market stalls sharing one stock of goods. Each item is looked after by one stall, with a partner keeping a note in case it closes. The warehouse ledger is updated once an hour. In this video, the domain is an online shop's flash sale of kettles. By the end, you will hear why the database was the bottleneck. How a real grid holds the stock. How it sells the last kettle only once. And what happens when a unit crashes.

## 2. The Scenario

Here is the scenario. A flash sale sends hundreds of kettle orders a second. Every order wrote the stock to the database, one at a time. More app servers only made more of them wait in the same queue.

## 3. Act One — One database for everyone

First demo: one database for everyone. Every order writes the stock to the database, one at a time. Three hundred kettle orders take more than one and a half seconds. More app servers would not help. They would only queue for the same database.

## 4. Act Two — Stock in the grid

Second demo: the stock lives in the grid. Three Hazelcast members start, and form a cluster. The stock is held in their memory. Three hundred orders, spread over the three units, take less than a second. Not one of them waits for the database.

## 5. Act Three — One grid, not three copies

Third demo: one grid, not three copies. Every unit reads the same stock. Seven hundred. Each item has one owner in the grid. With a backup copy on another member. Every unit asks the owner.

## 6. Act Four — Write-behind

Fourth demo: the database catches up, in the background. Hazelcast writes the database a little later. And only the latest value. Three hundred sales become at most three database writes. The database now says seven hundred. No customer waited for any of them.

## 7. Act Five — The last kettle, a crash, and the bill

Fifth demo: the last kettle, and a crash. One kettle is left. Two customers try for it, on two units, at the same moment. The sale runs on the member that owns the kettle, one at a time. One succeeds. The other is refused. Then unit three crashes. Its backup copies take over. Nothing is lost. The bill. Data in every unit's memory. A cluster to run. And if the whole grid stops before the database is written, the latest sales are gone.

## 8. The Pattern, in Hazelcast

Let's name the pattern, in Hazelcast's words. The data lives in the grid's memory. Each item has one owner, and one backup. Changes run on the owner, one at a time. And the database is written behind, in the background.

## 9. Who Does What

Here is who does what. The grid is three Hazelcast members, the processing units. Sell one is the sale, run on the member that owns the item. The stock store writes the database later. And the slow database is the old bottleneck.

## 10. Where You Have Seen It

You have probably met this already. Data grids such as Hazelcast, Apache Ignite, and Oracle Coherence. Ticket booking and trading systems, which keep their busiest data in a grid. And caches that write to a database behind the scenes.

## 11. When To Use It

So, when should you use it? For bursts of load that a single database cannot absorb. Change data with entry processors. Keep at least one backup. And remember that writing behind trades durability for speed.

## 12. Thanks for Watching

That's Space-Based Architecture, with Hazelcast. If you remember one sentence, make it this one. Keep the busy data in a grid, change it where it lives, and write the database behind. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Set the backup count to zero, and crash a unit. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
