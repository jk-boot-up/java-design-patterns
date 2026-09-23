# Splitter and Aggregator with Camel, Explained

## The pattern in one sentence

A splitter turns one message into several, each carrying the identifier of the thing it came from and its own place in it, and an aggregator holds those pieces until a completion condition says the answer is ready, then sends out one message.

## The analogy, before any of the framework's words

Think of a kitchen. One ticket comes in for a table of three. The head chef tears it into three slips and hands one to the grill, one to the fryer and one to the salad station. Each slip has the table number on it, and says which of the three courses it is. The stations finish in whatever order they finish. The pass gathers the plates by table number and holds them until all three are there, then sends the table's food out together.

Now the useful question. What does the pass do when the fryer never sends anything? It cannot wait for ever, because the other two plates are going cold and the table is waiting. So the pass has a rule: after so long, send out what you have and tell the floor what is missing. That rule — how long, and what counts as ready — is the whole of this project.

## What Camel calls these things

A **route** is the path a message takes, written down: where it starts, what happens to it, where it goes. A **split** is a step that sends out one message for each piece of the message that came in. An **aggregate** is a step that holds messages and sends out one when they are done.

A **correlation expression** is the rule for reading, off each message, the identifier that says which group it belongs to. Here it is the order number.

A **completion condition** is the rule that decides when the aggregate step has waited long enough. Camel offers several and you may set more than one. Two are used here: completion by **size**, which is a count of messages, and completion by **timeout**, which is a deadline in milliseconds. Camel records which one actually fired, and the demo prints Camel's own word for it.

## The six acts

### One Picker, One Order

The basket has three lines, held in Leeds, Reading and Glasgow. One worker walks all three, one after the other: three steps of work on one thread, and the basket comes to £283.42. While that worker walks, the other two warehouses do nothing.

```
  order ORD-4471 has 3 lines, held in 3 warehouses: Leeds, Reading, Glasgow.
  one picker walks all of them, one line after another: 3 steps of work on 1 thread, and the basket comes to £283.42.
  while that picker walks, the other warehouses stand idle.
```

### Camel Splits The Order

The split step sends out one message per line. Camel numbers the pieces itself, from zero, and the demo adds one so a person can read them. Camel also copies the original message's headers onto every piece, so the order number travels with each one without anybody arranging it.

```
  ORD-4471 shipment 1 of 3 to Leeds: 2 x MUG-BLUE, £15.98
  ORD-4471 shipment 2 of 3 to Reading: 1 x ESP-001, £249.99
  ORD-4471 shipment 3 of 3 to Glasgow: 5 x TEA-050, £17.45
  Camel numbered the pieces and copied the order number onto every one of them. that number is what puts them back.
```

### They Come Back In Any Order

The warehouses answer third, first, second. The aggregator does not care. It keys each arrival on the order number and files it under the place it says it is, so the finished answer comes out in the customer's own line order, totalling the same £283.42 the single worker reached. Camel says the reason it finished was `size`: three messages had arrived, and three were expected.

```
  the warehouses answered in the order: 3 1 2.
  the aggregator finished, completed by: size. 3 of 3 shipments: [2 x MUG-BLUE from Leeds, 1 x ESP-001 from Reading, 5 x TEA-050 from Glasgow], total £283.42.
  the pieces arrived jumbled and the answer came out in the customer's line order.
```

### The Completion Condition Decides Everything

Now the Glasgow warehouse is closed. Its message reaches the warehouse step and stops there, and nothing downstream is told. Two shipments come back to an aggregator whose only completion condition is a count of three. Two is not three. No answer comes out, one order sits open, and nothing will ever change that.

This is the part the hand-built project never had to face, because its completion test was written into the method that accepted a piece and could not be left out.

```
  ORD-4472: Glasgow is closed and never answers. shipments back: 2 of 3. answers out of the aggregator: 0. orders still open: 1.
  the only condition on this aggregator is a count, and 2 is not 3. nothing comes out, and nothing ever will.
```

### A Deadline, Which The Simulation Got For Free

The same thing happens to a different aggregator, and this one has a second completion condition: a deadline of six hundred milliseconds, looked at every hundred. Camel runs a background checker that watches every waiting order against the clock. When the deadline passes, the aggregator sends out what it has, on its own, with no prompting from the demo. Camel says the reason was `timeout`, not `size`, and the answer carries two of three shipments, names Glasgow as the one that never answered, and comes to £265.97 — the basket minus the Glasgow line.

The hand-built project had a clock the demo could push forward by thirty minutes in one line. That is a comfortable lie: a real deadline needs something running.

```
  ORD-4473: Glasgow is closed again, but this aggregator also has a deadline of 600 milliseconds, looked at every 100.
  the aggregator gave up on its own. completed by: timeout. 2 of 3 shipments, missing [Glasgow], complete: false, gathered so far £265.97.
  orders still open in that aggregator: 0. the wait ended without anybody asking it to.
```

### The Bill

A thousand orders each short of one shipment means a thousand orders held in the aggregator's memory, and Camel's default store for them is memory, so a restart throws every one of them away. That is why production systems move that store to a database.

Then the surprise. Completion by size counts **messages**, not distinct pieces. Deliver the Reading shipment twice and three messages have arrived, so Camel declares the order finished — with only two of the three lines in it. The duplicate check is yours to write, and the difference it makes is the difference between charging £265.97 and charging £515.96.

And the order number has to be unique, because it is all the aggregator has. Two orders sharing one number are gathered into a single answer.

```
  1000 orders each missing one shipment: 1000 orders held in the aggregator's memory, and a restart loses every one of them.
  a shipment delivered twice: Camel counts messages, not distinct pieces, so ORD-9001 completed by: size at 2 of 3 lines, with 1 duplicate noted.
  the fold has to check for itself: £265.97 with the check, £515.96 without it.
  and the order number has to be unique. two orders sharing one number are gathered into a single answer, because that number is all the aggregator has.
```

## The verdict

Split when the pieces can be worked on separately and the work is slow enough that doing several at once pays. Give every piece the identifier of the thing it came from and its own place in it. Then, on the aggregator, say two things out loud: when it is done, and when it has waited long enough. Never set only the first. And write the duplicate check yourself, because the framework counts messages and you care about pieces.

## How to recognise this in code you did not write

- A Camel route with `.split(...)` in one place and `.aggregate(...)` in another, joined only by an identifier.
- A `completionSize` with no `completionTimeout` beside it, which is a queue of orders that will never come out.
- A completion condition read from a header, so the splitter tells the aggregator how many to expect.
- An aggregation repository configured to a database rather than left in memory.
- Spring Integration's `splitter` and `aggregator`, with `MessageGroupStore` and `group-timeout`.

## Where you have already met this

An order sent to several suppliers and quoted back as one price. A batch file broken into records and reported as one summary. A search query fanned out to several indexes. Any place a single request becomes several and has to become one again.

## When this is too much

If the pieces are quick, or each piece needs the answer to the one before it, splitting costs more than it saves. If nothing can go missing, the hand-built partner project is smaller and clearer. And a framework has to be learned before a route can be trusted.
