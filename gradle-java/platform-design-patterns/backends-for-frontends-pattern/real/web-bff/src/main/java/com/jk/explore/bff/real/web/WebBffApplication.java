package com.jk.explore.bff.real.web;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;

/**
 * The desktop store's backend, as a service of its own on port 8081.
 *
 * <p>Owned by the desktop team. Same shop behind it, same five services, a different
 * answer — and both of these processes are running at the same time, on purpose,
 * neither one a fallback for the other.
 */
@SpringBootApplication
public class WebBffApplication {

    public static void main(String[] args) {
        SpringApplication.run(WebBffApplication.class, args);
    }

    @Bean
    RestClient shopClient(RestClient.Builder builder, @Value("${shop.base-url}") String baseUrl) {
        return builder.baseUrl(baseUrl).build();
    }
}
