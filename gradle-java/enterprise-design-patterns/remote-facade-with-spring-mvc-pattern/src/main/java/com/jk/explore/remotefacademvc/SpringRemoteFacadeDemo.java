package com.jk.explore.remotefacademvc;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * The five acts: a real Spring MVC service on a local port, called over HTTP by the "phone app".
 */
public final class SpringRemoteFacadeDemo {

    static final HttpClient HTTP = HttpClient.newHttpClient();

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (ConfigurableApplicationContext ctx = new SpringApplicationBuilder(ShopApp.class)
                .properties("server.port=0", "spring.main.banner-mode=off", "logging.level.root=OFF").run()) {
            String base = "http://127.0.0.1:" + ctx.getEnvironment().getProperty("local.server.port");
            OrderStore store = ctx.getBean(OrderStore.class);

            out.add("ONE. The phone app asks for each fact separately.");
            long start = System.nanoTime();
            for (String part : List.of("customer", "items", "total", "address", "slot")) {
                out.add("  GET /order/" + part + " -> " + get(base + "/order/" + part).body());
            }
            long millis = (System.nanoTime() - start) / 1_000_000;
            out.add("  order screen: 5 round trips, " + (millis >= 400 ? "over 0.4 s" : "under 0.4 s") + " on a mobile network");

            out.add("");
            out.add("TWO. A remote facade: the whole screen in one call, as JSON.");
            start = System.nanoTime();
            HttpResponse<String> summary = get(base + "/order-summary");
            millis = (System.nanoTime() - start) / 1_000_000;
            out.add("  GET /order-summary -> " + summary.body());
            out.add("  order screen: 1 round trip, " + (millis < 200 ? "under 0.2 s" : "over 0.2 s"));

            out.add("");
            out.add("THREE. A change in one call: all or nothing.");
            put(base + "/order/address", "text/plain", "12 High Street, York");
            HttpResponse<String> slot = put(base + "/order/slot", "text/plain", "Sun 9-12");
            out.add("  small calls: address changed, then slot -> " + slot.statusCode());
            out.add("  the order now: " + store.order().address() + ", " + store.order().slot() + " (new address, old slot)");
            store.reset();
            HttpResponse<String> refused = put(base + "/order-delivery", "application/json",
                    "{\"address\":\"12 High Street, York\",\"slot\":\"Sun 9-12\"}");
            out.add("  facade -> " + refused.statusCode() + " " + field(refused.body(), "detail") + "; the order: "
                    + store.order().address() + ", " + store.order().slot());
            HttpResponse<String> ok = put(base + "/order-delivery", "application/json",
                    "{\"address\":\"12 High Street, York\",\"slot\":\"Tue 9-12\"}");
            out.add("  facade, a valid slot -> " + ok.statusCode() + " " + ok.body() + "; the order: "
                    + store.order().address() + ", " + store.order().slot());

            out.add("");
            out.add("FOUR. Inside, the order stays fine-grained.");
            out.add("  the facade calls Order's small methods in-process; the rule about valid slots lives on Order");
            out.add("  the refusal came back as a standard problem report: " + refused.headers().firstValue("Content-Type").orElse(""));

            out.add("");
            out.add("FIVE. The bill: sometimes too much, and one more layer.");
            int small = get(base + "/order/slot").body().length();
            int whole = get(base + "/order-summary").body().length();
            out.add("  a widget that shows only the slot: " + small + " bytes with the small call, " + whole + " with the summary");
            out.add("  and each new screen may want its own facade method");
        }
        return out;
    }

    static HttpResponse<String> get(String url) throws Exception {
        return HTTP.send(HttpRequest.newBuilder(URI.create(url)).GET().build(), HttpResponse.BodyHandlers.ofString());
    }

    static HttpResponse<String> put(String url, String type, String body) throws Exception {
        return HTTP.send(HttpRequest.newBuilder(URI.create(url)).header("Content-Type", type)
                .PUT(HttpRequest.BodyPublishers.ofString(body)).build(), HttpResponse.BodyHandlers.ofString());
    }

    private static String field(String json, String name) {
        int at = json.indexOf("\"" + name + "\":\"");
        return at < 0 ? json : json.substring(at + name.length() + 4, json.indexOf('"', at + name.length() + 4));
    }

    private SpringRemoteFacadeDemo() {
    }
}
