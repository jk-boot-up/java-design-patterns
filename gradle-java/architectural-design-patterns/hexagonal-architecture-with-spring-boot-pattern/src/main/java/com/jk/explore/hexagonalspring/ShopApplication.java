package com.jk.explore.hexagonalspring;

import com.jk.explore.hexagonalspring.adapter.CardNetwork;
import com.jk.explore.hexagonalspring.adapter.driving.ConsoleCheckout;
import com.jk.explore.hexagonalspring.adapter.driving.CsvBatch;
import com.jk.explore.hexagonalspring.adapter.memory.InMemoryOrderStore;
import com.jk.explore.hexagonalspring.adapter.memory.InMemoryWarehouse;
import com.jk.explore.hexagonalspring.core.PlaceOrderService;
import com.jk.explore.hexagonalspring.core.port.OrderStore;
import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import com.jk.explore.hexagonalspring.core.port.Warehouse;
import org.springframework.beans.factory.NoSuchBeanDefinitionException;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.List;

/** The shortcut in {@code naive} is left out of the scan on purpose. */
@SpringBootApplication(scanBasePackages = {
        "com.jk.explore.hexagonalspring.adapter",
        "com.jk.explore.hexagonalspring.config"})
public class ShopApplication {

    static ConfigurableApplicationContext start(String store) {
        return new SpringApplicationBuilder(ShopApplication.class).web(WebApplicationType.NONE)
                .properties("orders.store=" + store).run();
    }

    public static void main(String[] args) {
        System.out.println("ONE. The core is plain Java.");
        try (ConfigurableApplicationContext ctx = start("memory")) {
            PlaceOrder useCase = ctx.getBean(PlaceOrder.class);
            System.out.println("  the use case the container hands out is a " + useCase.getClass().getSimpleName()
                    + ", not a proxy, in package " + useCase.getClass().getPackageName().replace("com.jk.explore.hexagonalspring.", "") + ".");
        }
        var inside = HexagonRules.checkInsideKnowsNoFramework().getFailureReport().getDetails();
        System.out.println("  classes in the core that mention Spring or an adapter: " + inside.stream().filter(d -> !d.contains("naive")).count() + ".");

        System.out.println("TWO. The same use case, two storage adapters.");
        for (String store : new String[]{"memory", "jdbc"}) {
            try (ConfigurableApplicationContext ctx = start(store)) {
                var receipt = ctx.getBean(PlaceOrder.class).place("ada", "ESP-001", 1);
                System.out.println("  orders.store=" + store + ": " + receipt.orderId() + " for " + receipt.totalPence() + " pence,"
                        + " kept by " + ctx.getBean(OrderStore.class).getClass().getSimpleName()
                        + ", stock now " + ctx.getBean(Warehouse.class).stockOf("ESP-001") + ".");
            }
        }

        System.out.println("THREE. Two doors into the same room.");
        try (ConfigurableApplicationContext ctx = start("memory")) {
            System.out.println("  console: " + ctx.getBean(ConsoleCheckout.class).run("ada, ESP-001, 1"));
            System.out.println("  console: " + ctx.getBean(ConsoleCheckout.class).run("ben, ESP-001, 10"));
            System.out.println("  batch of three lines: " + ctx.getBean(CsvBatch.class).run(List.of("cy,BNS-220,2", "di,BNS-220,50", "ed,BNS-220,1")));
            System.out.println("  neither adapter knows how the other works. both call the same port.");
        }

        System.out.println("FOUR. The core without a container.");
        var warehouse = new InMemoryWarehouse(1_000_000);
        var orders = new InMemoryOrderStore();
        var core = new PlaceOrderService(orders, warehouse, pence -> { });
        for (int i = 0; i < 10_000; i++) {
            core.place("load", "BNS-220", 1);
        }
        System.out.println("  10000 orders through the real use case, with adapters made by hand and no Spring context: " + orders.count() + " stored.");
        System.out.println("  the payment port was a one-line lambda. that is what a port is for.");

        System.out.println("FIVE. A use case that reaches for the framework.");
        var leaks = HexagonRules.checkInsideKnowsNoFramework().getFailureReport().getDetails();
        System.out.println("  the rule 'the inside knows no framework', run over every class: " + leaks.size() + " violations.");
        System.out.println("  every one is in SpringyPlaceOrder: " + leaks.stream().allMatch(d -> d.contains("SpringyPlaceOrder")) + ". the real core has none.");

        System.out.println("SIX. A port with no adapter.");
        try (ConfigurableApplicationContext ctx = start("nothing")) {
            System.out.println("  unexpectedly started");
        } catch (Exception e) {
            Throwable root = e;
            while (root.getCause() != null && !(root instanceof NoSuchBeanDefinitionException)) {
                root = root.getCause();
            }
            String missing = root instanceof NoSuchBeanDefinitionException n && n.getBeanType() != null ? n.getBeanType().getSimpleName() : "?";
            System.out.println("  orders.store=nothing: the application does not start. no bean of type " + missing + ".");
            System.out.println("  hand wiring would not have compiled. the container finds out at startup.");
        }
    }
}
