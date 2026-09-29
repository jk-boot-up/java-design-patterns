# Materialized View, Explained

## The pattern in one sentence

A materialized view is a ready-made copy of data from several services, shaped
for one page and kept up to date from events, so reading it is one fast lookup
that works even when those services are down.

## The 5 acts

### 1. Asking three services

`QueryOnRead` builds the "my orders" page on every visit. It asks the orders
service for the customer's orders, then, for each order, asks shipping whether
it has shipped and the catalogue for the product's name. Three orders make one
plus two times three: seven calls, about 280 milliseconds at 40 each. When the
catalogue is switched off, the whole page fails with "catalogue service
unavailable".

### 2. A ready-made view

`OrderHistoryView` listens to the events the services publish: order placed,
order shipped, product renamed. From seven events it writes three rows, one per
order, with the product's name and the shipping status already filled in.
Opening the page is now one lookup in that table: zero service calls, and it
works while the catalogue is still down. The rows are exactly the same as the
page built by asking.

### 3. A moment behind

Order three ships. The shipping service knows at once, and publishes an event.
Until that event reaches the view, the page still says `placed`. A moment
later, after delivery, it says `shipped`. This delay is called eventual
consistency: the view is not wrong forever, it catches up.

### 4. Rebuild from the events

The view is only a copy, so it can be thrown away. `EventLog` keeps every event
in order. Replaying all eight of them into an empty `OrderHistoryView` builds
exactly the same rows. This is how a view is repaired after a bug, or given a
new column: change the code, and rebuild it from the start.

### 5. The bill

The kettle is renamed "steel kettle". The catalogue changes one name. The view
has copied that name into every order row that bought it, so it rewrites two
rows. All three rows are data the services already hold, stored a second time.
And any page the view serves may be a moment out of date.

## The verdict

Use it for pages that are read far more often than the data changes and that
need data from several services, when a short delay is acceptable. Keep the
events, so the view can always be rebuilt. For answers that must be exactly
current, ask the owning service instead.

## How to recognise this in code you did not write

- A table or index named for a screen: `order_history`, `product_search`, `dashboard_stats`.
- Event handlers that only update a read table.
- A `rebuild` or `replay` job for a read model.
- Documentation that says data on a page "may take a few seconds to update".

## Where you have already met this

- Database materialized views, such as `CREATE MATERIALIZED VIEW` in PostgreSQL.
- The read side of CQRS, where commands and queries use different models.
- Search indexes such as Elasticsearch, filled from events or change data capture.
- Dashboards and reports built from a nightly or streaming copy of the data.
