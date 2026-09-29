package com.jk.explore.pageobjectselenium;

import java.net.URI;
import java.net.URL;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.chrome.ChromeOptions;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.Testcontainers;
import org.testcontainers.containers.GenericContainer;
import org.testcontainers.containers.wait.strategy.Wait;

/**
 * A real Chromium browser with a WebDriver server, in a container that this demo starts and stops.
 */
public final class Browser implements AutoCloseable {

    public static final String IMAGE = "selenium/standalone-chromium:152.0";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts a real Chromium browser in a container.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The browser container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final GenericContainer<?> container = new GenericContainer<>(IMAGE)
            .withExposedPorts(4444)
            .withSharedMemorySize(2L * 1024 * 1024 * 1024)
            .waitingFor(Wait.forHttp("/status").forPort(4444).forStatusCode(200));
    private final int sitePort;

    public Browser(int sitePort) {
        this.sitePort = sitePort;
    }

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        Testcontainers.exposeHostPorts(sitePort);   // lets the browser reach the shop's pages on this machine
        container.start();
    }

    /** A fresh browser session, as each test would have. */
    public WebDriver newSession() throws Exception {
        URL hub = URI.create("http://" + container.getHost() + ":" + container.getMappedPort(4444) + "/wd/hub").toURL();
        return new RemoteWebDriver(hub, new ChromeOptions());
    }

    public String checkoutUrl() {
        return "http://host.testcontainers.internal:" + sitePort + "/checkout";
    }

    @Override
    public void close() {
        container.stop();
    }
}
