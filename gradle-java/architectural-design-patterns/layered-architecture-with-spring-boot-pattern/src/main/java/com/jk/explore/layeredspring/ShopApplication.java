package com.jk.explore.layeredspring;

import com.jk.explore.layeredspring.infrastructure.CardNetwork;
import com.jk.explore.layeredspring.infrastructure.ProductRepository;
import com.jk.explore.layeredspring.naive.ShortcutController;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.server.context.WebServerApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.support.GenericApplicationContext;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

/** The shortcut controller lives in {@code naive} and is left out of the scan on purpose. */
@SpringBootApplication(scanBasePackages = {
        "com.jk.explore.layeredspring.presentation",
        "com.jk.explore.layeredspring.application",
        "com.jk.explore.layeredspring.infrastructure"})
public class ShopApplication {

    /** The running shop, and a client for its real HTTP port. */
    static final class Shop implements AutoCloseable {
        final ConfigurableApplicationContext context;
        final HttpClient client = HttpClient.newHttpClient();

        Shop(boolean withShortcut) {
            SpringApplicationBuilder builder = new SpringApplicationBuilder(ShopApplication.class).web(WebApplicationType.SERVLET);
            if (withShortcut) {
                builder.initializers(c -> ((GenericApplicationContext) c).registerBean(ShortcutController.class));
            }
            context = builder.run();
        }

        int port() {
            return ((WebServerApplicationContext) context).getWebServer().getPort();
        }

        ProductRepository products() {
            return context.getBean(ProductRepository.class);
        }

        CardNetwork cards() {
            return context.getBean(CardNetwork.class);
        }

        String post(String path, String json) {
            return send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port() + path))
                    .header("Content-Type", "application/json").POST(HttpRequest.BodyPublishers.ofString(json)).build());
        }

        String get(String path) {
            return send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port() + path)).GET().build());
        }

        private String send(HttpRequest request) {
            try {
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
                return (response.statusCode() + " " + response.body()).trim();
            } catch (IOException e) {
                throw new IllegalStateException(e);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new IllegalStateException(e);
            }
        }

        @Override
        public void close() {
            context.close();
        }
    }

    static final String ADA_ORDERS_ONE_MACHINE = "{\"customer\":\"ada\",\"sku\":\"ESP-001\",\"quantity\":1}";

    public static void main(String[] args) {
        try (Shop shop = new Shop(true)) {
            System.out.println("ONE. Four layers, one real request.");
            System.out.println("  POST /orders -> " + shop.post("/orders", ADA_ORDERS_ONE_MACHINE));
            System.out.println("  stock of ESP-001 afterwards: " + shop.products().stockOf("ESP-001") + ".");
            System.out.println("  controller, service, repository and record: each is one layer, marked by a Spring stereotype.");

            System.out.println("TWO. One transaction, in the application layer.");
            shop.cards().declineNextCharge();
            System.out.println("  the card is declined after the stock was reserved: " + shop.post("/orders", ADA_ORDERS_ONE_MACHINE));
            System.out.println("  stock of ESP-001 afterwards: " + shop.products().stockOf("ESP-001") + ". the reservation was rolled back.");

            System.out.println("THREE. Failures become statuses in one place.");
            System.out.println("  ten machines when four are left: " + shop.post("/orders", "{\"customer\":\"ada\",\"sku\":\"ESP-001\",\"quantity\":10}"));
            System.out.println("  the domain named the reason. only the presentation layer knows what number it becomes.");

            System.out.println("FOUR. The shortcut compiles, starts and answers.");
            System.out.println("  GET /raw-orders/ORD-000001 -> " + shop.get("/raw-orders/ORD-000001"));
            System.out.println("  a controller that reads the repository directly. Spring did not object.");

            System.out.println("FIVE. It also leaks.");
            System.out.println("  the shortcut's answer contains the shop's cost price: " + shop.get("/raw-orders/ORD-000001").contains("costPence") + ".");
            System.out.println("  the layered answer contains it: " + shop.post("/orders", "{\"customer\":\"bo\",\"sku\":\"BNS-220\",\"quantity\":1}").contains("costPence") + ".");
        }

        System.out.println("SIX. A rule the container does not have.");
        var details = LayerRules.check().getFailureReport().getDetails();
        boolean allInTheShortcut = details.stream().allMatch(d -> d.contains("ShortcutController"));
        System.out.println("  the layering rule, run over every class in the project: " + details.size() + " violations.");
        System.out.println("  every one is in ShortcutController: " + allInTheShortcut + ". the real four layers have none.");
        System.out.println("  Spring wires by type. Only a test can say a layer is not allowed to be there.");
    }
}
