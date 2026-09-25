package com.jk.explore.springcloudconfig;

import com.jk.explore.springcloudconfig.server.ConfigServerApplication;
import java.nio.file.Path;
import java.time.Duration;
import java.util.List;

/**
 * The config server, running as a separate Java program that this demo starts and stops.
 *
 * <p>It is a second process on purpose. The settings then really do live outside the shop: the
 * shop fetches them over HTTP, and the server can be stopped while the shop keeps running,
 * which is one of the things the demo shows.
 */
public final class ConfigServerProcess implements AutoCloseable {

    private static final Duration START_LIMIT = Duration.ofSeconds(90);

    private final int port;
    private final Path log;
    private Process process;

    private ConfigServerProcess(int port, Path log) {
        this.port = port;
        this.log = log;
    }

    /**
     * Starts the server against a git repository and waits until it says it is healthy.
     *
     * @param repositoryUri the repository to serve, a file URL
     * @param workFolder    a folder for the server's clone of the repository and its log
     */
    public static ConfigServerProcess start(String repositoryUri, Path workFolder) {
        ConfigServerProcess server = new ConfigServerProcess(Http.freePort(), workFolder.resolve("config-server.log"));
        server.launch(repositoryUri, workFolder.resolve("clone"));
        return server;
    }

    private void launch(String repositoryUri, Path cloneFolder) {
        String java = ProcessHandle.current().info().command().orElse("java");
        List<String> command = List.of(
                java,
                "-Xmx256m",
                "-cp", System.getProperty("java.class.path"),
                ConfigServerApplication.class.getName(),
                "--server.port=" + port,
                "--spring.config.name=config-server",
                "--logging.level.root=INFO",
                "--spring.cloud.config.server.git.uri=" + repositoryUri,
                "--spring.cloud.config.server.git.basedir=" + cloneFolder);
        try {
            process = new ProcessBuilder(command)
                    .redirectErrorStream(true)
                    .redirectOutput(log.toFile())
                    .start();
        } catch (java.io.IOException e) {
            throw new IllegalStateException("could not start the config server", e);
        }
        Runtime.getRuntime().addShutdownHook(new Thread(this::close));
        Poll.until("the config server to report itself healthy", START_LIMIT,
                () -> !process.isAlive() || Http.get(url() + "/actuator/health").body().contains("\"UP\""));
        if (!process.isAlive()) {
            throw new IllegalStateException("the config server stopped as it started; its log is " + log);
        }
    }

    public int port() {
        return port;
    }

    public String url() {
        return "http://localhost:" + port;
    }

    /** What the server would send an application with this name and profile, as JSON. */
    public String settingsFor(String application, String profile) {
        return Http.get(url() + "/" + application + "/" + profile).body();
    }

    public boolean running() {
        return process != null && process.isAlive();
    }

    /** Stops the process and waits until it has gone. */
    @Override
    public void close() {
        if (process == null) {
            return;
        }
        process.destroy();
        try {
            if (!process.waitFor(20, java.util.concurrent.TimeUnit.SECONDS)) {
                process.destroyForcibly().waitFor();
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
