package com.jk.explore.tracingjaeger;

import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.utility.DockerImageName;

/**
 * A real Jaeger, running in a container that this demo starts and stops itself.
 *
 * <p>Jaeger is the collector: a separate program that services send their finished spans to,
 * and that puts the spans of one request back together by their shared trace id. This image
 * holds the collector, the storage (in memory) and the query API in one process, so the demo
 * starts one container and nothing else.
 */
public class JaegerServer implements AutoCloseable {

    /** Jaeger 2.21.0, the newest release at the time this project was written. */
    public static final String IMAGE = "jaegertracing/jaeger:2.21.0";

    /** Where services send spans: OpenTelemetry's own protocol, OTLP, over plain HTTP. */
    private static final int OTLP_HTTP_PORT = 4318;

    /** Where the demo asks what Jaeger holds: the same API Jaeger's web page uses. */
    private static final int QUERY_PORT = 16686;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Jaeger collector.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but Jaeger will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The Jaeger container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    // Testcontainers maps both ports to free random ports on this machine, so this demo can
    // run beside any other Jaeger without a clash. The query page answering is the sign that
    // Jaeger is ready.
    private final GenericContainer<?> container =
            new GenericContainer<>(DockerImageName.parse(IMAGE))
                    .withExposedPorts(OTLP_HTTP_PORT, QUERY_PORT)
                    .waitingFor(Wait.forHttp("/").forPort(QUERY_PORT));

    /**
     * True when there is a container runtime this demo can use. Checked before anything
     * starts, so a machine without one gets a sentence rather than a stack trace.
     */
    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
    }

    /** The address a service sends its spans to. */
    public String otlpEndpoint() {
        return "http://" + container.getHost() + ":" + container.getMappedPort(OTLP_HTTP_PORT) + "/v1/traces";
    }

    /** A client for Jaeger's query API. */
    public JaegerQuery query() {
        return new JaegerQuery("http://" + container.getHost() + ":" + container.getMappedPort(QUERY_PORT));
    }

    /**
     * The line Jaeger prints at start-up saying where it keeps spans, as Jaeger wrote it. Out of
     * the box that is its memory, so everything it holds goes when the container does.
     */
    public String storageLine() {
        return container.getLogs().lines()
                .filter(line -> line.contains("storage") && line.contains("configuration"))
                .map(line -> line.replaceFirst("^\\S+ \\S+ ", "").trim())
                .findFirst()
                .orElse("no storage line printed");
    }

    @Override
    public void close() {
        container.stop();
    }
}
