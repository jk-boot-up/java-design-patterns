package com.jk.explore.cqrs;

import java.util.ArrayList;
import java.util.List;

/**
 * Five acts. The page composed on every view, the page kept ready, the window where the
 * ready page is wrong, why a cache is not the same thing, and the one number you must
 * never read from a read model.
 */
public final class CqrsDemo {

    private static final String CUSTOMER = "cust-7";
    private static final int VIEWS = 3;

    private CqrsDemo() {
    }

    public static void main(String[] args) {
        composingOnEveryView();
        thePageKeptReady();
        theWindowWhereItIsWrong();
        whyACacheIsNotTheSameThing();
        theNumberYouMustNotRead();
    }

    /** Act 1: two services called for every refresh of a page that never changes. */
    private static void composingOnEveryView() {
        System.out.println("Act 1 - composing the page on every view");

        Shop shop = new Shop();
        shop.placeAKettleOrder();
        shop.log.clear();
        int callsBeforeTheViews = shop.orders.callsReceived() + shop.catalog.callsReceived();

        for (int view = 1; view <= VIEWS; view++) {
            shop.composing.historyFor(CUSTOMER);
        }

        int callsForTheViews =
                shop.orders.callsReceived() + shop.catalog.callsReceived() - callsBeforeTheViews;
        System.out.print(shop.log.timeline());
        System.out.println("  " + VIEWS + " views cost " + shop.log.elapsedMillis()
                + "ms and " + callsForTheViews + " service calls");
        System.out.println("  every view rebuilt a page identical to the last one");
        System.out.println();
    }

    /** Act 2: the same page, already assembled, one lookup each. */
    private static void thePageKeptReady() {
        System.out.println("Act 2 - the page kept ready by the events");

        Shop shop = new Shop();
        shop.placeAKettleOrder();
        int callsToBuildIt = shop.catalog.callsReceived();
        shop.log.clear();

        List<OrderHistoryRow> page = List.of();
        for (int view = 1; view <= VIEWS; view++) {
            page = shop.readModel.historyFor(CUSTOMER);
        }

        print(page);
        System.out.print(shop.log.timeline());
        System.out.println("  " + VIEWS + " views cost " + shop.log.elapsedMillis()
                + "ms and 0 service calls");
        System.out.println("  the work did not vanish: Catalog was called "
                + callsToBuildIt + " time when the order was placed");
        System.out.println("  a shop places one order and shows this page a thousand"
                + " times, which is why that trade is worth making");
        System.out.println();
    }

    /** Act 3: the customer's own order, missing from the customer's own page. */
    private static void theWindowWhereItIsWrong() {
        System.out.println("Act 3 - eventually consistent, shown honestly");

        Shop shop = new Shop();
        shop.events.holdEvents();
        Order placed = shop.placeAKettleOrder();

        System.out.println("  " + placed.orderId() + " is placed, paid for, and final");
        System.out.println("  events still in flight: " + shop.events.undelivered());
        System.out.println("  rows on the customer's order history page: "
                + shop.readModel.historyFor(CUSTOMER).size());
        System.out.println("  the customer is looking at a page that does not have"
                + " their order on it");

        shop.events.deliverHeld();
        System.out.println("  events delivered -> rows on the page: "
                + shop.readModel.historyFor(CUSTOMER).size());
        System.out.println("  the window is however long delivery takes, and it closes"
                + " by itself");
        System.out.println();
    }

    /** Act 4: a cache is stale on a timer; a read model is stale until it is told. */
    private static void whyACacheIsNotTheSameThing() {
        System.out.println("Act 4 - the cache that cannot know it is wrong");

        Shop shop = new Shop();
        shop.placeAKettleOrder();
        shop.cached.historyFor(CUSTOMER);

        shop.catalog.rename("SKU-KETTLE", "Brushed Steel Kettle");
        System.out.println("  Catalog renamed the kettle");
        System.out.println("  cache says:      "
                + shop.cached.historyFor(CUSTOMER).get(0).productName());
        System.out.println("  read model says: "
                + shop.readModel.historyFor(CUSTOMER).get(0).productName());
        System.out.println("  the cache will keep saying that for "
                + CachedOrderHistory.EXPIRY_MILLIS / 1000 + " seconds, because nothing"
                + " tells it otherwise");
        System.out.println("  the read model was corrected by the same event that made"
                + " it wrong");
        System.out.println("  cache hits " + shop.cached.hits() + ", misses "
                + shop.cached.misses());
        System.out.println();
    }

    /** Act 5: display the stock number, never sell against it. */
    private static void theNumberYouMustNotRead() {
        System.out.println("Act 5 - the last kettle");

        Shop shop = new Shop();
        shop.stock.stock("SKU-KETTLE", 1);
        shop.events.holdEvents();
        shop.placeAKettleOrder();

        System.out.println("  read model still shows on the shelf: "
                + shop.readModel.stockOnDisplay("SKU-KETTLE"));
        System.out.println("  the ledger actually has: "
                + shop.stock.available("SKU-KETTLE"));
        System.out.println("  a second shopper arrives and the read model says yes");
        try {
            shop.placeAKettleOrder();
            System.out.println("  order placed -- the shop just sold a kettle it"
                    + " does not have");
        } catch (OutOfStockException refused) {
            System.out.println("  the ledger refused: " + refused.getMessage());
        }
        System.out.println("  it was the write side that saved the shop, because the"
                + " sale was decided there");
        System.out.println("  show a read model's stock number. Never sell against it.");

        shop.events.deliverHeld();
        List<ShopEvent> everything = new ArrayList<>(shop.recorded);
        shop.readModel.rebuildFrom(everything);
        System.out.println("  and a read model is throwaway: rebuilt from "
                + everything.size() + " events, "
                + shop.readModel.historyFor(CUSTOMER).size() + " rows back");
        System.out.println();
    }

    private static void print(List<OrderHistoryRow> page) {
        for (OrderHistoryRow row : page) {
            System.out.printf("  %-9s %-12s %-24s x%d  %s%n", row.orderId(), row.sku(),
                    row.productName(), row.quantity(), row.lineTotal());
        }
    }

    /** Both sides of the shop, wired together once. */
    private static final class Shop {

        private final SimulatedClock clock = new SimulatedClock();
        private final CallLog log = new CallLog(clock);
        private final EventBus events = new EventBus(log);
        private final List<ShopEvent> recorded = new ArrayList<>();
        private final StockLedger stock = new StockLedger(events);
        private final CatalogService catalog = new CatalogService(events, clock, log);
        private final OrderWriteService writeSide =
                new OrderWriteService(stock, events, clock, log);
        private final OrdersQueryApi orders = new OrdersQueryApi(writeSide, clock, log);
        private final OrderHistoryReadModel readModel;
        private final ComposingOrderHistory composing;
        private final CachedOrderHistory cached;

        private Shop() {
            readModel = new OrderHistoryReadModel(catalog, clock, log);
            events.subscribe(recorded::add);
            readModel.listenTo(events);
            composing = new ComposingOrderHistory(orders, catalog);
            cached = new CachedOrderHistory(composing, clock, log);

            catalog.add("SKU-KETTLE", "Stainless Steel Kettle");
            catalog.add("SKU-MUG", "Blue Stoneware Mug");
            stock.stock("SKU-KETTLE", 20);
            stock.stock("SKU-MUG", 50);
        }

        private Order placeAKettleOrder() {
            return writeSide.place(CUSTOMER, List.of(
                    new Order.Line("SKU-KETTLE", 1, Money.pence(3499)),
                    new Order.Line("SKU-MUG", 4, Money.pence(899))));
        }
    }
}
