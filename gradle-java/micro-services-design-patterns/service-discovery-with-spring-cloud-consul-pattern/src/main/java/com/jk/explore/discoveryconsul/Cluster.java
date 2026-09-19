package com.jk.explore.discoveryconsul;

import com.jk.explore.discoveryconsul.client.ClientApplication;
import com.jk.explore.discoveryconsul.client.PricingClient;
import com.jk.explore.discoveryconsul.instance.PricingInstance;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.boot.web.server.context.WebServerApplicationContext;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.discovery.DiscoveryClient;
import org.springframework.context.ConfigurableApplicationContext;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import java.util.concurrent.TimeUnit;

/** A real Consul agent, copies of Pricing that register with it, and a client that only knows a name. */
final class Cluster implements AutoCloseable {

    final ConsulAgent consul;
    final Map<String, ConfigurableApplicationContext> instances = new TreeMap<>();
    final ConfigurableApplicationContext clientContext;
    final DiscoveryClient discovery;
    final PricingClient pricing;

    Cluster() throws IOException, InterruptedException {
        consul = ConsulAgent.start();
        clientContext = new SpringApplicationBuilder(ClientApplication.class).web(WebApplicationType.NONE)
                .properties(consulProperties("client", "1s")).properties("spring.cloud.consul.discovery.register=false").run();
        discovery = clientContext.getBean(DiscoveryClient.class);
        pricing = clientContext.getBean(PricingClient.class);
    }

    private String[] consulProperties(String name, String checkInterval) {
        return new String[]{"spring.application.name=" + (name.equals("client") ? "client" : "pricing"),
                "spring.cloud.consul.host=127.0.0.1",
                "spring.cloud.consul.port=" + consul.baseUrl().replaceAll(".*:", ""),
                "spring.cloud.consul.discovery.instance-id=" + name,
                "spring.cloud.consul.discovery.health-check-interval=" + checkInterval,
                "instance.name=" + name};
    }

    void start(String name) {
        start(name, "1s");
    }

    /** Starts a copy of Pricing on a free port. It registers itself; nothing here tells Consul anything. */
    void start(String name, String checkInterval) {
        instances.put(name, new SpringApplicationBuilder(PricingInstance.class).web(WebApplicationType.SERVLET)
                .properties(consulProperties(name, checkInterval)).run());
    }

    /** A graceful stop: the copy deregisters itself on the way out. */
    void stop(String name) {
        instances.remove(name).close();
    }

    /** A crash: the copy stops answering and never says goodbye, so its registration stays. */
    void crash(String name) {
        ((WebServerApplicationContext) instances.get(name)).getWebServer().stop();
    }

    String baseUrl(String name) {
        return "http://127.0.0.1:" + ((WebServerApplicationContext) instances.get(name)).getWebServer().getPort();
    }

    List<String> listed() {
        return discovery.getInstances("pricing").stream().map(ServiceInstance::getInstanceId).sorted().toList();
    }

    /** Waits, up to a deadline, until Consul lists exactly this many healthy copies. */
    boolean awaitListed(int count) throws InterruptedException {
        long deadline = System.nanoTime() + TimeUnit.SECONDS.toNanos(30);
        while (System.nanoTime() < deadline) {
            if (listed().size() == count) {
                return true;
            }
            Thread.sleep(100);
        }
        return false;
    }

    /** Sends requests by service name and counts which copy answered, and how many failed. */
    Map<String, Integer> send(int requests) {
        Map<String, Integer> answers = new TreeMap<>();
        for (int i = 0; i < requests; i++) {
            try {
                answers.merge(pricing.price("MUG-BLUE"), 1, Integer::sum);
            } catch (RuntimeException e) {
                answers.merge("failed", 1, Integer::sum);
            }
        }
        return answers;
    }

    @Override
    public void close() {
        clientContext.close();
        new ArrayList<>(instances.values()).forEach(ConfigurableApplicationContext::close);
        consul.close();
    }
}
