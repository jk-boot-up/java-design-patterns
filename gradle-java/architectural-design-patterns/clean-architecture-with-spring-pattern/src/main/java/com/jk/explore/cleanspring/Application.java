package com.jk.explore.cleanspring;

import com.jk.explore.cleanspring.adapters.controller.BatchOrderController;
import com.jk.explore.cleanspring.adapters.controller.CheckoutController;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryNotificationGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryOrderRepository;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryPaymentGateway;
import com.jk.explore.cleanspring.adapters.gateway.InMemoryProductRepository;
import com.jk.explore.cleanspring.config.AppConfig;
import com.jk.explore.cleanspring.config.BrokenAppConfig;
import com.jk.explore.cleanspring.naive.usecases.NaivePlaceOrderInteractor;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.cleanspring.usecases.PlaceOrderInputBoundary;
import com.jk.explore.cleanspring.usecases.PlaceOrderInteractor;
import com.jk.explore.cleanspring.usecases.PlaceOrderOutput;

import org.springframework.beans.factory.UnsatisfiedDependencyException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.ComponentScan;
import org.springframework.context.annotation.FilterType;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * §66's five acts again, plus the one scene that is this project's entire
 * reason to exist. {@code BrokenAppConfig} is excluded from this
 * application's own component scan — deliberately, so the real app and the
 * broken demonstration never collide in one context — and is only ever
 * built as its own separate, throwaway context in {@link #actFive()}.
 */
@SpringBootApplication
@ComponentScan(excludeFilters = @ComponentScan.Filter(
        type = FilterType.ASSIGNABLE_TYPE, classes = BrokenAppConfig.class))
public class Application {

    private static PlaceOrderInput adasOrder() {
        return PlaceOrderInput.of("cust-8801", "ada@example.com",
                new RequestedLine("ESP-001", 1),
                new RequestedLine("GRD-014", 1),
                new RequestedLine("BNS-220", 2));
    }

    public static void main(String[] args) {
        System.out.println("CLEAN ARCHITECTURE WITH SPRING — the same graph, wired by a container\n");

        ConfigurableApplicationContext context = SpringApplication.run(Application.class, args);

        actOne();
        actTwo(context);
        actThree(context);
        actFour(context);
        actFive();
        context.close();

        // A fresh context, wired from the same AppConfig, so the acceptance
        // block starts from empty stock and an empty order store rather than
        // whatever acts two to four already did to the shared beans above.
        AnnotationConfigApplicationContext acceptanceContext =
                new AnnotationConfigApplicationContext(AppConfig.class);
        acceptance(acceptanceContext);
        acceptanceContext.close();
    }

    private static void actOne() {
        System.out.println("ONE. The naive version — a use case that imports gateways.");
        NaivePlaceOrderInteractor naive = new NaivePlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.working());
        PlaceOrderOutput output = naive.execute(adasOrder());
        System.out.println("  placed " + output.orderId() + " " + output.total());
        System.out.println("  same shortcut as every other project in this category.");
        System.out.println();
    }

    private static void actTwo(ConfigurableApplicationContext context) {
        System.out.println("TWO. The graph, wired by Spring instead of by hand.");
        CheckoutController checkout = context.getBean(CheckoutController.class);
        String response = checkout.post(jsonBodyFor(adasOrder()));
        System.out.println("  " + response);
        System.out.println("  AppConfig.java has one @Bean method per class");
        System.out.println("  PlaceAnOrderDemo.shop() built by hand. Same graph.");
        System.out.println();
    }

    private static void actThree(ConfigurableApplicationContext context) {
        System.out.println("THREE. Recognition: @Bean is those twenty lines.");
        System.out.println("  startup log (abridged):");
        for (String beanName : new String[]{"productRepository", "orderRepository",
                "paymentGateway", "notificationGateway", "placeOrderInputBoundary",
                "checkoutController", "batchOrderController"}) {
            Object bean = context.getBean(beanName);
            System.out.println("    " + beanName + " -> " + bean.getClass().getSimpleName());
        }
        System.out.println("  seven beans. PlaceAnOrderDemo.shop() wired the same");
        System.out.println("  seven objects, by hand, in the same order.");
        System.out.println();
    }

    private static void actFour(ConfigurableApplicationContext context) {
        System.out.println("FOUR. The forced change still costs nothing extra.");
        BatchOrderController batch = context.getBean(BatchOrderController.class);
        List<String> results = batch.importBatch(List.of("cust-9001,ops@example.com,ESP-001:1"));
        System.out.println("  " + results.get(0));
        System.out.println("  BatchOrderController was already wired -- one more");
        System.out.println("  @Bean method, same as one more line of new(...).");
        System.out.println();
    }

    /** The scene this whole project exists for. */
    private static void actFive() {
        System.out.println("FIVE. Hand-wiring fails at compile time.");
        System.out.println("  Container wiring fails at startup.");
        System.out.println("  removing an argument from PlaceAnOrderDemo's hand-wired");
        System.out.println("  new PlaceOrderInteractor(...) does not compile.");
        System.out.println("  removing @Bean notificationGateway() compiles cleanly --");
        System.out.println("  watch what happens when the container starts instead:");
        try {
            AnnotationConfigApplicationContext broken =
                    new AnnotationConfigApplicationContext(BrokenAppConfig.class);
            broken.close();
            System.out.println("  (did not fail -- this should not happen)");
        } catch (UnsatisfiedDependencyException failure) {
            System.out.println("  STARTUP FAILED: " + rootMessage(failure));
        }
        System.out.println();
    }

    private static String rootMessage(Throwable t) {
        Throwable cause = t;
        while (cause.getCause() != null) {
            cause = cause.getCause();
        }
        String msg = cause.getMessage();
        return msg == null ? cause.getClass().getSimpleName()
                : msg.lines().findFirst().orElse(msg);
    }

    private static void acceptance(ConfigurableApplicationContext context) {
        PlaceOrderInputBoundary placeOrder = context.getBean(PlaceOrderInputBoundary.class);
        InMemoryOrderRepository orders = (InMemoryOrderRepository) context.getBean("orderRepository");
        InMemoryProductRepository products =
                (InMemoryProductRepository) context.getBean("productRepository");
        InMemoryPaymentGateway payments = (InMemoryPaymentGateway) context.getBean("paymentGateway");
        InMemoryNotificationGateway notifications =
                (InMemoryNotificationGateway) context.getBean("notificationGateway");

        PlaceOrderOutput placed = placeOrder.execute(adasOrder());
        String orderId = placed.orderId();

        PlaceOrderOutput tooMuch = placeOrder.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("GRD-014", 3)));
        PlaceOrderOutput unknown = placeOrder.execute(PlaceOrderInput.of(
                "cust-8801", "ada@example.com", new RequestedLine("XXX-999", 1)));

        // A declining card, built directly rather than through a Spring bean:
        // acts two to four already proved the container wires this graph, so
        // the third refusal reuses the plain class rather than a second context.
        PlaceOrderInputBoundary declining = new PlaceOrderInteractor(
                InMemoryProductRepository.seeded(), new InMemoryOrderRepository(),
                InMemoryPaymentGateway.declining(), new InMemoryNotificationGateway());
        PlaceOrderOutput refused = declining.execute(adasOrder());

        System.out.println("ACCEPTANCE");
        System.out.println("  order " + orderId + " for cust-8801: PLACED, "
                + orders.find(orderId).orElseThrow().lines().size() + " lines, "
                + orders.find(orderId).orElseThrow().total());
        System.out.println("  stock ESP-001 " + products.stockOf("ESP-001")
                + ", GRD-014 " + products.stockOf("GRD-014")
                + ", BNS-220 " + products.stockOf("BNS-220"));
        System.out.println("  charged cust-8801 " + payments.charges().get(0).amount()
                + " " + (payments.charges().size() == 1 ? "once" : "TWICE"));
        System.out.println("  sent " + notifications.sent().size() + " confirmation to "
                + notifications.sent().get(0).to());
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
}
