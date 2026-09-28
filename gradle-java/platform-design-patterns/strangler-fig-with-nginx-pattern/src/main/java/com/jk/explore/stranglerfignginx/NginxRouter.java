package com.jk.explore.stranglerfignginx;

import java.util.Arrays;
import java.util.List;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.Testcontainers;
import org.testcontainers.containers.Container;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;
import org.testcontainers.images.builder.Transferable;
import org.testcontainers.utility.DockerImageName;

/**
 * A real NGINX, running in a container that this demo starts and stops itself. It is the
 * strangler: the one public address the customer uses, deciding route by route whether the
 * old shop or the new service answers.
 *
 * <p>The two services run inside this Java program, on this machine. Testcontainers opens a
 * way from the container back to this machine, and NGINX reaches both services through the
 * name {@code host.testcontainers.internal}.
 */
public class NginxRouter implements AutoCloseable {

    /** NGINX 1.31.6 on Alpine Linux, the newest release at the time this project was written. */
    public static final String IMAGE = "nginx:1.31.6-alpine";

    private static final int PORT = 8080;
    private static final String CONF = "/etc/nginx/nginx.conf";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real NGINX.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but NGINX will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The NGINX container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final int oldShopPort;
    private final int newServicePort;
    private final GenericContainer<?> container;
    private int generation = 1;
    private NginxConfig current;

    public NginxRouter(int oldShopPort, int newServicePort) {
        this.oldShopPort = oldShopPort;
        this.newServicePort = newServicePort;
        this.current = NginxConfig.everythingOnTheOldShop();
        // NGINX starts with every route on the old shop. Its own configuration file is
        // replaced by the demo's before it starts, so nothing from the image's default is used.
        this.container = new GenericContainer<>(DockerImageName.parse(IMAGE))
                .withExposedPorts(PORT)
                .withCopyToContainer(Transferable.of(current.render(generation, oldShopPort, newServicePort)), CONF)
                .waitingFor(Wait.forHttp("/router/generation").forStatusCode(200));
    }

    /**
     * True when there is a container runtime this demo can use. Checked before anything
     * starts, so a machine without one gets a sentence rather than a stack trace.
     */
    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        // Lets the container reach the two services on this machine. Must happen before start.
        Testcontainers.exposeHostPorts(oldShopPort, newServicePort);
        container.start();
    }

    /** The shop's one public address: NGINX, on a free random port on this machine. */
    public String address() {
        return "http://" + container.getHost() + ":" + container.getMappedPort(PORT);
    }

    public NginxConfig current() {
        return current;
    }

    public String version() {
        String out = exec("nginx", "-v");
        return out.substring(out.indexOf('/') + 1).trim();
    }

    /**
     * Writes a new configuration into the container, checks it with {@code nginx -t}, and
     * tells NGINX to reload with {@code nginx -s reload}.
     *
     * <p>A reload is not instant, and for a moment it is not tidy either. NGINX's main process
     * starts a new worker with the new configuration, and only then tells the old worker to
     * stop taking connections. In between, both workers take new connections, so a request can
     * still be answered under the old configuration after the new one has already answered
     * another. This method returns only when both things are true: NGINX answers with the new
     * configuration's generation number, and exactly one worker is taking new connections.
     */
    public void apply(NginxConfig config) {
        int next = generation + 1;
        container.copyFileToContainer(
                Transferable.of(config.render(next, oldShopPort, newServicePort)), CONF);
        execOrFail("nginx", "-t");
        execOrFail("nginx", "-s", "reload");
        Browser probe = new Browser(address());
        Poll.until("NGINX to answer with configuration generation " + next
                        + ", with only the new worker taking connections",
                () -> probe.get("/router/generation").body().equals(Integer.toString(next))
                        && workersTakingNewRequests() == 1);
        generation = next;
        current = config;
    }

    /** The process number of NGINX's main process, the one that reads the configuration. */
    public int mainProcessId() {
        return processes().stream()
                .filter(line -> line.contains("nginx: master process"))
                .map(line -> Integer.parseInt(line.trim().split("\\s+")[0]))
                .findFirst()
                .orElseThrow(() -> new IllegalStateException("no NGINX main process: " + processes()));
    }

    /** Worker processes that belong to an old configuration and are finishing their requests. */
    public int workersStillFinishing() {
        return (int) processes().stream().filter(line -> line.contains("worker process is shutting down")).count();
    }

    /** Worker processes taking new requests. */
    public int workersTakingNewRequests() {
        return (int) processes().stream()
                .filter(line -> line.contains("nginx: worker process") && !line.contains("shutting down"))
                .count();
    }

    public List<String> processes() {
        return Arrays.stream(exec("ps", "-o", "pid,args").split("\n")).skip(1).toList();
    }

    private String execOrFail(String... command) {
        try {
            Container.ExecResult result = container.execInContainer(command);
            if (result.getExitCode() != 0) {
                throw new IllegalStateException(String.join(" ", command) + " failed: " + result.getStderr());
            }
            return result.getStdout() + result.getStderr();
        } catch (RuntimeException e) {
            throw e;
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    private String exec(String... command) {
        return execOrFail(command);
    }

    @Override
    public void close() {
        container.stop();
    }
}
