# Sharding with PostgreSQL Pattern — Video Narration Script

## 1. Sharding with PostgreSQL

Hello, and welcome. This video explains the Sharding pattern, with real PostgreSQL databases, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Sharding splits data across several databases, by a key such as the customer number. So no single database has to take all the load. PostgreSQL is an open-source relational database. Here, three of them each hold a share of the shop's orders. Think of a library that splits its members across three branches, by membership number. Asking about one member means phoning one branch. Asking about everyone means phoning all three. In this video, the domain is an online shop's orders on Black Friday. By the end, you will hear how a router splits the orders. Which questions get easier, and which get harder. And what adding a shard costs.

## 2. The Scenario

Here is the scenario. On Black Friday, the shop takes two and a half thousand orders a minute. One database took every read, and every write. It became the limit.

## 3. Act One — One database

First demo: one database for every order. Two and a half thousand orders go into one PostgreSQL database. Every read, and every write, of Black Friday lands on that one server.

## 4. Act Two — Three shards

Second demo: three shards. Three separate PostgreSQL databases. The router picks one for each customer, from the customer number. They hold eight hundred and thirty-three, eight hundred and thirty-four, and eight hundred and thirty-three orders. Customer seventeen lives on shard two. Customer forty-two on shard zero.

## 5. Act Three — One customer, one shard

Third demo: a question about one customer asks one shard. Customer seventeen's orders come from shard two alone. The other two databases are not asked at all.

## 6. Act Four — Everyone, every shard

Fourth demo: a question about everyone asks every shard. How many orders are over five hundred pounds? All three databases are asked, and the application adds up the answers. One thousand, two hundred and fifty. Worse. A welcome coupon may only be used once. Each database enforces that. But customer seventeen and customer forty-two live on different shards. Both use it. Each database only knows its own rows.

## 7. Act Five — The bill: resharding

Fifth demo: the bill. A fourth shard is added. With the simple rule, customer number modulo four, one thousand eight hundred and seventy-four customers must move to another database. With consistent hashing, only six hundred and thirty. And no transaction covers two shards. One very busy customer still overloads their own shard.

## 8. The Pattern

Let's name the pattern. Several databases, each holding a share. A key, here the customer number, decides where each row lives. And a router sends each query to the right database.

## 9. Who Does What

Here is who does what. The shard router picks the database for each customer, and sends each query there. The shards are three PostgreSQL databases, in containers. And the application itself merges answers from several shards.

## 10. Where You Have Seen It

You have probably met this already. Citus, and Vitess, add sharding to PostgreSQL and MySQL. MongoDB and Cassandra shard by a key, built in. And cache clients use consistent hashing to pick a server.

## 11. When To Use It

So, when should you use it? When writes outgrow the largest single database you can run. Choose a key most queries share. Route with consistent hashing. And keep rules that span customers somewhere every shard can see.

## 12. Thanks for Watching

That's Sharding, with PostgreSQL. If you remember one sentence, make it this one. Split the data by a key, and remember that each database only knows its own share. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It needs Docker running, and starts the databases for you. Here is one exercise to try. Make the one-use coupon hold across all shards. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
