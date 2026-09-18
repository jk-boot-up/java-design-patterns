package com.jk.explore.externalisedconfig.real.configserver;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

/**
 * The config source, as a running service.
 *
 * <p>In Tier 1 the {@code ConfigSource} interface was eleven lines of Java and
 * the value lived in a map. Here it is a separate process on its own port, and
 * the checkout service reaches it over HTTP. Nothing about the pattern has
 * changed: the value still lives outside the code that uses it, and the code
 * that uses it still reads it at the moment it needs it.
 *
 * <p>What has changed is the failure mode, and that is the point of running
 * this tier at all. A map cannot be unreachable. A service on port 8888 can,
 * and section "When the server is not there" in {@code real/README.md} walks
 * through what the checkout service does about it.
 *
 * <p>The whole server is this annotation. Everything else is configuration.
 */
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
