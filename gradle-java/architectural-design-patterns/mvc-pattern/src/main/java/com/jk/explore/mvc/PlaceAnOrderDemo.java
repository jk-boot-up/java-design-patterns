package com.jk.explore.mvc;

import com.jk.explore.mvc.application.PlaceOrderRequest;
import com.jk.explore.mvc.application.PlaceOrderRequest.RequestedLine;
import com.jk.explore.mvc.application.PlaceOrderService;
import com.jk.explore.mvc.controller.OrderSummaryController;
import com.jk.explore.mvc.controller.OrderSummaryController.CheckoutOutcome;
import com.jk.explore.mvc.infrastructure.CardNetwork;
import com.jk.explore.mvc.infrastructure.EmailServer;
import com.jk.explore.mvc.infrastructure.InMemoryOrderTable;
import com.jk.explore.mvc.infrastructure.OrderTable;
import com.jk.explore.mvc.infrastructure.ProductTable;
import com.jk.explore.mvc.naive.EverythingOrderScreen;
import com.jk.explore.mvc.naive.view.RoundedEmailView;
import com.jk.explore.mvc.view.EmailConfirmationView;
import com.jk.explore.mvc.view.ScreenSummaryView;

import java.util.LinkedHashMap;
import java.util.Map;

/**
 * Five acts, in the order the argument runs. Also the composition root: the
 * one place that says {@code new} for a concrete view, which is why the
 * forced change further down is two lines in this file and nothing else.
 */
public class PlaceAnOrderDemo {

    private static PlaceOrderRequest adasOrder() {
        return PlaceOrderRequest.of("cust-8801",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    public static void main(String[] args) {
        System.out.println("MVC — one order, two views, one model that decides the total\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        acceptance();
    }

    private static void actOne() {
        System.out.println("ONE. No model, no view, no controller.");
        EverythingOrderScreen screen = new EverythingOrderScreen();
        Map<String, Integer> wanted = new LinkedHashMap<>();
        wanted.put("ESP-001", 1);
        wanted.put("GRD-014", 1);
        wanted.put("BNS-220", 2);
        System.out.println(screen.checkout(wanted));
        System.out.println("  it works. the screen text and the checkout are");
        System.out.println("  one method — you cannot test one without the other.");
        System.out.println();
    }

    private static void actTwo() {
        System.out.println("TWO. A model, a controller, and one view.");
        Shop shop = Shop.fresh();
        CheckoutOutcome outcome = shop.controller.checkout(
                adasOrder(), "ada@example.com", new ScreenSummaryView(), null);
        System.out.println(outcome.screenText());
        System.out.println("  the screen has one import: OrderSummaryModel.");
        System.out.println("  it does not know how a total is worked out.");
        System.out.println();
    }

    private static void actThree() {
        System.out.println("THREE. A second view, the shortcut way.");
        Shop shop = Shop.fresh();
        RoundedEmailView roundedEmail = new RoundedEmailView(shop.products);
        CheckoutOutcome outcome = shop.controller.checkout(
                adasOrder(), "ada@example.com", new ScreenSummaryView(), roundedEmail);
        System.out.println(outcome.screenText());
        System.out.println("  " + roundedEmail.render(outcome.model()));
        System.out.println("  the screen says £382.50. the email says £383.00.");
        System.out.println("  NOTHING IN THE BUILD OBJECTED.");
        System.out.println();
    }

    private static void actFour() {
        System.out.println("FOUR. The rule, written down where a build can read it.");
        System.out.println("  no class in ..view.. may depend on ..infrastructure..");
        System.out.println("  that sentence is an ArchUnit test in src/test, it runs in");
        System.out.println("  ./gradlew test, and when it fails it names the class and the");
        System.out.println("  class it reached for. Run the tests and watch it catch");
        System.out.println("  RoundedEmailView by name.");
        System.out.println();
    }

    private static void actFive() {
        System.out.println("FIVE. Add the real second view.");
        Shop shop = Shop.fresh();
        CheckoutOutcome outcome = shop.controller.checkout(
                adasOrder(), "ada@example.com",
                new ScreenSummaryView(), new EmailConfirmationView());
        System.out.println(outcome.screenText());
        System.out.println("  " + shop.email.sent().get(0).body());
        System.out.println("  both views: £382.50. every time, because neither");
        System.out.println("  one is allowed to add up a price.");
        System.out.println();
        System.out.println(ForcedChange.report());
        System.out.println();
        System.out.println(ForcedChange.shortcutReport());
        System.out.println();
    }

    /**
     * The five lines every project in this category must print identically.
     */
    private static void acceptance() {
        Shop shop = Shop.fresh();
        CheckoutOutcome placed = shop.controller.checkout(
                adasOrder(), "ada@example.com",
                new ScreenSummaryView(), new EmailConfirmationView());
        String orderId = placed.model().orderId();

        CheckoutOutcome tooMuch = shop.controller.checkout(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)),
                "ada@example.com", new ScreenSummaryView(), null);
        CheckoutOutcome unknown = shop.controller.checkout(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)),
                "ada@example.com", new ScreenSummaryView(), null);

        Shop declining = Shop.withCards(CardNetwork.declining());
        CheckoutOutcome refused = declining.controller.checkout(
                adasOrder(), "ada@example.com", new ScreenSummaryView(), null);

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

    private static String reasonOf(CheckoutOutcome outcome) {
        String reason = outcome.reason();
        if (reason.startsWith("only")) {
            return "not enough stock";
        }
        if (reason.startsWith("no such product")) {
            return "unknown product";
        }
        return "payment declined";
    }

    /** The assembled application: model layer, controller, and one screen view, wired once. */
    private record Shop(ProductTable products, OrderTable orders, CardNetwork cards,
                        EmailServer email, OrderSummaryController controller) {

        static Shop fresh() {
            return withCards(CardNetwork.working());
        }

        static Shop withCards(CardNetwork cards) {
            ProductTable products = ProductTable.seeded();
            OrderTable orders = new InMemoryOrderTable();
            EmailServer email = new EmailServer();
            PlaceOrderService placeOrder = new PlaceOrderService(products, orders, cards);
            OrderSummaryController controller =
                    new OrderSummaryController(placeOrder, orders, email);
            return new Shop(products, orders, cards, email, controller);
        }
    }
}
