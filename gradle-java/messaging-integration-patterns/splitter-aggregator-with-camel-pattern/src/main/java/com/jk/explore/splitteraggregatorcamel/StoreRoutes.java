package com.jk.explore.splitteraggregatorcamel;

import java.util.List;
import org.apache.camel.Exchange;
import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.processor.aggregate.MemoryAggregationRepository;

/**
 * Every route the store uses, written out once.
 *
 * <p>A route is a declared path a message travels: where it starts, the steps it passes through, and where
 * it ends. The splitter is one step on such a path; the aggregator is a step on another. The two are not
 * connected in code, only by the order number each shipment carries, which is what makes it possible for a
 * shipment to go missing at all.
 */
public class StoreRoutes extends RouteBuilder {

    /** How long the aggregator waits for a silent warehouse before it gives up, in milliseconds. */
    public static final long TIMEOUT_MILLIS = 600;

    /** How often the aggregator looks at the clock, in milliseconds. */
    public static final long CHECK_MILLIS = 100;

    private final ShipmentAggregationStrategy fold = new ShipmentAggregationStrategy();
    private final MemoryAggregationRepository holding = new MemoryAggregationRepository();
    private final MemoryAggregationRepository holdingWithTimeout = new MemoryAggregationRepository();
    private final MemoryAggregationRepository holdingBill = new MemoryAggregationRepository();

    private final OnePicker onePicker;
    private final Warehouse warehouse;
    private final List<Shipment> collected;
    private final Results results;

    public StoreRoutes(OnePicker onePicker, Warehouse warehouse, List<Shipment> collected, Results results) {
        this.onePicker = onePicker;
        this.warehouse = warehouse;
        this.collected = collected;
        this.results = results;
    }

    @Override
    public void configure() {
        // The before picture: no split at all. One worker, the whole order, one line after another.
        from("direct:one-picker")
                .process(onePicker);

        // The splitter. One order in, one message per line out. Camel numbers the pieces itself and copies
        // the order's headers onto every one of them, which is how each piece knows what it belongs to.
        from("direct:checkout")
                .process(exchange -> {
                    Order order = exchange.getIn().getBody(Order.class);
                    exchange.getIn().setHeader("orderId", order.id());
                    exchange.getIn().setHeader("shipmentCount", order.lines().size());
                    exchange.getIn().setBody(order.lines());
                })
                .split(body())
                    .process(exchange -> exchange.getIn().setHeader("shipmentIndex",
                            exchange.getProperty(Exchange.SPLIT_INDEX, Integer.class) + 1))
                    .to("direct:pick")
                .end();

        // A warehouse picks and prices its piece, then sends it on. A warehouse named as closed simply never
        // answers: the message stops here, and nothing downstream is told about it.
        from("direct:pick")
                .process(warehouse)
                .filter(exchange -> !exchange.getIn().getHeader("warehouse", "", String.class)
                        .equals(exchange.getIn().getHeader("closedWarehouse", "", String.class)))
                    .toD("${header.gatherTo}")
                .end();

        // A siding used by one act, so that the shipments can be handed to the aggregator out of order.
        from("direct:collect")
                .process(exchange -> collected.add(exchange.getIn().getBody(Shipment.class)));

        // The aggregator, with one completion condition: it finishes when as many messages have arrived as
        // the order said there would be. With nothing else set, an order short of a shipment waits for ever.
        from("direct:gather")
                .aggregate(header("orderId"), fold)
                    .completionSize(header("shipmentCount"))
                    .aggregationRepository(holding)
                .process(this::publish);

        // The same aggregator with a second completion condition: a deadline. Whichever condition is met
        // first ends the wait, and Camel records which one it was.
        from("direct:gather-with-timeout")
                .aggregate(header("orderId"), fold)
                    .completionSize(header("shipmentCount"))
                    .completionTimeout(TIMEOUT_MILLIS)
                    .completionTimeoutCheckerInterval(CHECK_MILLIS)
                    .aggregationRepository(holdingWithTimeout)
                .process(this::publish);

        // A third aggregator kept apart so the last act can count what it is holding without the earlier
        // acts' leftovers in the total.
        from("direct:gather-bill")
                .aggregate(header("orderId"), fold)
                    .completionSize(header("shipmentCount"))
                    .aggregationRepository(holdingBill)
                .process(this::publish);
    }

    private void publish(Exchange exchange) {
        results.add(new Gathered(exchange.getIn().getBody(Gathering.class),
                exchange.getProperty(Exchange.AGGREGATED_COMPLETED_BY, "", String.class)));
    }

    /** How many orders this aggregator is still holding, unfinished. */
    public int ordersOpen() {
        return holding.getKeys().size();
    }

    public int ordersOpenWithTimeout() {
        return holdingWithTimeout.getKeys().size();
    }

    public int ordersOpenInTheBill() {
        return holdingBill.getKeys().size();
    }
}
