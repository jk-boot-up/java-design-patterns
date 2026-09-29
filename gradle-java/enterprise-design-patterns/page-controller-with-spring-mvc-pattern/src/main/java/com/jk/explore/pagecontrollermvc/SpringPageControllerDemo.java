package com.jk.explore.pagecontrollermvc;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * The five acts: a real Spring MVC web application on a local port, called over HTTP.
 */
public final class SpringPageControllerDemo {

    static final HttpClient HTTP = HttpClient.newHttpClient();

    public static void main(String[] args) throws Exception {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (ConfigurableApplicationContext ctx = start(false)) {
            String base = base(ctx);

            out.add("ONE. One handler for every page.");
            out.add("  GET /old/basket?add=MUG-1&qty=2 -> " + get(base, "/old/basket?add=MUG-1&qty=2", false));
            out.add("  GET /old/product?sku=KETTLE-1   -> " + get(base, "/old/product?sku=KETTLE-1", false));
            out.add("  quantity parsing was added for the basket; it now runs for every page");

            out.add("");
            out.add("TWO. A @RestController for each page.");
            out.add("  GET /product?sku=KETTLE-1       -> " + get(base, "/product?sku=KETTLE-1", false));
            out.add("  GET /basket?add=MUG-1&qty=2     -> " + get(base, "/basket?add=MUG-1&qty=2", false));

            out.add("");
            out.add("THREE. Each page's input, converted and checked by Spring.");
            out.add("  GET /product?sku=SOFA-9         -> " + get(base, "/product?sku=SOFA-9", false));
            out.add("  GET /basket?add=MUG-1&qty=two   -> " + get(base, "/basket?add=MUG-1&qty=two", false)
                    + "  (Spring could not turn \"two\" into an int)");

            out.add("");
            out.add("FOUR. A new page is a new class.");
            out.add("  GET /reviews?sku=KETTLE-1       -> " + get(base, "/reviews?sku=KETTLE-1", false));
            out.add("  no other controller was opened; Spring found it by its annotation");

            out.add("");
            out.add("FIVE. The bill: checks every page needs.");
            out.add("  GET /checkout, not logged in    -> " + get(base, "/checkout", false)
                    + "  (its author forgot the login check)");
        }
        try (ConfigurableApplicationContext ctx = start(true)) {
            String base = base(ctx);
            out.add("  with one HandlerInterceptor registered for /basket and /checkout:");
            out.add("  GET /checkout, not logged in    -> " + get(base, "/checkout", false));
            out.add("  GET /checkout, logged in        -> " + get(base, "/checkout", true));
            out.add("  shared checks belong in one place; page controllers keep only what is theirs");
        }
        return out;
    }

    static ConfigurableApplicationContext start(boolean interceptor) {
        return new SpringApplicationBuilder(ShopApp.class)
                .properties("server.port=0", "spring.main.banner-mode=off", "logging.level.root=OFF",
                        "server.error.include-message=always", "shop.login-interceptor=" + interceptor)
                .run();
    }

    static String base(ConfigurableApplicationContext ctx) {
        return "http://127.0.0.1:" + ctx.getEnvironment().getProperty("local.server.port");
    }

    static String get(String base, String path, boolean loggedIn) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(URI.create(base + path)).GET();
        if (loggedIn) {
            r.header("X-Customer", "priya");
        }
        HttpResponse<String> response = HTTP.send(r.build(), HttpResponse.BodyHandlers.ofString());
        String body = response.body();
        if (body.startsWith("{")) {   // Spring's JSON error page: show its message, or its error name
            String message = field(body, "message");
            body = message == null || message.isEmpty() ? field(body, "error") : message;
        }
        return response.statusCode() + " " + body;
    }

    private static String field(String json, String name) {
        int at = json.indexOf("\"" + name + "\":\"");
        return at < 0 ? null : json.substring(at + name.length() + 4, json.indexOf('"', at + name.length() + 4));
    }

    private SpringPageControllerDemo() {
    }
}
