package com.jk.explore.discoveryconsul.client;

import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;

/** The caller. It is told a service name, never an address, and does not register itself. */
@SpringBootApplication
public class ClientApplication {

    @Bean
    @LoadBalanced
    RestClient.Builder loadBalancedBuilder() {
        return RestClient.builder();
    }

    @Bean
    PricingClient pricingClient(RestClient.Builder builder) {
        return new PricingClient(builder);
    }
}
