package com.jk.explore.layered;

import com.jk.explore.layered.application.PlaceOrderRequest;
import com.jk.explore.layered.application.PlaceOrderRequest.RequestedLine;
import com.jk.explore.layered.application.PlaceOrderService;
import com.jk.explore.layered.infrastructure.AppendOnlyOrderTable;
import com.jk.explore.layered.infrastructure.CardNetwork;
import com.jk.explore.layered.infrastructure.EmailServer;
import com.jk.explore.layered.infrastructure.InMemoryOrderTable;
import com.jk.explore.layered.infrastructure.OrderTable;
import com.jk.explore.layered.infrastructure.ProductTable;
import com.jk.explore.layered.naive.EverythingOrderService;
import com.jk.explore.layered.naive.presentation.OrderHistoryScreen;
import com.jk.explore.layered.presentation.CheckoutScreen;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Five acts, in the order the argument runs.
 *
 * <p>This class is also the <strong>composition root</strong>: the one place
 * that says {@code new} for the classes the layers only know by name. Every
 * layered application has one, usually called {@code main}, and its job is to
 * decide which implementations exist. That is why the forced change further
 * down is one line in this file and nothing anywhere else.
 */
public class PlaceAnOrderDemo {

    /** Ada's order: one machine, one grinder, two bags of beans. £382.50. */
    private static PlaceOrderRequest adasOrder() {
        return PlaceOrderRequest.of("cust-8801",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    public static void main(String[] args) {
        System.out.println("LAYERED ARCHITECTURE — one order, four layers, one rule\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        acceptance();
    }

    /** One class doing everything. It works, and that is the problem. */
    private static void actOne() {
        System.out.println("ONE. No layers at all.");
        EverythingOrderService everything = new EverythingOrderService();
        Map<String, Integer> wanted = new LinkedHashMap<>();
        wanted.put("ESP-001", 1);
        wanted.put("GRD-014", 1);
        wanted.put("BNS-220", 2);
        System.out.println("  " + everything.checkout("cust-8801", "ada@example.com", wanted));
        System.out.println("  it works. 74 lines, and the pricing cannot be tested");
        System.out.println("  without building the catalogue map, the order map and the outbox.");
        System.out.println();
    }

    /** The same feature, arranged. */
    private static void actTwo() {
        System.out.println("TWO. Four layers, and the same order.");
        Shop shop = Shop.with(new InMemoryOrderTable(), CardNetwork.working());
        System.out.println("  " + shop.screen.checkout(adasOrder(), "ada@example.com"));
        System.out.println("  stock now  ESP-001 " + shop.products.stockOf("ESP-001")
                + ", GRD-014 " + shop.products.stockOf("GRD-014")
                + ", BNS-220 " + shop.products.stockOf("BNS-220"));
        System.out.println("  the screen has two imports, both of them the application layer.");
        System.out.println("  it does not know the word 'map'.");
        System.out.println();
    }

    /** The shortcut. Ten minutes instead of an afternoon, and nothing objects. */
    private static void actThree() {
        System.out.println("THREE. The one call that ruins them.");
        InMemoryOrderTable store = new InMemoryOrderTable();
        Shop shop = Shop.with(store, CardNetwork.working());
        shop.screen.checkout(adasOrder(), "ada@example.com");

        OrderHistoryScreen history = new OrderHistoryScreen(store);
        System.out.print("  " + history.history("cust-8801"));
        System.out.println("  that screen skipped the application layer and read storage directly.");
        System.out.println("  it compiles, it is tidy, the tests pass, and it shipped.");
        System.out.println("  NOTHING IN THE BUILD OBJECTED.");
        System.out.println();
    }

    /** Which is why the rule stops being a convention and becomes a test. */
    private static void actFour() {
        System.out.println("FOUR. The rule, written down where a build can read it.");
        System.out.println("  no class in ..presentation.. may depend on ..infrastructure..");
        System.out.println("  that sentence is an ArchUnit test in src/test, it runs in");
        System.out.println("  ./gradlew test, and when it fails it names the class and the");
        System.out.println("  class it reached for. Run the tests and watch it catch");
        System.out.println("  OrderHistoryScreen by name.");
        System.out.println();
    }

    /** And the bill, counted. */
    private static void actFive() {
        System.out.println("FIVE. Replace the entire storage layer.");

        // The forced change, in full: this one line. Everything the layers do
        // is written against the OrderTable interface, so this is the only
        // place that names a particular way of keeping orders.
        OrderTable store = new AppendOnlyOrderTable();

        Shop shop = Shop.with(store, CardNetwork.working());
        System.out.println("  store is now " + store.describe());
        System.out.println("  " + shop.screen.checkout(adasOrder(), "ada@example.com"));
        System.out.println("  orders held: " + store.count());
        System.out.println();
        System.out.println(ForcedChange.report());
        System.out.println();
        System.out.println(ForcedChange.shortcutReport());
        System.out.println();
    }

    /**
     * The five lines every project in this category must print identically.
     * If two projects disagree here, the comparison the category rests on is
     * not valid and one of them is wrong.
     */
    private static void acceptance() {
        Shop shop = Shop.with(new InMemoryOrderTable(), CardNetwork.working());
        String placed = shop.screen.checkout(adasOrder(), "ada@example.com");
        String orderId = placed.split(" ")[1];

        String tooMuch = shop.screen.checkout(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)),
                "ada@example.com");
        String unknown = shop.screen.checkout(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)),
                "ada@example.com");

        Shop declining = Shop.with(new InMemoryOrderTable(), CardNetwork.declining());
        String refused = declining.screen.checkout(adasOrder(), "ada@example.com");

        System.out.println("ACCEPTANCE");
        System.out.println("  order " + orderId + " for cust-8801: PLACED, "
                + shop.orders.find(orderId).orElseThrow().lines().size() + " lines, "
                + shop.orders.find(orderId).orElseThrow().total());
        System.out.println("  stock ESP-001 " + shop.products.stockOf("ESP-001")
                + ", GRD-014 " + shop.products.stockOf("GRD-014")
                + ", BNS-220 " + shop.products.stockOf("BNS-220"));
        System.out.println("  charged cust-8801 " + shop.cards.charges().get(0).amount()
                + " " + (shop.cards.charges().size() == 1 ? "once" : "TWICE"));
        System.out.println("  sent " + shop.email.sent().size() + " confirmation to "
                + shop.email.sent().get(0).to());
        System.out.println("  refused: " + reasonOf(tooMuch) + ", " + reasonOf(unknown)
                + ", " + reasonOf(refused));
    }

    private static String reasonOf(String rendered) {
        if (rendered.startsWith("Sorry — only")) {
            return "not enough stock";
        }
        if (rendered.startsWith("Sorry — no such product")) {
            return "unknown product";
        }
        return "payment declined";
    }

    /**
     * The assembled application. Four layers wired together, which in a project
     * this size is six lines — and in a real one is the only file that grows
     * when an implementation is swapped.
     */
    private record Shop(ProductTable products,
                        OrderTable orders,
                        CardNetwork cards,
                        EmailServer email,
                        CheckoutScreen screen) {

        static Shop with(OrderTable orders, CardNetwork cards) {
            ProductTable products = ProductTable.seeded();
            EmailServer email = new EmailServer();
            PlaceOrderService placeOrder =
                    new PlaceOrderService(products, orders, cards, email);
            return new Shop(products, orders, cards, email, new CheckoutScreen(placeOrder));
        }
    }
}
