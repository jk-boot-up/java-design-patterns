package com.jk.explore.loadbalancersc;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.cloud.client.loadbalancer.LoadBalanced;
import org.springframework.cloud.loadbalancer.annotation.LoadBalancerClient;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.annotation.Bean;
import org.springframework.web.client.RestClient;

import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
@LoadBalancerClient(name = "catalogue-fast", configuration = LeastWorkConfiguration.class)
public class CatalogueApplication {

    @Bean
    @LoadBalanced
    RestClient.Builder loadBalancedRestClientBuilder() {
        return RestClient.builder();
    }

    /** Three copies of the catalogue: two fast, one on older hardware, and the client that finds them. */
    static final class Cluster implements AutoCloseable {
        final List<Backend> copies = List.of(new Backend("copy-a", 1), new Backend("copy-b", 1), new Backend("copy-c", 6));
        final ConfigurableApplicationContext context;
        final CatalogueClient client;

        Cluster() {
            List<String> properties = new ArrayList<>();
            for (int i = 0; i < copies.size(); i++) {
                for (String service : new String[]{"catalogue", "catalogue-fast"}) {
                    String prefix = "spring.cloud.discovery.client.simple.instances." + service + "[" + i + "].";
                    properties.add(prefix + "uri=http://127.0.0.1:" + copies.get(i).port());
                    properties.add(prefix + "metadata.cost=" + copies.get(i).cost());
                }
            }
            context = new SpringApplicationBuilder(CatalogueApplication.class)
                    .web(WebApplicationType.NONE)
                    .properties(properties.toArray(String[]::new))
                    .run();
            client = context.getBean(CatalogueClient.class);
        }

        String hits() {
            return copies.stream().map(c -> String.valueOf(c.hits())).toList().toString();
        }

        String work() {
            return copies.stream().map(c -> String.valueOf(c.work())).toList().toString();
        }

        @Override
        public void close() {
            context.close();
            copies.forEach(Backend::close);
        }
    }

    public static void main(String[] args) {
        System.out.println("ONE. Twelve requests, one logical name.");
        try (Cluster cluster = new Cluster()) {
            for (int i = 0; i < 12; i++) {
                cluster.client.get("catalogue", "/products/MUG-BLUE");
            }
            System.out.println("  requests answered by copy-a, copy-b, copy-c: " + cluster.hits() + ".");
            System.out.println("  the caller wrote http://catalogue/... and never saw an address. the default is round robin.");

            System.out.println("TWO. Fair is not fast.");
            System.out.println("  work done, counting the old machine as six times a fast one: " + cluster.work() + ".");
            System.out.println("  the slow copy did the most work, because round robin gives every copy the same number of requests.");
        }

        System.out.println("THREE. A strategy of our own.");
        try (Cluster cluster = new Cluster()) {
            for (int i = 0; i < 12; i++) {
                cluster.client.get("catalogue-fast", "/products/MUG-BLUE");
            }
            System.out.println("  least work so far, twelve requests: " + cluster.hits() + ". work done: " + cluster.work() + ".");
            System.out.println("  registered for one service name, catalogue-fast. the name catalogue still uses round robin.");
        }

        System.out.println("FOUR. A copy goes down.");
        try (Cluster cluster = new Cluster()) {
            cluster.copies.get(1).goDown();
            int failures = 0;
            for (int i = 0; i < 12; i++) {
                try {
                    cluster.client.get("catalogue", "/products/MUG-BLUE");
                } catch (RuntimeException e) {
                    failures++;
                }
            }
            System.out.println("  copy-b is stopped. 12 requests: " + failures + " failed, " + (12 - failures) + " answered.");
            System.out.println("  the list still holds copy-b, so a third of the requests are sent to it.");

            System.out.println("FIVE. A retry lands somewhere else.");
            int recovered = 0;
            int attempts = 0;
            for (int i = 0; i < 12; i++) {
                for (int attempt = 0; attempt < 2; attempt++) {
                    attempts++;
                    try {
                        cluster.client.get("catalogue", "/products/MUG-BLUE");
                        recovered++;
                        break;
                    } catch (RuntimeException e) {
                        // try again: the balancer moves on to the next copy
                    }
                }
            }
            System.out.println("  the same 12 requests, each allowed one retry: " + recovered + " answered. some needed a second attempt: " + (attempts > 12) + ".");
            System.out.println("  the retry is the caller's, and a balancer without health checks only spreads the failures.");
        }

        System.out.println("SIX. Only for names.");
        try (Cluster cluster = new Cluster()) {
            try {
                cluster.client.get("checkout", "/health");
            } catch (RuntimeException e) {
                System.out.println("  a name the balancer has no instances for: " + e.getClass().getSimpleName() + ".");
            }
            try {
                cluster.client.get("127.0.0.1:" + cluster.copies.get(0).port(), "/products/MUG-BLUE");
            } catch (RuntimeException e) {
                System.out.println("  a real address on a load-balanced client: " + e.getClass().getSimpleName() + ".");
            }
            System.out.println("  a load-balanced client treats every host as a service name.");
        }
    }
}
