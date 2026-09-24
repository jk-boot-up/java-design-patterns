package com.jk.explore.databaseperservicecontainers;

import org.testcontainers.DockerClientFactory;

/**
 * The two database servers, one of each engine, started together and stopped together.
 *
 * <p>Exactly one Postgres container and one MongoDB container, however many databases and
 * services use them.
 */
public class Engines implements AutoCloseable {

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real PostgreSQL server and a real MongoDB server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but a database will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "A database container would not start. The images are " + Postgres.IMAGE + " and " + Mongo.IMAGE + ".\n"
            + "Check that the container runtime is running, has about 1.5 GB of disk free and can reach the internet, then run ./gradlew run again.";

    private final Postgres postgres = new Postgres();
    private final Mongo mongo = new Mongo();

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
        postgres.start();
        mongo.start();
    }

    public Postgres postgres() {
        return postgres;
    }

    public Mongo mongo() {
        return mongo;
    }

    @Override
    public void close() {
        try {
            mongo.stop();
        } finally {
            postgres.stop();
        }
    }
}
