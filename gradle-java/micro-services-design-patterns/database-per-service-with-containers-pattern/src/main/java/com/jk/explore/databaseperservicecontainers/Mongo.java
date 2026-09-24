package com.jk.explore.databaseperservicecontainers;

import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import java.util.concurrent.TimeUnit;
import org.testcontainers.mongodb.MongoDBContainer;
import org.testcontainers.utility.DockerImageName;

/**
 * A real MongoDB server, running in a container that this demo starts and stops itself.
 *
 * <p>MongoDB is a document database. Instead of rows in a table with fixed columns, it
 * keeps documents — small records of named fields, like a filled-in form — in a
 * collection, and two documents in the same collection need not have the same fields. It
 * is asked questions with query documents rather than SQL. The Catalog service keeps its
 * products here.
 */
public class Mongo implements AutoCloseable {

    /**
     * MongoDB 8.3.11 on Ubuntu 24.04 ("noble"), the newest release at the time this project
     * was written. MongoDB publishes no Alpine image; this is its smallest Linux one.
     */
    public static final String IMAGE = "mongo:8.3.11-noble";

    /** How long a client waits for an answer before it gives up and reports an error. */
    private static final int GIVE_UP_AFTER_SECONDS = 3;

    private final MongoDBContainer container = new MongoDBContainer(DockerImageName.parse(IMAGE));

    public void start() {
        container.start();
    }

    /** A new client for this server. Each service that uses MongoDB opens its own. */
    public MongoClient newClient() {
        MongoClientSettings settings = MongoClientSettings.builder()
                .applyConnectionString(new ConnectionString(container.getConnectionString()))
                .applyToClusterSettings(b -> b.serverSelectionTimeout(GIVE_UP_AFTER_SECONDS, TimeUnit.SECONDS))
                .applyToSocketSettings(b -> b.connectTimeout(GIVE_UP_AFTER_SECONDS, TimeUnit.SECONDS)
                        .readTimeout(GIVE_UP_AFTER_SECONDS, TimeUnit.SECONDS))
                .build();
        return MongoClients.create(settings);
    }

    /** Stops the MongoDB server. Anything that asks it a question afterwards gets an error. */
    public void stop() {
        container.stop();
    }

    public boolean isRunning() {
        return container.isRunning();
    }

    @Override
    public void close() {
        stop();
    }
}
