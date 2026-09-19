package com.jk.explore.discoveryconsul;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.concurrent.TimeUnit;

/**
 * <strong>A real Consul agent, run as a local process in development mode.</strong>
 * Nothing is simulated: this is the actual {@code consul} binary. It picks free
 * ports for everything it listens on, so it cannot clash with another agent,
 * and it is stopped when closed. It needs {@code consul} on the PATH.
 */
public final class ConsulAgent implements AutoCloseable {

    private final Process process;
    private final int httpPort;

    private ConsulAgent(Process process, int httpPort) {
        this.process = process;
        this.httpPort = httpPort;
    }

    /** True when a {@code consul} binary can be run. */
    public static boolean available() {
        try {
            Process p = new ProcessBuilder("consul", "version").redirectErrorStream(true).start();
            p.getInputStream().readAllBytes();
            return p.waitFor(10, TimeUnit.SECONDS) && p.exitValue() == 0;
        } catch (IOException | InterruptedException e) {
            return false;
        }
    }

    public static ConsulAgent start() throws IOException, InterruptedException {
        int http = freePort();
        Process process = new ProcessBuilder("consul", "agent", "-dev", "-node=discovery-demo",
                "-bind=127.0.0.1", "-client=127.0.0.1", "-http-port=" + http, "-dns-port=-1", "-grpc-port=-1",
                "-server-port=" + freePort(), "-serf-lan-port=" + freePort(), "-serf-wan-port=" + freePort(),
                "-log-level=error")
                .redirectErrorStream(true).redirectOutput(ProcessBuilder.Redirect.DISCARD).start();
        ConsulAgent agent = new ConsulAgent(process, http);
        agent.awaitLeader();
        return agent;
    }

    public String baseUrl() {
        return "http://127.0.0.1:" + httpPort;
    }

    private void awaitLeader() throws InterruptedException {
        HttpClient http = HttpClient.newHttpClient();
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(20);
        while (System.nanoTime() < deadline) {
            try {
                String leader = http.send(HttpRequest.newBuilder(URI.create(baseUrl() + "/v1/status/leader")).build(),
                        HttpResponse.BodyHandlers.ofString()).body();
                if (leader.length() > 2) {
                    return;
                }
            } catch (IOException e) {
                // not up yet
            }
            Thread.sleep(100);
        }
        close();
        throw new IllegalStateException("consul did not elect a leader in time");
    }

    private static int freePort() throws IOException {
        try (ServerSocket s = new ServerSocket(0)) {
            return s.getLocalPort();
        }
    }

    @Override
    public void close() {
        process.destroy();
        try {
            process.waitFor(10, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
