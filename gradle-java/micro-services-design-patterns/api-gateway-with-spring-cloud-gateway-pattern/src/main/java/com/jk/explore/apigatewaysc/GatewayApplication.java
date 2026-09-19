package com.jk.explore.apigatewaysc;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.server.context.WebServerApplicationContext;
import org.springframework.context.ConfigurableApplicationContext;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;

@SpringBootApplication
public class GatewayApplication {

    /** The four internal services, and the gateway in front of them. */
    static final class Shop implements AutoCloseable {
        final Backend catalogue = new Backend("catalogue");
        final Backend pricing = new Backend("pricing");
        final Backend inventory = new Backend("inventory");
        final Backend recommendations = new Backend("recommendations");
        final ConfigurableApplicationContext gateway;
        final HttpClient client = HttpClient.newHttpClient();

        Shop() {
            gateway = new SpringApplicationBuilder(GatewayApplication.class)
                    .web(WebApplicationType.REACTIVE)
                    .properties("backend.catalogue.port=" + catalogue.port(),
                            "backend.pricing.port=" + pricing.port(),
                            "backend.inventory.port=" + inventory.port(),
                            "backend.recommendations.port=" + recommendations.port())
                    .run();
        }

        int gatewayPort() {
            return ((WebServerApplicationContext) gateway).getWebServer().getPort();
        }

        int total() {
            return catalogue.hits() + pricing.hits() + inventory.hits() + recommendations.hits();
        }

        /** Makes one call to the gateway and returns "status body". */
        String get(String path, String token) {
            HttpRequest.Builder request = HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + gatewayPort() + path));
            if (token != null) {
                request.header("Authorization", "Bearer " + token);
            }
            try {
                HttpResponse<String> response = client.send(request.build(), HttpResponse.BodyHandlers.ofString());
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
            gateway.close();
            catalogue.close();
            pricing.close();
            inventory.close();
            recommendations.close();
        }
    }

    public static void main(String[] args) throws Exception {
        try (Shop shop = new Shop()) {
            System.out.println("ONE. One address, four services.");
            for (String service : new String[]{"catalogue", "pricing", "inventory", "recommendations"}) {
                System.out.println("  GET /api/" + service + "/products/MUG-BLUE -> " + shop.get("/api/" + service + "/products/MUG-BLUE", "asha"));
            }
            System.out.println("  the client knows one address, and the gateway's routing table knows the rest.");

            System.out.println("TWO. The prefix is stripped.");
            System.out.println("  the client asked for /api/pricing/products/MUG-BLUE. the pricing service was asked for: " + shop.pricing.lastPath() + ".");
            System.out.println("  the pricing service saw the source header: " + shop.pricing.lastSource() + ".");

            System.out.println("THREE. One token check, for every route.");
            int before = shop.total();
            System.out.println("  no token: " + shop.get("/api/catalogue/products/MUG-BLUE", null));
            System.out.println("  no token, other route: " + shop.get("/api/inventory/stock/MUG-BLUE", null));
            System.out.println("  requests that reached a service: " + (shop.total() - before) + ".");
            System.out.println("  with a token: " + shop.get("/api/catalogue/products/MUG-BLUE", "asha"));

            System.out.println("FOUR. One service down.");
            shop.recommendations.goDown();
            System.out.println("  recommendations: " + statusOf(shop.get("/api/recommendations/for/MUG-BLUE", "asha")));
            System.out.println("  catalogue, still: " + statusOf(shop.get("/api/catalogue/products/MUG-BLUE", "asha")));
            System.out.println("  the failure stayed on its own route. but a refused connection is reported as 500, not 503:");
            System.out.println("  to the client it looks like a bug in the shop. map it in the gateway if the difference matters.");

            System.out.println("FIVE. A gateway forwards. It does not compose.");
            int calls = 0;
            int hitsBefore = shop.total();
            for (String service : new String[]{"catalogue", "pricing", "inventory"}) {
                shop.get("/api/" + service + "/products/MUG-BLUE", "asha");
                calls++;
            }
            System.out.println("  a product page needs three services here, so the client made " + calls + " calls, and " + (shop.total() - hitsBefore) + " reached services.");
            System.out.println("  merging them into one response is a job for composition code, in or behind the gateway.");
        }

        try (Shop shop = new Shop()) {
            System.out.println("SIX. A slow service.");
            Gate stuck = new Gate(1);
            shop.pricing.slowDownAt(stuck);
            System.out.println("  pricing never answers. the gateway answers for it: " + statusOf(shop.get("/api/pricing/products/MUG-BLUE", "asha")) + ".");
            System.out.println("  the wait is a setting, spring.cloud.gateway.server.webflux.httpclient.response-timeout.");
            stuck.open();
        }
    }

    private static String statusOf(String response) {
        return response.substring(0, response.indexOf(' ') < 0 ? response.length() : response.indexOf(' '));
    }
}
