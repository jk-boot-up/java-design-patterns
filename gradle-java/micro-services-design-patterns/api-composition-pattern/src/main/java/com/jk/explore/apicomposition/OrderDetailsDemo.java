package com.jk.explore.apicomposition;

/**
 * Five acts. Three calls in a queue, the same three sent together, one service down
 * under each composer, and the arithmetic nobody does until it is too late.
 */
public final class OrderDetailsDemo {

    private static final String ORDER_ID = "ord-3001";

    private OrderDetailsDemo() {
    }

    public static void main(String[] args) {
        threeCallsInAQueue();
        theSameThreeCallsTogether();
        shippingGoesDown();
        ordersGoesDown();
        theArithmetic();
    }

    /** Act 1: the obvious version. Each call waits for the one before it. */
    private static void threeCallsInAQueue() {
        System.out.println("Act 1 - three calls, one after another");

        Shop shop = new Shop();
        OrderDetailsPage page = new SequentialOrderDetailsComposer(
                shop.orders, shop.catalog, shop.shipping).pageFor(ORDER_ID);

        print(page);
        System.out.print(shop.log.timeline());
        System.out.println("  the shopper waited " + shop.log.elapsedMillis()
                + "ms: 30 + 60 + 120, added up");
        System.out.println();
    }

    /** Act 2: the same three answers, with the two independent calls sent together. */
    private static void theSameThreeCallsTogether() {
        System.out.println("Act 2 - Orders first, then Catalog and Shipping together");

        Shop shop = new Shop();
        OrderDetailsPage page = shop.composer.pageFor(ORDER_ID);

        print(page);
        System.out.print(shop.log.timeline());
        System.out.println("  the shopper waited " + shop.log.elapsedMillis()
                + "ms: 30, then the slower of 60 and 120");
        System.out.println("  Catalog cannot go first -- only Orders knows which skus"
                + " to ask about");
        System.out.println();
    }

    /** Act 3: the slowest service falls over. One composer copes; one does not. */
    private static void shippingGoesDown() {
        System.out.println("Act 3 - Shipping is down");

        Shop sequential = new Shop();
        sequential.shipping.goDown(1);
        try {
            new SequentialOrderDetailsComposer(sequential.orders, sequential.catalog,
                    sequential.shipping).pageFor(ORDER_ID);
            System.out.println("  sequential: page shown");
        } catch (ServiceUnavailableException failed) {
            System.out.println("  sequential: " + failed.getMessage()
                    + " -- no page at all");
            System.out.println("             the order and the product names had"
                    + " already arrived. Both thrown away.");
        }

        Shop composed = new Shop();
        composed.shipping.goDown(1);
        OrderDetailsPage page = composed.composer.pageFor(ORDER_ID);
        System.out.println("  composed:");
        print(page);
        System.out.println("  missing: " + page.missingSections());
        System.out.println("  the shopper can still see what they bought and what it"
                + " cost. The page says what it does not know.");
        System.out.println();
    }

    /** Act 4: the service the page genuinely cannot do without. */
    private static void ordersGoesDown() {
        System.out.println("Act 4 - Orders is down");

        Shop shop = new Shop();
        shop.orders.goDown(1);
        try {
            shop.composer.pageFor(ORDER_ID);
            System.out.println("  composed: page shown");
        } catch (ServiceUnavailableException failed) {
            System.out.println("  composed: " + failed.getMessage()
                    + " -- and that is correct");
        }
        System.out.println("  a page with no order on it is not a partial page,"
                + " it is a blank one");
        System.out.println("  Catalog was never called: " + shop.catalog.callsReceived()
                + " calls");
        System.out.println();
    }

    /** Act 5: the number that decides whether composition is enough. */
    private static void theArithmetic() {
        System.out.println("Act 5 - what three dependencies do to availability");

        double perService = 0.999;
        double all = Availability.whenAllAreRequired(perService, perService, perService);
        System.out.println("  each service up " + Availability.asPercent(perService)
                + " of the time -> " + Availability.downtimeMinutesPerMonth(perService)
                + " min down a month");
        System.out.println("  a page needing all three: " + Availability.asPercent(all)
                + " -> " + Availability.downtimeMinutesPerMonth(all)
                + " min down a month");
        System.out.println("  availabilities multiply. Three good services make a"
                + " worse page than any of them.");

        double one = Availability.whenOnlyOneIsRequired(perService);
        System.out.println("  with only Orders required: " + Availability.asPercent(one)
                + " -> " + Availability.downtimeMinutesPerMonth(one)
                + " min down a month");
        System.out.println("  that is what deciding in advance what is optional"
                + " actually buys.");

        Shop slow = new Shop(400);
        slow.composer.pageFor(ORDER_ID);
        System.out.println("  and the page is only ever as fast as its slowest"
                + " dependency: Shipping at 400ms makes the page "
                + slow.log.elapsedMillis() + "ms");
        System.out.println("  when neither number can be lived with, the answer is"
                + " CQRS: keep a copy already assembled.");
        System.out.println();
    }

    private static void print(OrderDetailsPage page) {
        System.out.println("  " + page.orderId() + "  total " + page.total());
        for (OrderDetailsPage.PageLine line : page.lines()) {
            System.out.printf("    %-12s %-24s x%d  %s%n", line.sku(), line.productName(),
                    line.quantity(), line.lineTotal());
        }
        System.out.println("    delivery: " + page.delivery().carrier() + ", "
                + page.delivery().state());
    }

    /** The three services and a composer, wired up so each act starts clean. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final OrderService orders = new OrderService(clock, log);
        private final CatalogService catalog = new CatalogService(clock, log);
        private final ShippingService shipping;
        private final OrderDetailsComposer composer;

        private Shop() {
            this(ShippingService.LATENCY_MILLIS);
        }

        private Shop(long shippingLatencyMillis) {
            shipping = new ShippingService(clock, log, shippingLatencyMillis);
            composer = new OrderDetailsComposer(orders, catalog, shipping, clock, log);
        }
    }
}
