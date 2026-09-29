package com.jk.explore.secretsopenbao;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;

/**
 * A real OpenBao server, the open-source fork of HashiCorp Vault, in a container that this demo starts
 * and stops itself. It runs in development mode: unsealed, in memory, with a known root token.
 */
public final class OpenBao implements AutoCloseable {

    public static final String IMAGE = "openbao/openbao:2.7.0";
    public static final String ROOT = "root-token-for-the-demo-only";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real OpenBao secrets server.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The OpenBao container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final GenericContainer<?> container = new GenericContainer<>(IMAGE)
            .withExposedPorts(8200)
            .withEnv("BAO_DEV_ROOT_TOKEN_ID", ROOT)
            .withEnv("BAO_DEV_LISTEN_ADDRESS", "0.0.0.0:8200")
            .withCommand("server", "-dev")
            .waitingFor(Wait.forHttp("/v1/sys/health").forPort(8200).forStatusCode(200));
    private final HttpClient http = HttpClient.newHttpClient();

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
    }

    /** One HTTP call to OpenBao's API. Returns the status code and the JSON body. */
    public Reply call(String method, String path, String token, String json) throws Exception {
        HttpRequest.Builder r = HttpRequest.newBuilder(
                        URI.create("http://" + container.getHost() + ":" + container.getMappedPort(8200) + "/v1/" + path))
                .header("X-Vault-Token", token);
        r.method(method, json == null ? HttpRequest.BodyPublishers.noBody() : HttpRequest.BodyPublishers.ofString(json));
        HttpResponse<String> response = http.send(r.build(), HttpResponse.BodyHandlers.ofString());
        return new Reply(response.statusCode(), response.body());
    }

    /** A status code and a JSON body, with a tiny helper to read one field. */
    public record Reply(int status, String body) {

        public String field(String name) {
            Matcher m = Pattern.compile("\"" + name + "\":\\s*\"?([^\",}]*)").matcher(body);
            return m.find() ? m.group(1) : null;
        }
    }

    @Override
    public void close() {
        container.stop();
    }
}
