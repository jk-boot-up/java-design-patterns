package com.jk.explore.meshenvoy;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;

/** A real Envoy proxy in a Docker container, in front of the payment service. The policy is its configuration. */
public class Envoy implements AutoCloseable {

    public static final String IMAGE = "envoyproxy/envoy:v1.37-latest";
    public static final int LISTEN = 10000;
    public static final int ADMIN = 9901;
    private static final String CONTAINER = "patterns-envoy";

    private final int paymentsPort;
    private Path config;

    public Envoy(int paymentsPort) {
        this.paymentsPort = paymentsPort;
    }

    public static boolean toolsAvailable() {
        return Shell.works("docker", "info") && Shell.works("docker", "image", "inspect", IMAGE) || Shell.works("docker", "info") && Shell.works("docker", "pull", "-q", IMAGE);
    }

    /** The whole policy, as Envoy reads it: how many retries, and who may call. */
    static String configuration(int paymentsPort, int retries, List<String> allowedCallers) {
        StringBuilder rbac = new StringBuilder();
        if (!allowedCallers.isEmpty()) {
            rbac.append("          - name: envoy.filters.http.rbac\n")
                .append("            typed_config:\n")
                .append("              \"@type\": type.googleapis.com/envoy.extensions.filters.http.rbac.v3.RBAC\n")
                .append("              rules:\n                action: ALLOW\n                policies:\n                  callers:\n")
                .append("                    permissions: [{any: true}]\n                    principals:\n");
            for (String c : allowedCallers) {
                rbac.append("                      - header: {name: x-caller, string_match: {exact: ").append(c).append("}}\n");
            }
        }
        return """
                static_resources:
                  listeners:
                  - name: ingress
                    address: {socket_address: {address: 0.0.0.0, port_value: %d}}
                    filter_chains:
                    - filters:
                      - name: envoy.filters.network.http_connection_manager
                        typed_config:
                          "@type": type.googleapis.com/envoy.extensions.filters.network.http_connection_manager.v3.HttpConnectionManager
                          stat_prefix: ingress
                          route_config:
                            name: routes
                            virtual_hosts:
                            - name: payments
                              domains: ["*"]
                              routes:
                              - match: {prefix: "/"}
                                route:
                                  cluster: payments
                                  retry_policy: {retry_on: "5xx", num_retries: %d, per_try_timeout: 2s}
                          http_filters:
                %s          - name: envoy.filters.http.router
                            typed_config:
                              "@type": type.googleapis.com/envoy.extensions.filters.http.router.v3.Router
                  clusters:
                  - name: payments
                    type: STRICT_DNS
                    connect_timeout: 2s
                    load_assignment:
                      cluster_name: payments
                      endpoints:
                      - lb_endpoints:
                        - endpoint: {address: {socket_address: {address: host.docker.internal, port_value: %d}}}
                admin:
                  address: {socket_address: {address: 0.0.0.0, port_value: %d}}
                """.formatted(LISTEN, retries, rbac, paymentsPort, ADMIN);
    }

    /** Starts Envoy with this policy, replacing any earlier one. Returns when Envoy answers on its admin port. */
    public void start(int retries, List<String> allowedCallers) throws IOException {
        stop();
        config = Files.createTempFile("envoy", ".yaml");
        Files.writeString(config, configuration(paymentsPort, retries, allowedCallers));
        Shell.run("docker", "run", "-d", "--rm", "--name", CONTAINER,
                "-p", "127.0.0.1:" + LISTEN + ":" + LISTEN, "-p", "127.0.0.1:" + ADMIN + ":" + ADMIN,
                "-v", config + ":/etc/envoy/envoy.yaml:ro", IMAGE, "-c", "/etc/envoy/envoy.yaml", "--log-level", "warn");
        long end = System.nanoTime() + 60_000_000_000L;
        while (System.nanoTime() < end) {
            if (stats().contains("server.live: 1")) {
                return;
            }
            try {
                Thread.sleep(200);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("Envoy did not come up: " + Shell.run("docker", "logs", CONTAINER));
    }

    public void stop() {
        Shell.works("docker", "rm", "-f", CONTAINER);
    }

    public String url() {
        return "http://127.0.0.1:" + LISTEN + "/charge";
    }

    /** The proxy's own counters, as text. */
    public String stats() {
        try (HttpClient client = HttpClient.newBuilder().connectTimeout(java.time.Duration.ofSeconds(1)).build()) {
            return client.send(HttpRequest.newBuilder(URI.create("http://127.0.0.1:" + ADMIN + "/stats")).timeout(java.time.Duration.ofSeconds(2)).build(),
                    HttpResponse.BodyHandlers.ofString()).body();
        } catch (Exception e) {
            return "";
        }
    }

    /** One counter, such as cluster.payments.upstream_rq_retry. */
    public long counter(String name) {
        for (String line : stats().split("\n")) {
            if (line.startsWith(name + ": ")) {
                return Long.parseLong(line.substring(name.length() + 2).trim());
            }
        }
        return 0;
    }

    @Override
    public void close() {
        stop();
    }
}
