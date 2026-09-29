# Sharding Pattern — Video Narration Script

## 1. Sharding

Hello, and welcome. This video explains the Sharding pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Sharding splits one large set of data across several databases, called shards. Each row goes to a shard chosen from a key, such as the customer number. So each database holds, and serves, only its share. Think of a doctor's surgery that has outgrown one filing cabinet. The records are split into three cabinets: A to H, I to P, and Q to Z. One patient's file is in one cabinet. But a fourth cabinet means refiling many folders. In this video, the domain is an online shop, on Black Friday. Orders arrive faster than one database can take them. By the end, you will hear how shards share the load. Which questions are easy, and which are not. And what adding a shard costs.

## 2. The Scenario

Here is the scenario. Every order is saved in one database. It can take a thousand new orders a minute. On Black Friday, two and a half thousand arrive every minute.

## 3. Act One — One database

First demo: one database for every order. It can take one thousand new orders a minute. On Black Friday, two and a half thousand arrive, every minute. Fifteen hundred are left waiting, every minute. And the queue keeps growing.

## 4. Act Two — Three shards

Second demo: three shards, split by customer number. Each order goes to one of three databases. Which one is worked out from the customer's number alone. The two and a half thousand orders split into three shares of about eight hundred and thirty. Each is within its database's limit. Customer seventeen always lives on shard two.

## 5. Act Three — One customer, one shard

Third demo: a question about one customer asks one shard. Where are customer seventeen's orders? The router knows: shard two. Only one shard is asked.

## 6. Act Four — Everyone, every shard

Fourth demo: a question about everyone asks every shard. Which orders this minute were over five hundred pounds? There is no single place to look. All three shards are asked, and their answers are merged. Twenty-five orders.

## 7. Act Five — The bill

Fifth demo: the bill. The shop grows, and adds a fourth shard. With the same simple rule, now the customer number modulo four, one thousand eight hundred and seventy-four of the two and a half thousand customers belong on a different shard. All their orders must be copied across. And one very busy customer still lands entirely on one shard.

## 8. The Pattern

Let's name the pattern. Use several databases, called shards. A shard key, here the customer number, decides which shard each order goes to. A question about one customer asks one shard. A question about everyone asks every shard, and merges the answers.

## 9. Who Does What

Here is who does what. Sharded orders is the router. It works out the shard from the customer number, and asks the right database. An order database is one shard, with its own limit. And an order carries the customer number, its shard key.

## 10. Where You Have Seen It

You have probably met this pattern already. MongoDB and Elasticsearch split data into shards. Cassandra and DynamoDB split it into partitions, by a partition key. Vitess and Citus shard MySQL and Postgres. And consistent hashing is the trick that moves less data when shards are added.

## 11. When To Use It

So, when should you use it? Only when one database truly cannot cope, after a bigger server, caching, and read copies. Choose a key that spreads the load evenly, and matches your most common questions. And plan, from day one, for adding shards.

## 12. Thanks for Watching

That's the Sharding pattern. If you remember one sentence, make it this one. Split the data by a key, and each database carries only its share. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Add a fourth shard using a lookup table, so only new customers go there. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
