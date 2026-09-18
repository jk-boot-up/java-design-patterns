package com.jk.explore.hexagonal;

import com.jk.explore.hexagonal.adapter.driving.cli.CliCheckoutAdapter;
import com.jk.explore.hexagonal.adapter.driving.http.HttpCheckoutAdapter;
import com.jk.explore.hexagonal.adapter.notification.InMemoryNotifier;
import com.jk.explore.hexagonal.adapter.payment.InMemoryPaymentGateway;
import com.jk.explore.hexagonal.adapter.persistence.AppendOnlyOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryOrderStore;
import com.jk.explore.hexagonal.adapter.persistence.InMemoryProductCatalog;
import com.jk.explore.hexagonal.core.PlaceOrderRequest;
import com.jk.explore.hexagonal.core.PlaceOrderRequest.RequestedLine;
import com.jk.explore.hexagonal.core.PlaceOrderResult;
import com.jk.explore.hexagonal.core.PlaceOrderService;
import com.jk.explore.hexagonal.core.port.OrderStore;
import com.jk.explore.hexagonal.naive.core.NaivePlaceOrderService;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * Five acts, in the order the argument runs. Also the composition root: the
 * one place allowed to say {@code new} for a concrete adapter.
 */
public class PlaceAnOrderDemo {

    private static PlaceOrderRequest adasOrder() {
        return PlaceOrderRequest.of("cust-8801",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    public static void main(String[] args) {
        System.out.println("HEXAGONAL — one core, ports in, adapters out\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        acceptance();
    }

    /** The naive shape: the core's own use case names three concrete adapters. */
    private static void actOne() {
        System.out.println("ONE. The naive version — the core imports the adapters.");
        NaivePlaceOrderService naive = new NaivePlaceOrderService(
                InMemoryProductCatalog.seeded(), new InMemoryOrderStore(),
                InMemoryPaymentGateway.working());
        PlaceOrderResult result = naive.place(adasOrder());
        System.out.println("  placed " + result.orderId() + " " + result.total());
        System.out.println("  it works. and its constructor names three adapter");
        System.out.println("  classes directly, so testing it means building all three.");
        System.out.println();
    }

    /** The real core, driven by a simulated HTTP request. */
    private static void actTwo() {
        System.out.println("TWO. The real core, driven by HTTP.");
        Shop shop = Shop.fresh();
        HttpCheckoutAdapter http = new HttpCheckoutAdapter(shop.service);
        String response = http.post(jsonBodyFor(adasOrder(), "ada@example.com"));
        System.out.println("  " + response);
        System.out.println("  the core has two imports: core.domain and core.port.");
        System.out.println("  it does not know HTTP, or any adapter, exists.");
        System.out.println();
    }

    /** The driven side swapped: storage changes, the core does not. */
    private static void actThree() {
        System.out.println("THREE. The driven side swapped — storage changes.");
        InMemoryProductCatalog catalog = InMemoryProductCatalog.seeded();
        OrderStore store = new AppendOnlyOrderStore();
        PlaceOrderService service = new PlaceOrderService(
                catalog, store, InMemoryPaymentGateway.working(), new InMemoryNotifier());
        PlaceOrderResult result = service.place(adasOrder(), "ada@example.com");
        System.out.println("  store is now " + store.describe());
        System.out.println("  placed " + result.orderId() + " " + result.total());
        System.out.println("  PlaceOrderService.java: zero lines changed.");
        System.out.println();
    }

    /** The driving side swapped: the same core, now called from a CLI. */
    private static void actFour() {
        System.out.println("FOUR. The driving side swapped — a CLI calls in.");
        Shop shop = Shop.fresh();
        CliCheckoutAdapter cli = new CliCheckoutAdapter(shop.service);
        String out = cli.run("checkout cust-8801 ada@example.com "
                + "ESP-001:1,GRD-014:1,BNS-220:2");
        System.out.println("  $ " + out);
        System.out.println("  the same PlaceOrderService instance shape, called from");
        System.out.println("  a shape as different from HTTP as this project has.");
        System.out.println();
    }

    private static void actFive() {
        System.out.println("FIVE. The rule, and the bill.");
        System.out.println("  no class in ..core.. may depend on ..adapter..");
        System.out.println("  that sentence is an ArchUnit test in src/test, it runs in");
        System.out.println("  ./gradlew test, and when it fails it names the class and the");
        System.out.println("  class it reached for. Run the tests and watch it catch");
        System.out.println("  NaivePlaceOrderService by name.");
        System.out.println();
        System.out.println(ForcedChange.report());
        System.out.println();
        System.out.println(ForcedChange.shortcutReport());
        System.out.println();
    }

    private static void acceptance() {
        Shop shop = Shop.fresh();
        PlaceOrderResult placed = shop.service.place(adasOrder(), "ada@example.com");
        String orderId = placed.orderId();

        PlaceOrderResult tooMuch = shop.service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("GRD-014", 3)),
                "ada@example.com");
        PlaceOrderResult unknown = shop.service.place(
                PlaceOrderRequest.of("cust-8801", new RequestedLine("XXX-999", 1)),
                "ada@example.com");

        Shop declining = Shop.withPayments(InMemoryPaymentGateway.declining());
        PlaceOrderResult refused = declining.service.place(adasOrder(), "ada@example.com");

        System.out.println("ACCEPTANCE");
        System.out.println("  order " + orderId + " for cust-8801: PLACED, "
                + shop.orders.find(orderId).orElseThrow().lines().size() + " lines, "
                + shop.orders.find(orderId).orElseThrow().total());
        System.out.println("  stock ESP-001 " + shop.catalog.stockOf("ESP-001")
                + ", GRD-014 " + shop.catalog.stockOf("GRD-014")
                + ", BNS-220 " + shop.catalog.stockOf("BNS-220"));
        System.out.println("  charged cust-8801 " + shop.payments.charges().get(0).amount()
                + " " + (shop.payments.charges().size() == 1 ? "once" : "TWICE"));
        System.out.println("  sent " + shop.notifier.sent().size() + " confirmation to "
                + shop.notifier.sent().get(0).to());
        System.out.println("  refused: " + reasonOf(tooMuch) + ", " + reasonOf(unknown)
                + ", " + reasonOf(refused));
    }

    private static String reasonOf(PlaceOrderResult result) {
        String reason = result.reason();
        if (reason.startsWith("only")) {
            return "not enough stock";
        }
        if (reason.startsWith("no such product")) {
            return "unknown product";
        }
        return "payment declined";
    }

    private static Map<String, Object> jsonBodyFor(PlaceOrderRequest request, String email) {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("customerId", request.customerId());
        body.put("email", email);
        List<Map<String, Object>> lines = request.lines().stream()
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

    private record Shop(InMemoryProductCatalog catalog, OrderStore orders,
                        InMemoryPaymentGateway payments, InMemoryNotifier notifier,
                        PlaceOrderService service) {

        static Shop fresh() {
            return withPayments(InMemoryPaymentGateway.working());
        }

        static Shop withPayments(InMemoryPaymentGateway payments) {
            InMemoryProductCatalog catalog = InMemoryProductCatalog.seeded();
            OrderStore orders = new InMemoryOrderStore();
            InMemoryNotifier notifier = new InMemoryNotifier();
            PlaceOrderService service = new PlaceOrderService(catalog, orders, payments, notifier);
            return new Shop(catalog, orders, payments, notifier, service);
        }
    }
}
