package com.jk.explore.tracingjaeger;

import com.sun.net.httpserver.HttpExchange;
import io.opentelemetry.context.propagation.TextMapGetter;
import io.opentelemetry.context.propagation.TextMapSetter;
import java.io.IOException;
import java.io.OutputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * The small amount of HTTP both services need: reading and writing the trace context header,
 * sending a GET, and answering one.
 */
final class Http {

    /** The W3C Trace Context header. The one line of text that carries a trace across a hop. */
    static final String TRACEPARENT = "traceparent";

    private static final HttpClient CLIENT = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(10))
            .version(HttpClient.Version.HTTP_1_1)
            .build();

    private Http() {
    }

    /** How OpenTelemetry writes a header onto an outgoing request. */
    static final TextMapSetter<HttpRequest.Builder> ONTO_REQUEST =
            (request, name, value) -> request.header(name, value);

    /** How OpenTelemetry reads a header off an incoming request. */
    static final TextMapGetter<HttpExchange> OFF_EXCHANGE = new TextMapGetter<>() {
        @Override
        public Iterable<String> keys(HttpExchange exchange) {
            return exchange.getRequestHeaders().keySet();
        }

        @Override
        public String get(HttpExchange exchange, String name) {
            return exchange == null ? null : exchange.getRequestHeaders().getFirst(name);
        }
    };

    static String get(HttpRequest.Builder request) {
        try {
            HttpResponse<String> response = CLIENT.send(request.GET().timeout(Duration.ofSeconds(30)).build(),
                    HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != 200) {
                throw new IllegalStateException("HTTP " + response.statusCode() + ": " + response.body());
            }
            return response.body();
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    static String get(String url) {
        return get(HttpRequest.newBuilder(URI.create(url)));
    }

    static void answer(HttpExchange exchange, int status, String body) throws IOException {
        byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
        exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
        exchange.sendResponseHeaders(status, bytes.length);
        try (OutputStream out = exchange.getResponseBody()) {
            out.write(bytes);
        }
    }

    /** The query string as a map: {@code visit=visit-1} becomes {visit: visit-1}. */
    static Map<String, String> query(HttpExchange exchange) {
        Map<String, String> result = new HashMap<>();
        String raw = exchange.getRequestURI().getRawQuery();
        if (raw == null) {
            return result;
        }
        for (String pair : raw.split("&")) {
            int eq = pair.indexOf('=');
            if (eq > 0) {
                result.put(pair.substring(0, eq), pair.substring(eq + 1));
            }
        }
        return result;
    }

    /** Lines of {@code name: value} back into a map. Both services answer in that form. */
    static Map<String, String> fields(String body) {
        Map<String, String> result = new HashMap<>();
        for (String line : List.of(body.split("\n"))) {
            int colon = line.indexOf(": ");
            if (colon > 0) {
                result.put(line.substring(0, colon), line.substring(colon + 2));
            }
        }
        return result;
    }

    /** Stands in for real work: a database query, a price calculation, a model scoring products. */
    static void work(long millis) {
        if (millis <= 0) {
            return;
        }
        try {
            Thread.sleep(millis);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
