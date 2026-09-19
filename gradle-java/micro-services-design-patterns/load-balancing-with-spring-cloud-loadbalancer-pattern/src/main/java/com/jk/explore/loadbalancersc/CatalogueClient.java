package com.jk.explore.loadbalancersc;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestClient;

/** Calls a service by its logical name; the load balancer turns the name into an address per request. */
@Service
public class CatalogueClient {

    private final RestClient.Builder builder;

    public CatalogueClient(RestClient.Builder loadBalancedBuilder) {
        this.builder = loadBalancedBuilder;
    }

    public String get(String service, String path) {
        return builder.build().get().uri("http://" + service + path).retrieve().body(String.class);
    }
}
