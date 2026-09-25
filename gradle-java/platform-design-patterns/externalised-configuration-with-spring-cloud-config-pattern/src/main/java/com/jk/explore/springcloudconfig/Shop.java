package com.jk.explore.springcloudconfig;

import com.jk.explore.springcloudconfig.shop.ShopApplication;
import java.util.LinkedHashMap;
import java.util.Map;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * One running copy of the shop, a Spring Boot web application on a port of its own.
 *
 * <p>The demo talks to it only over HTTP, the way a customer's browser would. The three ways of
 * starting it differ in one thing: what the shop should do at startup if the config server
 * cannot be reached.
 */
public final class Shop implements AutoCloseable {

    /** What the shop does at startup when the config server does not answer. */
    public enum WhenServerIsDown {
        /** {@code spring.cloud.config.fail-fast=true}: refuse to start. */
        REFUSE_TO_START,
        /** {@code optional:configserver:}: start anyway, on the shop's own defaults. */
        START_ON_LOCAL_DEFAULTS
    }

    private static final java.util.concurrent.atomic.AtomicInteger STARTED = new java.util.concurrent.atomic.AtomicInteger();
    private static final java.util.concurrent.atomic.AtomicInteger RUNNING = new java.util.concurrent.atomic.AtomicInteger();

    private final ConfigurableApplicationContext context;
    private final int port;

    private Shop(ConfigurableApplicationContext context, int port) {
        this.context = context;
        this.port = port;
    }

    /**
     * Starts a shop that fetches its settings from {@code configServerUrl}.
     *
     * @throws RuntimeException whatever Spring Boot throws if the shop refuses to start
     */
    public static Shop start(String configServerUrl, WhenServerIsDown whenDown) {
        int port = Http.freePort();
        Map<String, Object> p = new LinkedHashMap<>();
        p.put("server.port", port);
        p.put("spring.config.name", "shop");
        if (whenDown == WhenServerIsDown.REFUSE_TO_START) {
            p.put("spring.config.import", "configserver:" + configServerUrl);
            p.put("spring.cloud.config.fail-fast", "true");
        } else {
            p.put("spring.config.import", "optional:configserver:" + configServerUrl);
        }
        // The demo's printed lines are the lesson, so the shop's own log is switched off.
        p.put("spring.main.banner-mode", "off");
        p.put("spring.main.log-startup-info", "false");
        p.put("logging.level.root", "OFF");
        // The config server's library is on this program's class path too, because the demo
        // also starts the server. That library switches the config client off unless told
        // otherwise, so the shop says so explicitly.
        p.put("spring.cloud.config.enabled", "true");
        String[] args = p.entrySet().stream().map(e -> "--" + e.getKey() + "=" + e.getValue()).toArray(String[]::new);
        ConfigurableApplicationContext context = new SpringApplicationBuilder(ShopApplication.class).run(args);
        STARTED.incrementAndGet();
        RUNNING.incrementAndGet();
        return new Shop(context, port);
    }

    public String url() {
        return "http://localhost:" + port;
    }

    /** The delivery quote for a basket, one line of text. */
    public Http.Reply quote(String goods) {
        return Http.get(url() + "/quote?goods=" + goods);
    }

    /** The promotion banner across the top of the home page. */
    public String banner() {
        return Http.get(url() + "/banner").body();
    }

    /** {@code POST /actuator/refresh}: fetch the settings again, without a restart. */
    public Http.Reply refresh() {
        return Http.post(url() + "/actuator/refresh");
    }

    /** When this running copy of the shop started, in milliseconds since 1970. Unchanged means not restarted. */
    public long startedAt() {
        return context.getStartupDate();
    }

    /** How many copies of the shop this program has started, and how many are still running. */
    public static int started() {
        return STARTED.get();
    }

    public static int running() {
        return RUNNING.get();
    }

    @Override
    public void close() {
        if (context.isActive()) {
            context.close();
            RUNNING.decrementAndGet();
        }
    }
}
