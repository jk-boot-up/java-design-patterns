package com.jk.explore.clean;

import com.jk.explore.clean.adapters.controller.BatchOrderController;
import com.jk.explore.clean.adapters.controller.CheckoutController;
import com.jk.explore.clean.adapters.gateway.FileBackedOrderRepository;
import com.jk.explore.clean.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.clean.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.clean.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.clean.naive.usecases.NaivePlaceOrderInteractor;
import com.jk.explore.clean.usecases.OrderRepository;
import com.jk.explore.clean.usecases.PlaceOrderInput;
import com.jk.explore.clean.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.clean.usecases.PlaceOrderInputBoundary;
import com.jk.explore.clean.usecases.PlaceOrderInteractor;
import com.jk.explore.clean.usecases.PlaceOrderOutput;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Five acts, in the order the argument runs. Also the composition root —
 * the one place in the whole project allowed to say {@code new} for a
 * concrete gateway or controller. Wiring the whole graph by hand, in this
 * one method, is this project's central scene: watch {@link #shop()} reach
 * into the outermost circle for concrete classes and hand them to an
 * interactor that only ever names an interface.
 */
public class PlaceAnOrderDemo {

    private static PlaceOrderInput adasOrder() {
        return PlaceOrderInput.of("cust-8801", "ada@example.com",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    public static void main(String[] args) {
        System.out.println("CLEAN ARCHITECTURE — entities, use cases, adapters, the arrow points in\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        acceptance();
    }

    private static void actOne() {
        System.out.println("ONE. The naive version — a use case that imports gateways.");
        NaivePlaceOrderInteractor naive = new NaivePlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working());
        PlaceOrderOutput output = naive.execute(adasOrder());
        System.out.println("  placed " + output.orderId() + " " + output.total());
        System.out.println("  it works. its constructor names three gateway classes,");
        System.out.println("  two circles further out than a use case should reach.");
        System.out.println();
    }

    private static void actTwo() {
        System.out.println("TWO. The real graph, wired by hand.");
        Shop shop = shop();
        CheckoutController checkout = new CheckoutController(shop.interactor);
        String response = checkout.post(jsonBodyFor(adasOrder()));
        System.out.println("  " + response);
        System.out.println("  PlaceOrderInteractor has two imports: entities and");
        System.out.println("  usecases. main() wired four gateways to it by hand --");
        System.out.println("  no container anywhere in this project.");
        System.out.println();
    }

    /** The dependency-inversion moment, shown rather than described. */
    private static void actThree() {
        System.out.println("THREE. The arrow flips. The call does not.");
        System.out.println("  interactor calls: orders.save(order)");
        System.out.println("  orders is typed as: usecases.OrderRepository (an interface)");
        System.out.println("  declared in usecases. implemented in adapters.gateway.");
        System.out.println("  control flows OUT, to whichever gateway was wired in.");
        System.out.println("  the dependency points IN, at an interface usecases owns.");
        System.out.println("  those are two different directions, on purpose.");
        System.out.println();
    }

    private static void actFour() {
        System.out.println("FOUR. Add a delivery mechanism AND a data source, at once.");
        InMemoryProductRepository products = InMemoryProductRepository.seeded();
        OrderRepository fileStore = new FileBackedOrderRepository();
        PlaceOrderInputBoundary secondInteractor = new PlaceOrderInteractor(
                products, fileStore, InMemoryPaymentGateway.working(),
                new InMemoryNotificationGateway());
        BatchOrderController batch = new BatchOrderController(secondInteractor);
        List<String> results = batch.importBatch(
                List.of("cust-9001,ops@example.com,ESP-001:1"));
        System.out.println("  " + results.get(0));
        System.out.println("  store: " + fileStore.describe());
        System.out.println("  PlaceOrderInteractor.java: zero lines changed.");
        System.out.println("  CheckoutController.java: zero lines changed.");
        System.out.println();
    }

    private static void actFive() {
        System.out.println("FIVE. The rule, and the bill.");
        System.out.println("  source code dependencies point only inward.");
        System.out.println("  entities <- usecases <- adapters, and never the other way.");
        System.out.println("  that sentence is an ArchUnit layered-architecture test in");
        System.out.println("  src/test, it runs in ./gradlew test, and when it fails it");
        System.out.println("  names the class. Run the tests and watch it catch");
        System.out.println("  NaivePlaceOrderInteractor by name.");
        System.out.println();
        System.out.println(ForcedChange.report());
        System.out.println();
        System.out.println(ForcedChange.shortcutReport());
        System.out.println();
    }

    private static void acceptance() {
        Shop shop = shop();
        PlaceOrderOutput placed = shop.interactor.execute(adasOrder());
        String orderId = placed.orderId();

        PlaceOrderOutput tooMuch = shop.interactor.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("GRD-014", 3)));
        PlaceOrderOutput unknown = shop.interactor.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("XXX-999", 1)));

        Shop declining = shop(InMemoryPaymentGateway.declining());
        PlaceOrderOutput refused = declining.interactor.execute(adasOrder());

        System.out.println("ACCEPTANCE");
        System.out.println("  order " + orderId + " for cust-8801: PLACED, "
                + shop.orders.find(orderId).orElseThrow().lines().size() + " lines, "
                + shop.orders.find(orderId).orElseThrow().total());
        System.out.println("  stock ESP-001 " + shop.products.stockOf("ESP-001")
                + ", GRD-014 " + shop.products.stockOf("GRD-014")
                + ", BNS-220 " + shop.products.stockOf("BNS-220"));
        System.out.println("  charged cust-8801 " + shop.payments.charges().get(0).amount()
                + " " + (shop.payments.charges().size() == 1 ? "once" : "TWICE"));
        System.out.println("  sent " + shop.notifications.sent().size() + " confirmation to "
                + shop.notifications.sent().get(0).to());
        System.out.println("  refused: " + reasonOf(tooMuch) + ", " + reasonOf(unknown)
                + ", " + reasonOf(refused));
    }

    private static String reasonOf(PlaceOrderOutput output) {
        String reason = output.reason();
        if (reason.startsWith("only")) {
            return "not enough stock";
        }
        if (reason.startsWith("no such product")) {
            return "unknown product";
        }
        return "payment declined";
    }

    private static Map<String, Object> jsonBodyFor(PlaceOrderInput input) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("customerId", input.customerId());
        body.put("email", input.contact());
        List<Map<String, Object>> lines = input.lines().stream()
                .map(line -> {
                    Map<String, Object> m = new LinkedHashMap<>();
                    m.put("sku", line.sku());
                    m.put("quantity", line.quantity());
                    return m;
                })
                .toList();
        body.put("lines", lines);
        return body;
    }

    private static Shop shop() {
        return shop(InMemoryPaymentGateway.working());
    }

    /**
     * The whole object graph, by hand. Twenty-ish lines, reaching into the
     * outermost circle for four concrete gateways and handing them to an
     * interactor that only ever asks for four interfaces. This is the
     * scene a dependency-injection container would make invisible, and the
     * reason this project has no container anywhere in it.
     */
    private static Shop shop(InMemoryPaymentGateway payments) {
        InMemoryProductRepository products = InMemoryProductRepository.seeded();
        InMemoryOrderRepository orders = new InMemoryOrderRepository();
        InMemoryNotificationGateway notifications = new InMemoryNotificationGateway();
        PlaceOrderInteractor interactor =
                new PlaceOrderInteractor(products, orders, payments, notifications);
        return new Shop(products, orders, payments, notifications, interactor);
    }

    private record Shop(InMemoryProductRepository products, InMemoryOrderRepository orders,
                        InMemoryPaymentGateway payments, InMemoryNotificationGateway notifications,
                        PlaceOrderInteractor interactor) {
    }
}
