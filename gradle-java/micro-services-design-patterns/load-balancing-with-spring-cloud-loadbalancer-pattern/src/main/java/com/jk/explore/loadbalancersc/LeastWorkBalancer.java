package com.jk.explore.loadbalancersc;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.client.loadbalancer.DefaultResponse;
import org.springframework.cloud.client.loadbalancer.EmptyResponse;
import org.springframework.cloud.client.loadbalancer.Request;
import org.springframework.cloud.client.loadbalancer.Response;
import org.springframework.cloud.loadbalancer.core.ReactorServiceInstanceLoadBalancer;
import org.springframework.cloud.loadbalancer.core.ServiceInstanceListSupplier;
import reactor.core.publisher.Mono;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * A strategy of our own, plugged into Spring Cloud LoadBalancer: send each request to the copy
 * that has been given the least work so far. Each instance says what one request costs it in
 * its metadata. Ties go to the earlier one in the list, so the choice is the same every run.
 */
public class LeastWorkBalancer implements ReactorServiceInstanceLoadBalancer {

    private final ObjectProvider<ServiceInstanceListSupplier> suppliers;
    private final Map<Integer, Integer> workByPort = new HashMap<>();

    public LeastWorkBalancer(ObjectProvider<ServiceInstanceListSupplier> suppliers) {
        this.suppliers = suppliers;
    }

    @Override
    public Mono<Response<ServiceInstance>> choose(Request request) {
        return suppliers.getIfAvailable().get(request).next().map(this::pick);
    }

    private synchronized Response<ServiceInstance> pick(List<ServiceInstance> instances) {
        ServiceInstance best = null;
        for (ServiceInstance candidate : instances) {
            if (best == null || work(candidate) < work(best)) {
                best = candidate;
            }
        }
        if (best == null) {
            return new EmptyResponse();
        }
        workByPort.merge(best.getPort(), Integer.parseInt(best.getMetadata().getOrDefault("cost", "1")), Integer::sum);
        return new DefaultResponse(best);
    }

    private int work(ServiceInstance instance) {
        return workByPort.getOrDefault(instance.getPort(), 0);
    }
}
