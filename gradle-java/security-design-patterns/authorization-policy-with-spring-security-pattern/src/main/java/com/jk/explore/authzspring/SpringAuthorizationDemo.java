package com.jk.explore.authzspring;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.Base64;
import java.util.List;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * The five acts: a real Spring Boot server with Spring Security, called over HTTP as four users.
 */
public final class SpringAuthorizationDemo {

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

            out.add("ONE. Signed in is enough: the view endpoint forgot the owner check.");
            out.add("  ana views ben's order ORD-7: " + get(base + "/before/orders/ORD-7", "ana"));

            out.add("");
            out.add("TWO. Roles only: hasRole(\"CUSTOMER\") on the URL.");
            out.add("  ana views ben's order ORD-7: " + get(base + "/roles/orders/ORD-7", "ana"));
            out.add("  a role says \"customers may view orders\", not \"their own\"");

            out.add("");
            out.add("THREE. @PreAuthorize rules over who, which order, and how much.");
            out.add("  ana views ORD-7 (ben's):   " + get(base + "/orders/ORD-7", "ana"));
            out.add("  ben views ORD-7 (ben's own): " + get(base + "/orders/ORD-7", "ben"));
            out.add("  sam (support) refunds 80:  " + post(base + "/orders/ORD-7/refund?amount=80", "sam"));
            out.add("  sam (support) refunds 250: " + post(base + "/orders/ORD-7/refund?amount=250", "sam"));
            out.add("  alex (admin) refunds 250:  " + post(base + "/orders/ORD-7/refund?amount=250", "alex"));

            out.add("");
            out.add("FOUR. Deny by default: anyRequest().denyAll().");
            out.add("  alex (admin) exports ORD-7, an endpoint no rule mentions: " + get(base + "/orders/ORD-7/export", "alex"));

            out.add("");
            out.add("FIVE. The bill.");
            out.add("  refusals Spring Security announced as events: " + ctx.getBean(ShopApp.class).denials.size());
            out.add("  rules are strings of SpEL checked only when they run; a typo fails at the first request, not at build time");
            out.add("  and a rule on one method protects only that method: new endpoints rely on denyAll to start closed");
        }
        return out;
    }

    static String get(String url, String user) throws Exception {
        return status(HTTP.send(HttpRequest.newBuilder(URI.create(url)).header("Authorization", basic(user)).GET().build(),
                HttpResponse.BodyHandlers.ofString()));
    }

    static String post(String url, String user) throws Exception {
        return status(HTTP.send(HttpRequest.newBuilder(URI.create(url)).header("Authorization", basic(user))
                .POST(HttpRequest.BodyPublishers.noBody()).build(), HttpResponse.BodyHandlers.ofString()));
    }

    static String status(HttpResponse<String> r) {
        return r.statusCode() == 200 ? "200 " + r.body() : r.statusCode() + " forbidden";
    }

    static String basic(String user) {
        return "Basic " + Base64.getEncoder().encodeToString((user + ":pw").getBytes(StandardCharsets.UTF_8));
    }

    private SpringAuthorizationDemo() {
    }
}
