package com.jk.explore.locatorconsul.nginx;

import com.jk.explore.locatorconsul.consul.Address;

import java.io.IOException;
import java.net.ServerSocket;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.concurrent.TimeUnit;
import java.util.stream.Collectors;

/**
 * <strong>Server-side discovery: nginx in a Docker container, in front of the instances.</strong>
 * The caller is given one address and never asks anything. The upstream list is
 * written from what Consul reported healthy. It reaches the host through
 * {@code host.docker.internal}, which Docker Desktop provides. On Linux the
 * container would also need {@code --add-host host.docker.internal:host-gateway}. This is the alternative to a
 * locator: the class does not look anything up.
 */
public final class NginxFront implements AutoCloseable {

    private static final String IMAGE = "nginx:1.31.5-alpine";
    private static final String NAME = "locator-demo-nginx";

    private final int port;
    private final Path config;

    private NginxFront(int port, Path config) {
        this.port = port;
        this.config = config;
    }

    /** True when Docker is running and the nginx image is available locally. */
    public static boolean available() {
        return run("docker", "image", "inspect", IMAGE) == 0;
    }

    public static NginxFront start(List<Address> upstreams) throws IOException {
        int port;
        try (ServerSocket s = new ServerSocket(0)) {
            port = s.getLocalPort();
        }
        String servers = upstreams.stream().map(a -> "        server host.docker.internal:" + a.port() + ";")
                .collect(Collectors.joining("\n"));
        Path conf = Files.createTempFile("locator-demo-nginx", ".conf");
        Files.writeString(conf, """
                events {}
                http {
                    upstream gateways {
                %s
                    }
                    server {
                        listen 80;
                        location = /nginx-ready {
                            return 200 "ok";
                        }
                        location / {
                            proxy_pass http://gateways;
                            proxy_connect_timeout 1s;
                            proxy_next_upstream error timeout;
                        }
                    }
                }
                """.formatted(servers));
        run("docker", "rm", "-f", NAME);
        int code = run("docker", "run", "-d", "--rm", "--name", NAME,
                "-p", "127.0.0.1:" + port + ":80", "-v", conf + ":/etc/nginx/nginx.conf:ro", IMAGE);
        if (code != 0) {
            throw new IllegalStateException("could not start the nginx container");
        }
        NginxFront front = new NginxFront(port, conf);
        front.awaitReady();
        return front;
    }

    public String url() {
        return "http://127.0.0.1:" + port;
    }

    /** Ready means nginx itself answered an HTTP request. A published port accepts connections before nginx is up. */
    private void awaitReady() {
        java.net.http.HttpClient http = java.net.http.HttpClient.newHttpClient();
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(20);
        while (System.nanoTime() < deadline) {
            try {
                var response = http.send(java.net.http.HttpRequest.newBuilder(java.net.URI.create(url() + "/nginx-ready")).build(),
                        java.net.http.HttpResponse.BodyHandlers.ofString());
                if (response.statusCode() == 200) {
                    return;
                }
            } catch (IOException e) {
                // not answering yet
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
            try {
                Thread.sleep(100);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        close();
        throw new IllegalStateException("nginx did not come up in time");
    }

    private static int run(String... command) {
        try {
            Process p = new ProcessBuilder(command).redirectErrorStream(true).start();
            p.getInputStream().readAllBytes();
            return p.waitFor(60, TimeUnit.SECONDS) ? p.exitValue() : -1;
        } catch (IOException e) {
            return -1;
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return -1;
        }
    }

    @Override
    public void close() {
        run("docker", "rm", "-f", NAME);
        try {
            Files.deleteIfExists(config);
        } catch (IOException ignored) {
            // a temporary file
        }
    }
}
