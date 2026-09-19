package com.jk.explore.mvcspring;

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
public class SummaryApplication {

    /** A running shop, and a client for its real HTTP port. It never follows redirects, so they can be seen. */
    static final class Shop implements AutoCloseable {
        final ConfigurableApplicationContext context = new SpringApplicationBuilder(SummaryApplication.class)
                .web(WebApplicationType.SERVLET).run();
        final HttpClient client = HttpClient.newBuilder().followRedirects(HttpClient.Redirect.NEVER).build();

        int port() {
            return ((WebServerApplicationContext) context).getWebServer().getPort();
        }

        HttpResponse<String> get(String path, String accept) {
            return send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port() + path)).header("Accept", accept).GET().build());
        }

        HttpResponse<String> postForm(String path, String form) {
            return send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + port() + path))
                    .header("Content-Type", "application/x-www-form-urlencoded").POST(HttpRequest.BodyPublishers.ofString(form)).build());
        }

        private HttpResponse<String> send(HttpRequest request) {
            try {
                return client.send(request, HttpResponse.BodyHandlers.ofString());
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

    static String between(String html, String before) {
        int start = html.indexOf(before) + before.length();
        return html.substring(start, html.indexOf('<', start));
    }

    public static void main(String[] args) {
        try (Shop shop = new Shop()) {
            System.out.println("ONE. The controller names a view.");
            HttpResponse<String> page = shop.get("/orders/ORD-000001", "text/html");
            System.out.println("  GET /orders/ORD-000001, as a browser -> " + page.statusCode() + ", " + page.headers().firstValue("Content-Type").orElse("") .split(";")[0] + ".");
            System.out.println("  the page says: Total: " + between(page.body(), "Total: <span>") + ", Discount: " + between(page.body(), "Discount: <span>") + ".");

            System.out.println("TWO. The same model, a second view.");
            HttpResponse<String> json = shop.get("/orders/ORD-000001", "application/json");
            System.out.println("  GET /orders/ORD-000001, as a program -> " + json.statusCode() + " " + json.body());
            System.out.println("  the controller method changed, and the model did not.");

            System.out.println("THREE. The total is worked out once per request.");
            int before = OrderSummary.COMPUTATIONS.get();
            shop.get("/orders/ORD-000001", "text/html");
            System.out.println("  summaries computed for one page view: " + (OrderSummary.COMPUTATIONS.get() - before) + ".");
            System.out.println("  the model alone, no server: " + OrderSummary.of(new OrderStore().find("ORD-000001").orElseThrow()).totalDisplay() + ".");

            System.out.println("FOUR. A sum in the view.");
            HttpResponse<String> naive = shop.get("/orders/ORD-000001/naive", "text/html");
            System.out.println("  the shortcut view says: Total: " + between(naive.body(), "Total: <span>") + "."
                    + " the model says " + OrderSummary.of(new OrderStore().find("ORD-000001").orElseThrow()).totalPence() + " pence.");
            System.out.println("  the view added up the lines and never heard of the discount.");

            System.out.println("FIVE. The same view, another order.");
            HttpResponse<String> created = shop.postForm("/orders", "customer=bo&sku=BNS-220&quantity=1");
            String where = created.headers().firstValue("Location").orElse("").replaceAll("^.*/orders/", "/orders/");
            System.out.println("  POST /orders -> " + created.statusCode() + " redirect to " + where + ".");
            System.out.println("  the shortcut view on that one-line order: " + shop.get(where + "/naive", "text/html").statusCode() + ".");
            System.out.println("  the real view on it: " + shop.get(where, "text/html").statusCode() + ", Total: "
                    + between(shop.get(where, "text/html").body(), "Total: <span>") + ".");

            System.out.println("SIX. Post, redirect, get.");
            System.out.println("  the form post answered with a redirect, not a page.");
            System.out.println("  refreshing the browser repeats the GET, and cannot place the order twice.");
        }
    }
}
