# Priority Queue with RabbitMQ, Explained

## The pattern in one sentence

With RabbitMQ, a queue declared with `x-max-priority` hands out higher-priority
messages first, but only among those still waiting on the queue.

## The 5 acts

### 1. First in, first out

An ordinary RabbitMQ queue hands out orders in the order they arrived. A
hundred standard orders came first, then five same-day orders. Picking ten a
minute from nine o'clock, the last same-day order is picked at 9:11. The van
left at 9:05.

### 2. A priority queue

Now the queue is declared with `x-max-priority` set to ten, and same-day
orders are sent with priority nine, standard ones with priority one. RabbitMQ
hands out the highest priority first. All five same-day orders are picked in
the first minute, by 9:01.

### 3. A flood

A thousand standard orders are queued first. It makes no difference: the
five same-day orders overtake them all and are still picked by 9:01.

### 4. Only what is still waiting

A picker's handheld subscribes with no prefetch limit, and RabbitMQ pushes all
a hundred standard orders to it at once. When the same-day orders arrive, they
join the back of the handheld, at positions 101 to 105: priority only
reorders what is still waiting on the queue. With a prefetch of one, only one
order sits in the handheld, and the next one the queue hands out is SAME-1.

### 5. The bill: starvation

In a rush, twelve same-day orders arrive every minute, more than the ten
picks. With strict priority, none of the twenty standard orders is picked in
ten minutes. RabbitMQ has no reserved share, so the shop builds one: standard
orders on their own queue, with two picks a minute kept for it. All twenty
are picked.

## The verdict

Use a RabbitMQ priority queue for work with genuinely earlier deadlines. Keep
consumer prefetch small, use few priority levels, and build a reserved share
for routine work yourself.

## How to recognise this in code you did not write

- `queueDeclare(..., Map.of("x-max-priority", n))`.
- `BasicProperties.Builder().priority(p)`.
- Separate high and low queues with weighted consumers.

## Where you have already met this

- RabbitMQ `x-max-priority` queues and message priority.
- Separate high and low priority queues in Amazon SQS.
- Hospital triage and airport fast-track lanes.
