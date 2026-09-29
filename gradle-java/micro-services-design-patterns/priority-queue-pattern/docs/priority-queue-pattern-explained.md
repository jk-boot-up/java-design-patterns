# Priority Queue, Explained

## The pattern in one sentence

A priority queue lets urgent messages overtake routine ones, with a share of
capacity kept so routine work still gets done.

## The 5 acts

### 1. First come, first served

Pickers take ten orders a minute from a first-in-first-out queue. A hundred
standard orders arrive at 9:00 and five same-day orders at 9:01. The same-day
orders wait behind every standard one, and the last is picked at 9:10: the
van left at 9:05.

### 2. A priority queue

The queue now orders by priority: same-day before standard, then oldest
first. All five same-day orders are picked in the 9:01 minute, in time for the
van, and the standard orders carry on straight after.

### 3. A flood of standard orders

A thousand standard orders arrive first. It makes no difference to the
same-day orders: they overtake the whole backlog and are still picked by 9:01.

### 4. Starvation, and a reserved share

In a rush, twelve same-day orders arrive every minute, more than the pickers'
ten. With strict priority, none of the twenty standard orders is picked in
ten minutes. Keeping two picks a minute for the oldest standard orders gets
all twenty done.

### 5. The bill

Marketplace sellers notice that same-day orders jump the queue, and start
marking every order same-day. Now nothing is urgent. Priorities need rules
about who may set them, and more queues and settings to watch.

## The verdict

Use priorities when some work has a genuinely earlier deadline. Order by
priority then age, reserve capacity or age waiting work to prevent
starvation, and control who can mark work urgent.

## How to recognise this in code you did not write

- `PriorityQueue` or `PriorityBlockingQueue` with a comparator.
- Separate queues named `high`, `normal`, `low`.
- Message headers carrying a priority.

## Where you have already met this

- `java.util.PriorityQueue` and `PriorityBlockingQueue`.
- RabbitMQ priority queues and separate SQS queues per priority.
- Hospital triage and airport fast-track lanes.
