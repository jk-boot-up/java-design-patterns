package com.jk.explore.locatorconsul;

import com.jk.explore.locatorconsul.consul.Address;
import com.jk.explore.locatorconsul.consul.ConsulAgent;
import com.jk.explore.locatorconsul.consul.ConsulClient;
import com.jk.explore.locatorconsul.gateway.ServiceInstance;
import com.jk.explore.locatorconsul.nginx.NginxFront;
import com.jk.explore.locatorconsul.pattern.CachingLocator;
import com.jk.explore.locatorconsul.pattern.ConsulLocator;
import com.jk.explore.locatorconsul.pattern.Discovery;
import com.jk.explore.locatorconsul.pattern.LocatorCheckout;
import com.jk.explore.locatorconsul.pattern.NoHealthyInstance;

import java.net.http.HttpClient;
import java.util.List;

/**
 * Six acts, against a real Consul agent, real HTTP service instances, and, where
 * Docker is available, a real nginx container. Ports are chosen at run time and
 * never printed, so the output is the same every run.
 */
public final class ConsulDemo {

    public static void main(String[] args) throws Exception {
        System.out.println("SERVICE LOCATOR WITH CONSUL — real service discovery\n");
        if (!ConsulAgent.available()) {
            System.out.println("  the consul binary is not on the PATH, so this demo cannot run. install Consul and try again.");
            return;
        }
        try (ConsulAgent agent = ConsulAgent.start();
             ServiceInstance gateway1 = new ServiceInstance("gateway-1");
             ServiceInstance gateway2 = new ServiceInstance("gateway-2");
             ServiceInstance notifier = new ServiceInstance("notifier-1")) {
            ConsulClient consul = new ConsulClient(agent.baseUrl());
            consul.register("payment-gateway", "gateway-1", gateway1.port());
            consul.register("payment-gateway", "gateway-2", gateway2.port());
            consul.register("notifier", "notifier-1", notifier.port());
            actOne(consul, gateway1, gateway2);
            actTwo(consul, gateway1, gateway2);
            actThree(consul, gateway1, gateway2, notifier);
            actFour(consul, gateway1, gateway2);
            actFive(consul, gateway1, gateway2);
            actSix();
        }
    }

    private static void actOne(ConsulClient consul, ServiceInstance g1, ServiceInstance g2) {
        System.out.println("ONE. The locator asks Consul, and Consul answers with what is really running.");
        Discovery.use(new ConsulLocator(consul));
        System.out.println("  registered: two payment-gateway instances and one notifier, each a real HTTP server, each with a health check.");
        System.out.println("  healthy payment-gateway instances Consul reports: " + consul.healthy("payment-gateway").size());
        LocatorCheckout checkout = new LocatorCheckout();
        for (int i = 0; i < 4; i++) {
            checkout.place(10_000);
        }
        System.out.println("  four orders placed. served by gateway-1: " + g1.hits() + ", by gateway-2: " + g2.hits() + ".");
        System.out.println("  LocatorCheckout never knew an address. it asked for \"payment-gateway\" by name.\n");
    }

    private static void actTwo(ConsulClient consul, ServiceInstance g1, ServiceInstance g2) {
        System.out.println("TWO. The genuine advance: instances change and the caller's code does not.");
        int before1 = g1.hits();
        int before2 = g2.hits();
        consul.fail("gateway-1");
        System.out.println("  gateway-1's health check is marked failing. healthy instances now: " + consul.healthy("payment-gateway").size());
        LocatorCheckout checkout = new LocatorCheckout();
        for (int i = 0; i < 4; i++) {
            checkout.place(10_000);
        }
        System.out.println("  four more orders. gateway-1 served " + (g1.hits() - before1) + ", gateway-2 served " + (g2.hits() - before2) + ".");
        consul.pass("gateway-1");
        System.out.println("  gateway-1 recovers and is used again: healthy instances " + consul.healthy("payment-gateway").size() + ".");
        System.out.println("  no change to LocatorCheckout. this is what a registry with static entries could never do.\n");
    }

    private static void actThree(ConsulClient consul, ServiceInstance g1, ServiceInstance g2, ServiceInstance notifier) {
        System.out.println("THREE. The bill: the names are strings, and the compiler says nothing.");
        try {
            Discovery.find("payment-gatway");
        } catch (NoHealthyInstance e) {
            System.out.println("  a typo, \"payment-gatway\", compiled. at run time: " + e.getMessage());
        }
        consul.deregister("notifier-1");
        System.out.println("  the notifier's registration is lost, and nothing about LocatorCheckout says it needs one.");
        int before = g1.hits() + g2.hits();
        try {
            new LocatorCheckout().place(10_000);
        } catch (NoHealthyInstance e) {
            System.out.println("  then, on a real order: " + e.getMessage());
        }
        System.out.println("  and the payment gateway had already been called: " + (g1.hits() + g2.hits() - before) + " charge went through.");
        System.out.println("  the failure arrived in production, after the money moved. the same bill as the hand-built locator.\n");
        consul.register("notifier", "notifier-1", notifier.port());
    }

    private static void actFour(ConsulClient consul, ServiceInstance g1, ServiceInstance g2) {
        System.out.println("FOUR. The bill: a cached answer goes stale.");
        CachingLocator caching = new CachingLocator(consul);
        HttpClient http = HttpClient.newHttpClient();
        Address first = caching.find("payment-gateway");
        System.out.println("  a caching locator asked Consul once, and remembers the answer.");
        g1.stop();
        consul.fail("gateway-1");
        System.out.println("  gateway-1 dies, and Consul is told. the cache is not.");
        try {
            LocatorCheckout.call(http, caching.find("payment-gateway"), "/charge?pence=9000");
        } catch (IllegalStateException e) {
            System.out.println("  the cached address is still handed out, and the call fails: " + e.getMessage().replaceAll("127.0.0.1:\\d+", "the dead instance"));
        }
        System.out.println("  Consul was asked " + caching.timesConsulWasAsked() + " time in total. faster, and wrong.");
        Discovery.use(new ConsulLocator(consul));
        System.out.println("  the uncached locator recovers at once: " + LocatorCheckout.call(http, Discovery.find("payment-gateway"), "/charge?pence=9000").substring(0, 20));
        caching.refresh();
        System.out.println("  after a refresh the cache heals too. deciding when to refresh is now your problem.\n");
    }

    private static void actFive(ConsulClient consul, ServiceInstance g1, ServiceInstance g2) throws Exception {
        System.out.println("FIVE. The alternative: do not ask. be given.");
        if (!NginxFront.available()) {
            System.out.println("  (skipped: Docker is not running, or the nginx image is not available locally.)\n");
            return;
        }
        consul.pass("gateway-1");
        try (ServiceInstance fresh = new ServiceInstance("gateway-3")) {
            consul.register("payment-gateway", "gateway-3", fresh.port());
            List<Address> healthy = consul.healthy("payment-gateway").stream().filter(a -> a.port() != g1.port()).toList();
            try (NginxFront nginx = NginxFront.start(healthy)) {
                HttpClient http = HttpClient.newHttpClient();
                int g2Before = g2.hits();
                int g3Before = fresh.hits();
                int okBefore = 0;
                for (int i = 0; i < 4; i++) {
                    okBefore += send(http, nginx.url()) ? 1 : 0;
                }
                System.out.println("  nginx, in a Docker container, was given the healthy instances once, from Consul.");
                System.out.println("  the caller was given one address, nginx's, and asked nothing. " + okBefore + " of 4 requests succeeded.");
                System.out.println("  it spread them across the two instances: gateway-2 served " + (g2.hits() - g2Before)
                        + ", gateway-3 served " + (fresh.hits() - g3Before) + ".");
                int g3Mid = fresh.hits();
                g2.stop();
                int okAfter = 0;
                for (int i = 0; i < 4; i++) {
                    okAfter += send(http, nginx.url()) ? 1 : 0;
                }
                System.out.println("  gateway-2 is stopped. " + okAfter + " of 4 more requests still succeed: all " + (fresh.hits() - g3Mid)
                        + " were served by gateway-3, because nginx retried the next instance.");
                System.out.println("  the class never knew, because it never looked anything up.\n");
            }
        }
    }

    private static boolean send(HttpClient http, String url) {
        try {
            return http.send(java.net.http.HttpRequest.newBuilder(java.net.URI.create(url + "/charge?pence=9000")).build(),
                    java.net.http.HttpResponse.BodyHandlers.ofString()).statusCode() == 200;
        } catch (Exception e) {
            return false;
        }
    }

    private static void actSix() {
        System.out.println("SIX. The verdict.");
        System.out.println("  service discovery is the strongest case for a locator: where instances are is a run-time fact.");
        System.out.println("  even so, prefer to be given an address by the platform, a proxy or DNS, than to have every class ask.");
        System.out.println("  where you have met this: Spring Cloud's DiscoveryClient, Consul, Eureka, and Kubernetes DNS.");
    }
}
