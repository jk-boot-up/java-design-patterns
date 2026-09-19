package com.jk.explore.discoveryconsul;

import java.util.Map;

public class DiscoveryApplication {

    public static void main(String[] args) throws Exception {
        if (!ConsulAgent.available()) {
            System.out.println("consul is not on the PATH, so there is nothing to discover with. Install it and run again.");
            return;
        }
        try (Cluster shop = new Cluster()) {
            System.out.println("ONE. Three copies announce themselves.");
            shop.start("pricing-1");
            shop.start("pricing-2", "10s");
            shop.start("pricing-3");
            shop.awaitListed(3);
            System.out.println("  the client was given the name pricing and no address.");
            System.out.println("  Consul lists: " + shop.listed() + ".");
            System.out.println("  nobody told Consul. each copy registered itself when it started.");

            System.out.println("TWO. Requests find them.");
            System.out.println("  six requests to http://pricing/...: " + shop.send(6) + ".");

            System.out.println("THREE. A deployment moves a copy.");
            String oldAddress = shop.baseUrl("pricing-1");
            shop.stop("pricing-1");
            shop.start("pricing-1");
            shop.awaitListed(3);
            System.out.println("  pricing-1 restarted on a new port.");
            try {
                shop.pricing.priceAt(oldAddress, "MUG-BLUE");
            } catch (RuntimeException e) {
                System.out.println("  a hardcoded address to pricing-1 now fails: " + e.getClass().getSimpleName() + ".");
            }
            System.out.println("  by name, six requests: " + shop.send(6) + ".");

            System.out.println("FOUR. A graceful stop is noticed at once.");
            shop.stop("pricing-3");
            System.out.println("  pricing-3 stopped. Consul lists, immediately: " + shop.listed() + ".");
            System.out.println("  six requests: " + shop.send(6) + ".");

            System.out.println("FIVE. A crash is not.");
            shop.crash("pricing-2");
            System.out.println("  pricing-2 crashed without a word. Consul lists, straight away: " + shop.listed() + ".");
            Map<String, Integer> during = shop.send(6);
            System.out.println("  six requests while the entry is stale: " + during + ".");
            boolean removed = shop.awaitListed(1);
            System.out.println("  after its health check fails, Consul lists: " + shop.listed() + " (removed: " + removed + ").");
            System.out.println("  six requests: " + shop.send(6) + ".");
            System.out.println("  the list is only as good as its last check. that is the taxi rank's catch.");

            System.out.println("SIX. The registry itself goes away.");
            shop.consul.close();
            try {
                shop.listed();
                System.out.println("  unexpectedly answered");
            } catch (RuntimeException e) {
                System.out.println("  Consul stopped. asking it for pricing: " + e.getClass().getSimpleName() + ".");
                System.out.println("  the client remembered nothing. a last-known-good list is the client's job.");
            }
        }
    }
}
