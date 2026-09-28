package com.jk.explore.tracingjaeger;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.Scope;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.net.URI;
import java.net.http.HttpRequest;
import java.util.Map;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

/**
 * The product page: the shop's front door, and the first of the two services.
 *
 * <p>It answers {@code GET /product/{sku}}. It looks the product up in the catalog, asks
 * pricing for a quote, checks stock, then calls the recommendations service over real HTTP,
 * and renders the page. Every one of those is a span. The call to recommendations is where the
 * trace has to cross into another program, and whether it does depends on one line: the one
 * that writes the traceparent header onto the outgoing request.
 */
public final class ProductPageService implements AutoCloseable {

    static final String NAME = "product-page";

    /** How long each step of building a page takes. */
    public record Work(long catalog, long pricing, long inventory, long render) {
        public static final Work NORMAL = new Work(120, 180, 90, 110);
        public static final Work NONE = new Work(0, 0, 0, 0);
    }

    private final OpenTelemetrySdk sdk;
    private final Tracer tracer;
    private final String recommendationsUrl;
    private final Work work;
    private final boolean forwardsTheHeader;
    private final HttpServer server;
    private final ExecutorService threads = Executors.newFixedThreadPool(4);

    /**
     * @param forwardsTheHeader false to leave out the one line that writes traceparent onto
     *                          the call to recommendations, as a service nobody instrumented would
     */
    public ProductPageService(OpenTelemetrySdk sdk, String recommendationsUrl, Work work, boolean forwardsTheHeader) {
        this.sdk = sdk;
        this.tracer = sdk.getTracer(NAME);
        this.recommendationsUrl = recommendationsUrl;
        this.work = work;
        this.forwardsTheHeader = forwardsTheHeader;
        try {
            this.server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
        server.createContext("/product/", this::handle);
        server.setExecutor(threads);
        server.start();
    }

    public String baseUrl() {
        return "http://127.0.0.1:" + server.getAddress().getPort();
    }

    void handle(HttpExchange exchange) throws IOException {
        String sku = exchange.getRequestURI().getPath().substring("/product/".length());
        String visit = Http.query(exchange).getOrDefault("visit", "none");
        // The customer's browser sends no traceparent, so this starts a new trace: the front door.
        Context parent = sdk.getPropagators().getTextMapPropagator()
                .extract(Context.root(), exchange, Http.OFF_EXCHANGE);

        Span page = tracer.spanBuilder("GET /product/" + sku)
                .setSpanKind(SpanKind.SERVER)
                .setParent(parent)
                .setAttribute(RecommendationsService.VISIT, visit)
                .startSpan();
        String body;
        try (Scope ignored = page.makeCurrent()) {
            step("catalog", work.catalog());
            step("pricing", work.pricing());
            step("inventory", work.inventory());
            Map<String, String> recommendations = callRecommendations(visit);
            step("render", work.render());
            body = "trace-id: " + page.getSpanContext().getTraceId() + "\n"
                    + "sampled: " + page.getSpanContext().isSampled() + "\n"
                    + "sent-traceparent: " + recommendations.get("sent-traceparent") + "\n"
                    + "received-traceparent: " + recommendations.get("received-traceparent") + "\n"
                    + "recommendations-trace-id: " + recommendations.get("trace-id") + "\n";
        } finally {
            page.end();
        }
        Http.answer(exchange, 200, body);
    }

    private void step(String name, long millis) {
        Span span = tracer.spanBuilder(name).startSpan();
        try (Scope ignored = span.makeCurrent()) {
            Http.work(millis);
        } finally {
            span.end();
        }
    }

    private Map<String, String> callRecommendations(String visit) {
        Span call = tracer.spanBuilder("call recommendations").setSpanKind(SpanKind.CLIENT).startSpan();
        try (Scope ignored = call.makeCurrent()) {
            HttpRequest.Builder request = HttpRequest.newBuilder(URI.create(recommendationsUrl + "/recommendations?visit=" + visit));
            if (forwardsTheHeader) {
                // The pattern, in one line: write the current trace context onto the request.
                sdk.getPropagators().getTextMapPropagator().inject(Context.current(), request, Http.ONTO_REQUEST);
            }
            String sent = request.build().headers().firstValue(Http.TRACEPARENT).orElse("none");
            Map<String, String> answer = Http.fields(Http.get(request));
            answer.put("sent-traceparent", sent);
            return answer;
        } finally {
            call.end();
        }
    }

    @Override
    public void close() {
        server.stop(0);
        threads.shutdownNow();
    }
}
