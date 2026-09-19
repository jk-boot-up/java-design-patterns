package com.jk.explore.flagd;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;
import java.util.Map;
import java.util.TreeMap;
import java.util.function.BooleanSupplier;

/** A real flagd, the OpenFeature flag daemon, in a Docker container. Its flags are a file that it watches. */
public class Flagd implements AutoCloseable {

    public static final String IMAGE = "ghcr.io/open-feature/flagd:latest";
    private static final String CONTAINER = "patterns-flagd";
    private static final int PORT = 8013;

    private final Path dir;
    private final Map<String, Rule> flags = new TreeMap<>();
    private int revision;

    public Flagd() throws IOException {
        this.dir = Files.createTempDirectory("flagd");
    }

    public static boolean toolsAvailable() {
        return Shell.works("docker", "info") && (Shell.works("docker", "image", "inspect", IMAGE) || Shell.works("docker", "pull", "-q", IMAGE));
    }

    /** The file exactly as flagd reads it. */
    static String file(Map<String, Rule> flags) {
        StringBuilder b = new StringBuilder("{\"$schema\":\"https://flagd.dev/schema/v0/flags.json\",\"flags\":{");
        boolean first = true;
        for (Map.Entry<String, Rule> e : flags.entrySet()) {
            b.append(first ? "" : ",").append('"').append(e.getKey()).append("\":").append(e.getValue().json());
            first = false;
        }
        return b.append("}}").toString();
    }

    /**
     * Writes the file. Every write also carries a flag named after its revision, which is always on, so that
     * the demo can tell when flagd has read this version of the file and not an earlier one.
     */
    public void define(String name, Rule rule) throws IOException {
        flags.put(name, rule);
        flags.remove("revision-" + revision);
        revision++;
        flags.put("revision-" + revision, new Rule.On());
        Files.writeString(dir.resolve("flags.json"), file(flags));
    }

    public void start() {
        stop();
        Shell.run("docker", "run", "-d", "--rm", "--name", CONTAINER, "-p", "127.0.0.1:" + PORT + ":" + PORT,
                "-v", dir + ":/flags:ro", IMAGE, "start", "--uri", "file:/flags/flags.json");
        waitUntil(() -> Boolean.TRUE.equals(evaluate("revision-" + revision, "probe")));
    }

    public void stop() {
        Shell.works("docker", "rm", "-f", CONTAINER);
    }

    /** Changes a flag's rule by rewriting the file, and waits until flagd has read the new file. */
    public void change(String name, Rule rule) throws IOException {
        define(name, rule);
        int expected = revision;
        waitUntil(() -> Boolean.TRUE.equals(evaluate("revision-" + expected, "probe")));
    }

    /** Asks flagd for a boolean flag. Returns null if flagd cannot be reached, or does not know the flag. */
    public Boolean evaluate(String flag, String customer) {
        try (HttpClient client = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(1)).build()) {
            HttpResponse<String> r = client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + PORT + "/flagd.evaluation.v1.Service/ResolveBoolean"))
                    .timeout(Duration.ofSeconds(2)).header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString("{\"flagKey\":\"" + flag + "\",\"context\":{\"targetingKey\":\"" + customer + "\"}}")).build(),
                    HttpResponse.BodyHandlers.ofString());
            if (r.statusCode() != 200) {
                return null;
            }
            return r.body().contains("\"value\":true");
        } catch (Exception e) {
            return null;
        }
    }

    static void waitUntil(BooleanSupplier condition) {
        long end = System.nanoTime() + Duration.ofSeconds(30).toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("flagd did not settle in 30 seconds");
    }

    @Override
    public void close() {
        stop();
    }
}
