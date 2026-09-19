package com.jk.explore.locatorconsul.consul;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * <strong>Consul's HTTP API, called directly.</strong> No client library: the
 * whole protocol needed here is a handful of PUT and GET calls. Each service is
 * registered with a TTL health check that this project passes or fails by hand,
 * so the outcome is immediate and deterministic.
 */
public class ConsulClient {

    private static final Pattern ADDRESS = Pattern.compile("\"Address\"\\s*:\\s*\"([^\"]*)\"");
    private static final Pattern PORT = Pattern.compile("\"Port\"\\s*:\\s*(\\d+)");

    private static final Pattern SERVICE_OBJECT = Pattern.compile("\"Service\"\\s*:\\s*\\{");

    private final String baseUrl;
    private final HttpClient http = HttpClient.newHttpClient();

    public ConsulClient(String baseUrl) {
        this.baseUrl = baseUrl;
    }

    public void register(String serviceName, String instanceId, int port) {
        String body = "{\"ID\":\"" + instanceId + "\",\"Name\":\"" + serviceName + "\",\"Address\":\"127.0.0.1\",\"Port\":" + port
                + ",\"Check\":{\"TTL\":\"1h\"}}";
        put("/v1/agent/service/register", body);
        pass(instanceId);
    }

    public void pass(String instanceId) {
        put("/v1/agent/check/pass/service:" + instanceId, "");
    }

    /** Marks an instance unhealthy: Consul stops returning it. */
    public void fail(String instanceId) {
        put("/v1/agent/check/fail/service:" + instanceId, "");
    }

    public void deregister(String instanceId) {
        put("/v1/agent/service/deregister/" + instanceId, "");
    }

    /** The instances of a service whose health checks are passing. */
    public List<Address> healthy(String serviceName) {
        String json = get("/v1/health/service/" + serviceName + "?passing");
        List<Address> found = new ArrayList<>();
        for (String entry : json.split("\"Node\"\\s*:\\s*\\{")) {
            Matcher service = SERVICE_OBJECT.matcher(entry);
            int checks = entry.indexOf("\"Checks\"");
            if (!service.find() || checks < service.start()) {
                continue;
            }
            String text = entry.substring(service.start(), checks);
            Matcher address = ADDRESS.matcher(text);
            Matcher port = PORT.matcher(text);
            if (address.find() && port.find()) {
                found.add(new Address(address.group(1), Integer.parseInt(port.group(1))));
            }
        }
        return found;
    }

    private void put(String path, String body) {
        try {
            HttpResponse<String> response = http.send(HttpRequest.newBuilder(URI.create(baseUrl + path))
                    .PUT(HttpRequest.BodyPublishers.ofString(body)).build(), HttpResponse.BodyHandlers.ofString());
            if (response.statusCode() != 200) {
                throw new IllegalStateException("consul " + path + " -> " + response.statusCode() + " " + response.body());
            }
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    private String get(String path) {
        try {
            return http.send(HttpRequest.newBuilder(URI.create(baseUrl + path)).build(), HttpResponse.BodyHandlers.ofString()).body();
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }
}
