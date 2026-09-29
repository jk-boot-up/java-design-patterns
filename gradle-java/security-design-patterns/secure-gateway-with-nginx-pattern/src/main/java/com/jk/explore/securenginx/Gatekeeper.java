package com.jk.explore.securenginx;

import org.testcontainers.DockerClientFactory;
import org.testcontainers.Testcontainers;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.images.builder.Transferable;
import org.testcontainers.utility.DockerImageName;

/**
 * The gatekeeper: a real NGINX in a container, the only thing the "internet" talks to. It holds no
 * secrets. Its whole policy is the configuration file below.
 */
public final class Gatekeeper implements AutoCloseable {

    public static final String IMAGE = "nginx:1.31.6-alpine";
    static final int PORT = 8080;

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real NGINX as the gatekeeper.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The NGINX container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    /** The allow-list. Anything not matched by one of the two order locations falls to "return 404". */
    static String config(int orderServicePort) {
        String upstream = "http://host.testcontainers.internal:" + orderServicePort;
        return """
                events {}
                http {
                    client_max_body_size 1m;                     # bigger bodies: 413
                    server {
                        listen %d;
                        location = /health { return 200 "ok"; }
                        location ~ "^/orders/[0-9]{1,9}$" {      # GET an order by its number
                            limit_except GET { deny all; }        # any other method: 403
                            proxy_set_header X-Internal-Admin ""; # an empty value removes the header
                            proxy_pass %s;
                        }
                        location = /orders {                      # POST a new order
                            limit_except POST { deny all; }
                            proxy_set_header X-Internal-Admin "";
                            proxy_pass %s;
                        }
                        location / { return 404; }                # everything else
                    }
                }
                """.formatted(PORT, upstream, upstream);
    }

    private final GenericContainer<?> container;
    private final int orderServicePort;

    public Gatekeeper(int orderServicePort) {
        this.orderServicePort = orderServicePort;
        this.container = new GenericContainer<>(DockerImageName.parse(IMAGE))
                .withExposedPorts(PORT)
                .withCopyToContainer(Transferable.of(config(orderServicePort)), "/etc/nginx/nginx.conf")
                .waitingFor(Wait.forHttp("/health").forPort(PORT).forStatusCode(200));
    }

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        Testcontainers.exposeHostPorts(orderServicePort);   // lets NGINX reach the service on this machine
        container.start();
    }

    public String url() {
        return "http://" + container.getHost() + ":" + container.getMappedPort(PORT);
    }

    /** Whether anything in the gatekeeper's environment mentions a password. */
    public boolean holdsCredentials() throws Exception {
        String env = container.execInContainer("env").getStdout();
        return env.toLowerCase().contains("password") || env.contains(OrderService.DATABASE_PASSWORD);
    }

    @Override
    public void close() {
        container.stop();
    }
}
