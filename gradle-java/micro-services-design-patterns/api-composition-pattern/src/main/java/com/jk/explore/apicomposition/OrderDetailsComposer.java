package com.jk.explore.apicomposition;

import java.util.ArrayList;
import java.util.List;
import java.util.Map;

/**
 * The pattern: ask all three services at once, then assemble the page yourself.
 *
 * Two decisions make this class what it is, and neither of them is the parallelism.
 *
 * <p>The first is that the calls leave together, so the page costs the slowest of the
 * three rather than the sum. That is arithmetic, and it is the easy half.
 *
 * <p>The second is that every dependency has been classified in advance as one the page
 * cannot live without or one it can. Orders is required: a page with no order on it is
 * not a page, so if Orders is down the shopper gets an error. Catalog and Shipping are
 * not: the page can show a sku code instead of a product name, and can say plainly that
 * the delivery status cannot be checked. That classification is a product decision
 * rather than a technical one, and somebody has to make it before the outage, because
 * the middle of an outage is the worst possible time to be deciding what a page means.
 */
public final class OrderDetailsComposer {

    private final OrderService orders;
    private final CatalogService catalog;
    private final ShippingService shipping;
    private final SimulatedClock clock;
    private final CallLog log;

    public OrderDetailsComposer(OrderService orders, CatalogService catalog,
                                ShippingService shipping, SimulatedClock clock,
                                CallLog log) {
        this.orders = orders;
        this.catalog = catalog;
        this.shipping = shipping;
        this.clock = clock;
        this.log = log;
    }

    /**
     * The order details page.
     *
     * @throws ServiceUnavailableException if Orders cannot be reached, because there is
     *     no honest page to show without it
     */
    public OrderDetailsPage pageFor(String orderId) {
        // Catalog needs to know which skus to name, and only Orders knows that. So this
        // page cannot be one flat fan-out: it is one call, then two in parallel. Being
        // clear about which calls genuinely depend on which is most of the work in
        // composing a page, and it is where an imagined "just parallelise it" comes
        // unstuck.
        Order order = orders.fetch(orderId);

        Fanout fanout = new Fanout(clock, log);
        Fanout.Branch<Map<String, String>> names =
                fanout.add("catalog", () -> catalog.namesFor(order.skus()));
        Fanout.Branch<DeliveryStatus> delivery =
                fanout.add("shipping", () -> shipping.statusFor(orderId));
        fanout.awaitAll();

        List<String> missing = new ArrayList<>();
        if (names.failed()) {
            missing.add("product names");
        }
        if (delivery.failed()) {
            missing.add("delivery status");
        }
        if (!missing.isEmpty()) {
            log.note("Composer", "PARTIAL", "page missing " + String.join(" and ", missing));
        }

        return new OrderDetailsPage(order.orderId(),
                linesOf(order, names.valueOr(Map.of())),
                order.total(),
                delivery.valueOr(DeliveryStatus.unknown()),
                List.copyOf(missing));
    }

    private static List<OrderDetailsPage.PageLine> linesOf(Order order,
                                                           Map<String, String> names) {
        List<OrderDetailsPage.PageLine> lines = new ArrayList<>();
        for (Order.Line line : order.lines()) {
            lines.add(new OrderDetailsPage.PageLine(line.sku(),
                    names.getOrDefault(line.sku(), CatalogService.NAME_UNAVAILABLE),
                    line.quantity(), line.lineTotal()));
        }
        return lines;
    }
}
