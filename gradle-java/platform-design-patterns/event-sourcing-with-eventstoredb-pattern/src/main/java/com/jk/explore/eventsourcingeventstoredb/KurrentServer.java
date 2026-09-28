package com.jk.explore.eventsourcingeventstoredb;

import io.kurrent.dbclient.KurrentDBClient;
import io.kurrent.dbclient.KurrentDBConnectionString;
import java.time.Duration;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.utility.DockerImageName;

/**
 * A real KurrentDB server — the database once called EventStoreDB — running in a container that
 * this demo starts and stops itself.
 *
 * <p>KurrentDB is a database built for one job: keeping events in order, in named lists it calls
 * streams, and never changing them. It is a separate program from the shop. Any program that can
 * reach it sees the same streams.
 *
 * <p><strong>It runs insecure here.</strong> The container is started with security switched off:
 * no TLS, so traffic is not encrypted, and no user names or passwords, so anyone who can reach the
 * port can read and write everything. That keeps the demo to one container and one port on your
 * own machine. A production server must never run like this.
 */
public class KurrentServer implements AutoCloseable {

    /** The newest release of KurrentDB at the time this project was written. */
    public static final String VERSION = "26.1.2";

    /**
     * The image for this machine. KurrentDB publishes its Intel build under the plain version tag,
     * and its ARM build, for Apple silicon, under a tag the vendor labels experimental. The two are
     * the same release.
     */
    public static final String IMAGE_INTEL = "kurrentplatform/kurrentdb:" + VERSION;
    public static final String IMAGE_ARM = "kurrentplatform/kurrentdb:" + VERSION + "-experimental-arm64-10.0-noble";

    /** KurrentDB answers both its HTTP health check and its gRPC clients on this one port. */
    private static final int PORT = 2113;

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real KurrentDB server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but KurrentDB will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The KurrentDB container would not start. The image is " + IMAGE_INTEL + " (or its ARM build).\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final GenericContainer<?> container = new GenericContainer<>(DockerImageName.parse(imageForThisMachine()))
            .withExposedPorts(PORT)
            // Security off: no TLS and no passwords. For a demo on one machine only.
            .withEnv("KURRENTDB_INSECURE", "true")
            // One server, not a cluster, and none of the server-side projections this project does not use.
            .withEnv("KURRENTDB_CLUSTER_SIZE", "1")
            .withEnv("KURRENTDB_RUN_PROJECTIONS", "None")
            .withEnv("KURRENTDB_TELEMETRY_OPTOUT", "true")
            .waitingFor(Wait.forHttp("/health/live").forPort(PORT).forStatusCode(204)
                    .withStartupTimeout(Duration.ofMinutes(3)));

    /**
     * True when there is a container runtime this demo can use. Checked before anything starts,
     * so a machine without one gets a sentence rather than a stack trace.
     */
    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    /** The ARM image on an ARM container runtime, the Intel one everywhere else. */
    public static String imageForThisMachine() {
        try {
            String arch = DockerClientFactory.instance().getInfo().getArchitecture();
            if (arch != null && (arch.contains("aarch64") || arch.contains("arm64"))) {
                return IMAGE_ARM;
            }
        } catch (Throwable ignored) {
            // fall through to the Intel image
        }
        return IMAGE_INTEL;
    }

    public void start() {
        container.start();
    }

    /** How a client finds the server: host, the random port on this machine, and tls=false. */
    public String connectionString() {
        return "kurrentdb://" + container.getHost() + ":" + container.getMappedPort(PORT) + "?tls=false";
    }

    /**
     * A new, separate connection. Each till in the demo gets its own, so the two tills are two
     * clients of the server, exactly as two checkout machines in a shop would be.
     */
    public KurrentDBClient connect() {
        return KurrentDBClient.create(KurrentDBConnectionString.parseOrThrow(connectionString()));
    }

    @Override
    public void close() {
        container.stop();
    }
}
