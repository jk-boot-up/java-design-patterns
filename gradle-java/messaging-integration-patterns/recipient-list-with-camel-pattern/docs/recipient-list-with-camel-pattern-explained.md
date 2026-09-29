# Recipient List with Apache Camel, Explained

## The pattern in one sentence

With Camel, a recipient list is one `recipientList()` step that asks a
routing table for each message's recipients and sends each a copy.

## The 5 acts

### 1. Every order to every warehouse

First, the old way in Camel: `multicast()` sends a copy of every order to all
four warehouses. Five orders make twenty deliveries, and every warehouse must
sort through orders it has nothing to do with.

### 2. A recipient list

Now `recipientList()` asks the routing table, for each order, which endpoints
should get it. ORD-1, kitchen and furniture, goes to north and big-items.
ORD-3, chilled, goes to cold-store only. The five orders make ten deliveries,
including the extra recipients the rules add.

### 3. Rules add recipients

The same table adds recipients by rule. ORD-4 is worth £650, over the £500
line, so fraud-review gets a copy too. ORD-2 is a gift, so gift-wrap gets one.
Camel needs no change for this: the table simply returns more addresses.

### 4. The table changes while running

North closes for stocktake, and kitchen items are assigned to south instead.
The table is changed while the routes keep running. ORD-5 now reaches south
and cold-store. No route was changed or restarted.

### 5. One recipient fails

The big-items warehouse becomes unreachable. ORD-1 is sent: south gets its
copy, big-items fails, and Camel reports the failure to the sender. Half the
order is out. Camel makes the failure visible; retrying the failed copy, or
undoing the one that went out, is still the shop's job.

## The verdict

Use `recipientList()` when who needs a message depends on its content. Keep
the table in plain code, and decide in advance what happens when one
recipient fails.

## How to recognise this in code you did not write

- `.recipientList(method(...))` or `.recipientList(header("to"))`.
- A method returning comma-separated endpoint addresses.
- Options such as `stopOnException()` and `parallelProcessing()`.

## Where you have already met this

- Camel's `recipientList()` and Spring Integration's recipient list router.
- Email's To and Cc lines, chosen per message.
- Routing rules in order-management systems that split orders across warehouses.
