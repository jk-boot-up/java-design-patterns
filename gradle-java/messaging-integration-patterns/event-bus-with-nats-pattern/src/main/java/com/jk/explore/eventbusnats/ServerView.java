package com.jk.explore.eventbusnats;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.time.Duration;
import java.util.function.LongPredicate;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * Asks the bus about itself.
 *
 * <p>With a bus inside one program you can ask the bus object how many listeners it holds. Once the bus is
 * a separate program, no service can know: only the server does, and it has to be asked over a second port
 * that exists for exactly that. The server also keeps a handful of listeners of its own, for its own
 * housekeeping, so the count here is only of listeners for store events.
 */
public final class ServerView {

    private static final Pattern SUBJECT = Pattern.compile("\"subject\"\\s*:\\s*\"([^\"]+)\"");

    private final HttpClient http = HttpClient.newBuilder().connectTimeout(Duration.ofSeconds(10)).build();
    private final String baseUrl;
    private final String prefix;

    public ServerView(String baseUrl, String prefix) {
        this.baseUrl = baseUrl;
        this.prefix = prefix;
    }

    /** How many listeners for store events the server is holding, across every service connected to it. */
    public long storeListeners() {
        String body = get("/subsz?subs=1&limit=4096");
        Matcher m = SUBJECT.matcher(body);
        long found = 0;
        while (m.find()) {
            if (m.group(1).startsWith(prefix)) {
                found++;
            }
        }
        return found;
    }

    /**
     * Keeps asking the server until its answer is the one being waited for, and gives up with a clear
     * failure rather than hanging. A connection closing is something the server notices in its own time,
     * so asking until it says so is the only honest way to know it has happened.
     */
    public long waitUntilStoreListeners(LongPredicate wanted) {
        long deadline = System.nanoTime() + Duration.ofSeconds(30).toNanos();
        long seen = storeListeners();
        while (!wanted.test(seen)) {
            if (System.nanoTime() > deadline) {
                throw new IllegalStateException(
                        "the server still reports " + seen + " store listeners after 30 seconds");
            }
            Thread.onSpinWait();
            seen = storeListeners();
        }
        return seen;
    }

    private String get(String path) {
        try {
            HttpRequest request = HttpRequest.newBuilder(URI.create(baseUrl + path))
                    .timeout(Duration.ofSeconds(10))
                    .GET()
                    .build();
            HttpResponse<String> response = http.send(request, HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != 200) {
                throw new IllegalStateException("the server answered " + response.statusCode() + " for " + path);
            }
            return response.body();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }
}
