package com.jk.explore.sidecarjavaproxy.real.javaproxy;

import java.io.OutputStream;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.security.cert.X509Certificate;
import java.time.Duration;
import java.util.concurrent.Executors;

import javax.net.ssl.SSLContext;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;

/**
 * The replacement proxy: the same job nginx was doing, in Java, on the same port.
 *
 * <p><b>Why this class takes no framework.</b> The argument this project makes
 * is that twenty-two lines of somebody else's configuration became a few dozen
 * lines of your own code, and that the bill for those lines is longer than the
 * benefit. A proxy that pulled in a web framework to make the point would not
 * be that proxy — it would be a service, with a container image ten times the
 * size and a dependency tree to patch. So the HTTP server here is the one built
 * into the JDK, the client is {@code java.net.http.HttpClient}, and the whole
 * of it compiles against the platform and nothing else.
 *
 * <p><b>What it has that nginx does not.</b> One sentence: it waits between
 * attempts, and doubles the wait each time. That is {@link #BACKOFF_MILLIS} and
 * the {@code sleep} in {@link #forward}, and it is the entire difference. nginx
 * retries by moving to the next entry in an upstream group, and that move is
 * immediate by design; there is no directive in its http proxy module that
 * expresses a delay.
 *
 * <p><b>What it does not have, and nginx did.</b> Everything else. There is no
 * connection pool worth the name, no access log in the shop's shared format, no
 * header hygiene, no request buffering, no rate limiting, no way to terminate
 * TLS on the inbound side, and nobody is publishing security fixes for it while
 * you sleep. This class is deliberately not improved past the point the
 * argument needs, because a forty-line proxy that grows all of that back is not
 * a forty-line proxy any more, and the honest version of this project has to
 * keep showing you that.
 *
 * <p><b>The 429 is final.</b> A refusal means the merchant account's allowance
 * is spent. Retrying it is how one service's over-eager policy takes down every
 * other service's payments, so it breaks out of the loop immediately — the same
 * rule nginx enforces through {@code proxy_next_upstream error timeout http_503}
 * and nothing else. Being able to write the waiting is not a licence to become
 * greedier, and both proxies spend exactly the same allowance.
 */
public final class JavaProxy {

    /** The port the service next door is configured with. It never changes. */
    private static final int PORT = 8081;

    /** Up to three attempts, as the provider's March letter asks. */
    private static final int MAX_ATTEMPTS = 3;

    /** The first wait. The second is twice this, the third twice that. */
    private static final long BACKOFF_MILLIS = 200;

    private static final Duration TIMEOUT = Duration.ofSeconds(2);

    private final String serviceName;
    private final URI provider;
    private final HttpClient client;

    private JavaProxy(String serviceName, URI provider) throws Exception {
        this.serviceName = serviceName;
        this.provider = provider;
        this.client = HttpClient.newBuilder()
                .connectTimeout(TIMEOUT)
                .sslContext(trustingTheDemoCertificate())
                .build();
    }

    public static void main(String[] args) throws Exception {
        String serviceName = env("SERVICE_NAME", "checkout");
        URI provider = URI.create(env("PROVIDER_URL", "https://gateway:9443/pay"));

        JavaProxy proxy = new JavaProxy(serviceName, provider);
        HttpServer server = HttpServer.create(new java.net.InetSocketAddress(PORT), 0);
        server.createContext("/pay", proxy::handlePay);
        server.createContext("/healthz", exchange ->
                reply(exchange, 200, serviceName + " java-proxy up\n"));
        // A single-threaded executor, because the demo makes one payment at a
        // time and a thread pool here would be a claim about production
        // readiness this class has no right to make.
        server.setExecutor(Executors.newSingleThreadExecutor());
        server.start();
        System.out.println("java-proxy for " + serviceName + " listening on " + PORT
                + ", forwarding to " + provider);
    }

    private void handlePay(HttpExchange exchange) {
        try {
            byte[] payment = exchange.getRequestBody().readAllBytes();
            Answer answer = forward(payment);
            reply(exchange, answer.status, answer.body);
        } catch (Exception couldNotReachTheProvider) {
            reply(exchange, 502, "{\"outcome\":\"proxy could not reach the provider\","
                    + "\"note\":\"" + couldNotReachTheProvider.getClass().getSimpleName()
                    + "\"}");
        }
    }

    /**
     * The loop. Read it beside §41's nginx configuration and the only thing
     * this one has that that one has no words for is the sleep.
     */
    private Answer forward(byte[] payment) throws Exception {
        long backoff = BACKOFF_MILLIS;
        Answer last = new Answer(502, "{\"outcome\":\"no attempt was made\"}");

        for (int attempt = 1; attempt <= MAX_ATTEMPTS; attempt++) {
            HttpRequest request = HttpRequest.newBuilder(provider)
                    .timeout(TIMEOUT)
                    .header("Content-Type", "application/json")
                    .header("X-Service", serviceName)
                    .POST(HttpRequest.BodyPublishers.ofByteArray(payment))
                    .build();

            HttpResponse<String> response =
                    client.send(request, HttpResponse.BodyHandlers.ofString());
            last = new Answer(response.statusCode(), response.body());

            if (response.statusCode() == 429) {
                break;                       // a refusal is final, never retried
            }
            if (response.statusCode() < 500) {
                return last;                 // charged, or an answer worth keeping
            }
            if (attempt < MAX_ATTEMPTS) {
                Thread.sleep(backoff);
                backoff *= 2;                // 200ms, then 400ms
            }
        }
        return last;
    }

    private static void reply(HttpExchange exchange, int status, String body) {
        try (OutputStream out = exchange.getResponseBody()) {
            byte[] bytes = body.getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().add("Content-Type", "application/json");
            exchange.sendResponseHeaders(status, bytes.length);
            out.write(bytes);
        } catch (Exception ignored) {
            // The caller has gone. There is nothing useful to do and nowhere
            // useful to say it.
        }
    }

    private static String env(String name, String fallback) {
        String value = System.getenv(name);
        return value == null || value.isBlank() ? fallback : value;
    }

    /**
     * Trust the provider's certificate, which {@code demo.sh} generated a few
     * seconds ago and which is signed by nobody.
     *
     * <p>This is the same compromise §41's nginx configuration makes with
     * {@code proxy_ssl_verify off}, and it is worth being explicit about: in
     * production this is where a trust store goes. The point that survives
     * either way is that it goes <i>here</i>, in the proxy, and not in the
     * service — which has no keystore, no trust store and no protocol list, and
     * did not acquire one when the proxy beside it changed language.
     */
    private static SSLContext trustingTheDemoCertificate() throws Exception {
        TrustManager[] trustAll = {new X509TrustManager() {
            public X509Certificate[] getAcceptedIssuers() {
                return new X509Certificate[0];
            }

            public void checkClientTrusted(X509Certificate[] chain, String authType) {
            }

            public void checkServerTrusted(X509Certificate[] chain, String authType) {
            }
        }};
        SSLContext context = SSLContext.getInstance("TLSv1.3");
        context.init(null, trustAll, new SecureRandom());
        return context;
    }

    /** What the provider said, on its way back to the service. */
    private record Answer(int status, String body) {
    }
}
