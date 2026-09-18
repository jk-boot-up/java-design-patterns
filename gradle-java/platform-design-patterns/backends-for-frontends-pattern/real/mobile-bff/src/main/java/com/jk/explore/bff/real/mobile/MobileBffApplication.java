package com.jk.explore.bff.real.mobile;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;

/**
 * The phone's backend, as a service of its own on port 8080.
 *
 * <p>Owned by the phone team. Its repository, its pipeline, its release. That sentence
 * is the pattern and it is also the thing a single-process demonstration can only
 * assert — here it is a separate process with a separate address, which is as close as
 * a repository can get to it.
 */
@SpringBootApplication
public class MobileBffApplication {

    public static void main(String[] args) {
        SpringApplication.run(MobileBffApplication.class, args);
    }

    /**
     * The client this backend uses to reach the shop.
     *
     * <p>The base URL is configuration rather than a constant because the shop's
     * address is not this team's business; everything else about what gets asked for,
     * and what is done with the answer, is.
     */
    @Bean
    RestClient shopClient(RestClient.Builder builder, @Value("${shop.base-url}") String baseUrl) {
        return builder.baseUrl(baseUrl).build();
    }
}
