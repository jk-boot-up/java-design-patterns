package com.jk.explore.tracingjaeger;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.trace.Span;
import io.opentelemetry.api.trace.SpanKind;
import io.opentelemetry.api.trace.Tracer;
import io.opentelemetry.context.Context;
import io.opentelemetry.context.Scope;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import java.io.IOException;
import java.net.InetAddress;
import java.net.InetSocketAddress;
import java.util.concurrent.Executors;

/**
 * The recommendations service: a separate Java program, with its own HTTP server and its own
 * OpenTelemetry, which reports its spans to Jaeger by itself.
 *
 * <p>It answers {@code GET /recommendations}. It reads the traceparent header, if there is one,
 * and continues that trace; if there is none, it starts a trace of its own. Inside, it runs a
 * ranking model, which is the slowest single piece of work in the whole page.
 *
 * <p>It prints its port on one line, and runs until its standard input is closed. Then it sends
 * whatever spans it is still holding and exits, which is a polite shutdown. Killing it instead
 * skips that last send.
 */
public final class RecommendationsService {

    static final String NAME = "recommendations";
    static final AttributeKey<String> VISIT = AttributeKey.stringKey("shop.visit");

    private final Tracer tracer;
    private final OpenTelemetrySdk sdk;
    private final long ownMillis;
    private final long rankingMillis;

    RecommendationsService(OpenTelemetrySdk sdk, long ownMillis, long rankingMillis) {
        this.sdk = sdk;
        this.tracer = sdk.getTracer(NAME);
        this.ownMillis = ownMillis;
        this.rankingMillis = rankingMillis;
    }

    /** Arguments: collector address, clock offset in milliseconds, own work, ranking work, id seed. */
    public static void main(String[] args) throws IOException {
        Telemetry.Settings settings = Telemetry.Settings.of(NAME, args[0], Long.parseLong(args[4]))
                .withClockOffBy(Long.parseLong(args[1]));
        OpenTelemetrySdk sdk = Telemetry.start(settings);
        RecommendationsService service = new RecommendationsService(sdk, Long.parseLong(args[2]), Long.parseLong(args[3]));

        HttpServer server = HttpServer.create(new InetSocketAddress(InetAddress.getLoopbackAddress(), 0), 0);
        server.createContext("/recommendations", service::handle);
        server.setExecutor(Executors.newFixedThreadPool(4));
        server.start();
        System.out.println("listening on port " + server.getAddress().getPort());
        System.out.flush();

        // Runs until whoever started it closes our standard input.
        while (System.in.read() != -1) {
            // nothing to read; waiting for the end
        }
        server.stop(0);
        Telemetry.stop(sdk);
        System.out.println("stopped, spans sent");
        System.exit(0);
    }

    void handle(HttpExchange exchange) throws IOException {
        String received = exchange.getRequestHeaders().getFirst(Http.TRACEPARENT);
        Context parent = sdk.getPropagators().getTextMapPropagator()
                .extract(Context.root(), exchange, Http.OFF_EXCHANGE);
        String visit = Http.query(exchange).getOrDefault("visit", "none");

        Span span = tracer.spanBuilder("GET /recommendations")
                .setSpanKind(SpanKind.SERVER)
                .setParent(parent)
                .setAttribute(VISIT, visit)
                .startSpan();
        String body;
        try (Scope ignored = span.makeCurrent()) {
            Http.work(ownMillis / 2);
            Span ranking = tracer.spanBuilder("ranking-model").startSpan();
            try (Scope alsoIgnored = ranking.makeCurrent()) {
                Http.work(rankingMillis);
            } finally {
                ranking.end();
            }
            Http.work(ownMillis - ownMillis / 2);
            body = "received-traceparent: " + (received == null ? "none" : received) + "\n"
                    + "trace-id: " + span.getSpanContext().getTraceId() + "\n"
                    + "recommended: SKU-9002 SKU-1183 SKU-5530\n";
        } finally {
            // Ended before the answer goes back, so that by the time the page has its answer
            // this service has finished its span and holds it, waiting for the next batch.
            span.end();
        }
        Http.answer(exchange, 200, body);
    }
}
