package com.jk.explore.springcloudconfig.server;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.config.server.EnableConfigServer;

/**
 * The config server, the whole of it.
 *
 * <p>It is a separate program. The demo starts it as a second Java process, on a port of its
 * own, and the shop reaches it only over HTTP. It reads a git repository, and when an
 * application asks "what are my settings?", it answers with the file named after that
 * application, as it stands in the newest commit.
 *
 * <p>The one annotation, {@code @EnableConfigServer}, is all the code there is. Everything else
 * is the settings in {@code config-server.yml}, and the repository address the demo passes in.
 */
@SpringBootApplication
@EnableConfigServer
public class ConfigServerApplication {

    public static void main(String[] args) {
        SpringApplication.run(ConfigServerApplication.class, args);
    }
}
