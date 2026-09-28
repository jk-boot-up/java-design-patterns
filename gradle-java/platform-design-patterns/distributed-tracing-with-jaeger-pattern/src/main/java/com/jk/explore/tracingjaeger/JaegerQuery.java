package com.jk.explore.tracingjaeger;

import java.io.IOException;
import java.net.URI;
import java.net.URLEncoder;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.time.Instant;
import java.time.temporal.ChronoUnit;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import tools.jackson.databind.JsonNode;
import tools.jackson.databind.ObjectMapper;

/**
 * Asks Jaeger what it holds, through the same HTTP API that Jaeger's own web page uses.
 *
 * <p>Nothing in this class knows what the services did. Everything it returns is what reached
 * the collector, as the collector assembled it. That is the whole point: the services' own
 * account of a request can be wrong, and this is the check they cannot fake.
 */
public final class JaegerQuery {

    private static final ObjectMapper JSON = new ObjectMapper();
    private static final HttpClient CLIENT = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();

    private final String base;

    JaegerQuery(String base) {
        this.base = base;
    }

    /** One span, as Jaeger holds it. Times are in microseconds. */
    public record HeldSpan(String spanId, String parentSpanId, String name, String service,
                           long startMicros, long durationMicros) {

        public boolean isRoot() {
            return parentSpanId == null;
        }
    }

    /** One trace, as Jaeger assembled it, with any warnings Jaeger attached. */
    public record HeldTrace(String traceId, List<HeldSpan> spans, List<String> warnings) {

        public long roots() {
            return spans.stream().filter(HeldSpan::isRoot).count();
        }

        public long servicesCount() {
            return spans.stream().map(HeldSpan::service).distinct().count();
        }

        public long spansFrom(String service) {
            return spans.stream().filter(s -> s.service().equals(service)).count();
        }

        public Optional<HeldSpan> named(String name) {
            return spans.stream().filter(s -> s.name().equals(name)).findFirst();
        }

        public Optional<HeldSpan> named(String name, String service) {
            return spans.stream().filter(s -> s.name().equals(name) && s.service().equals(service)).findFirst();
        }

        public Optional<HeldSpan> parentOf(HeldSpan span) {
            return spans.stream().filter(s -> s.spanId().equals(span.parentSpanId())).findFirst();
        }

        /** Spans in start order, which is the order they happened in, if every clock agrees. */
        public List<HeldSpan> inStartOrder() {
            List<HeldSpan> sorted = new ArrayList<>(spans);
            sorted.sort(Comparator.comparingLong(HeldSpan::startMicros));
            return sorted;
        }

        public List<HeldSpan> childrenOf(HeldSpan parent) {
            return inStartOrder().stream().filter(s -> parent.spanId().equals(s.parentSpanId())).toList();
        }
    }

    /** The trace with this id, or nothing if Jaeger has never received a span of it. */
    public Optional<HeldTrace> trace(String traceId) {
        List<HeldTrace> found = traces(base + "/api/v3/traces/" + traceId);
        return found.isEmpty() ? Optional.empty() : Optional.of(found.get(0));
    }

    /**
     * Every trace holding a span from {@code service} tagged with this shop visit. This is how
     * you find a trace when you do not know its id: by something the business recorded.
     */
    public List<HeldTrace> tracesForVisit(String service, String visit) {
        Instant now = Instant.now();
        String url = base + "/api/v3/traces?query.service_name=" + service
                + "&query.attributes=" + URLEncoder.encode("{\"shop.visit\":\"" + visit + "\"}", StandardCharsets.UTF_8)
                + "&query.start_time_min=" + now.minus(Duration.ofHours(1)).truncatedTo(ChronoUnit.SECONDS)
                + "&query.start_time_max=" + now.plus(Duration.ofHours(1)).truncatedTo(ChronoUnit.SECONDS);
        return traces(url);
    }

    /** The names of every service that has reported at least one span, Jaeger's own included. */
    public List<String> services() {
        JsonNode data = JSON.readTree(send(base + "/api/v3/services").body()).path("services");
        List<String> names = new ArrayList<>();
        for (JsonNode name : data) {
            names.add(name.asString());
        }
        names.sort(Comparator.naturalOrder());
        return names;
    }

    /**
     * Jaeger's version 3 API answers in OpenTelemetry's own format: spans grouped by the service
     * that sent them. This regroups them by trace id, which is the collector's whole job.
     */
    private static List<HeldTrace> traces(String url) {
        HttpResponse<String> response = send(url);
        if (response.statusCode() == 404) {
            return List.of();
        }
        if (response.statusCode() != 200) {
            throw new IllegalStateException("Jaeger answered " + response.statusCode() + ": " + response.body());
        }
        Map<String, List<HeldSpan>> byTrace = new LinkedHashMap<>();
        Map<String, List<String>> warnings = new LinkedHashMap<>();
        for (JsonNode group : JSON.readTree(response.body()).path("result").path("resourceSpans")) {
            String service = attribute(group.path("resource").path("attributes"), "service.name");
            for (JsonNode scope : group.path("scopeSpans")) {
                for (JsonNode span : scope.path("spans")) {
                    String traceId = span.path("traceId").asString();
                    String parent = span.path("parentSpanId").asString("");
                    long start = Long.parseLong(span.path("startTimeUnixNano").asString());
                    long end = Long.parseLong(span.path("endTimeUnixNano").asString());
                    byTrace.computeIfAbsent(traceId, k -> new ArrayList<>()).add(new HeldSpan(
                            span.path("spanId").asString(), parent.isEmpty() ? null : parent,
                            span.path("name").asString(), service, start / 1000, (end - start) / 1000));
                    for (JsonNode a : span.path("attributes")) {
                        if (JAEGER_WARNINGS.equals(a.path("key").asString())) {
                            for (JsonNode w : a.path("value").path("arrayValue").path("values")) {
                                warnings.computeIfAbsent(traceId, k -> new ArrayList<>()).add(w.path("stringValue").asString());
                            }
                        }
                    }
                }
            }
        }
        List<HeldTrace> result = new ArrayList<>();
        byTrace.forEach((id, spans) -> result.add(new HeldTrace(id, List.copyOf(spans),
                List.copyOf(warnings.getOrDefault(id, List.of())))));
        return result;
    }

    /** Where Jaeger puts the warnings it attaches to a span it thinks is suspicious. */
    private static final String JAEGER_WARNINGS = "@jaeger@warnings";

    private static String attribute(JsonNode attributes, String key) {
        for (JsonNode a : attributes) {
            if (key.equals(a.path("key").asString())) {
                return a.path("value").path("stringValue").asString();
            }
        }
        return "unknown";
    }

    private static HttpResponse<String> send(String url) {
        try {
            return CLIENT.send(HttpRequest.newBuilder(URI.create(url)).timeout(Duration.ofSeconds(30)).GET().build(),
                    HttpResponse.BodyHandlers.ofString());
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
