package com.jk.explore.loadbalancersc;

import org.springframework.beans.factory.ObjectProvider;
import org.springframework.cloud.client.ServiceInstance;
import org.springframework.cloud.loadbalancer.core.ReactorLoadBalancer;
import org.springframework.cloud.loadbalancer.core.ServiceInstanceListSupplier;
import org.springframework.context.annotation.Bean;

/**
 * Deliberately not annotated as a configuration: Spring Cloud LoadBalancer creates it inside
 * the child context of one named service. If component scanning found it, every service in the
 * application would use it.
 */
class LeastWorkConfiguration {

    @Bean
    ReactorLoadBalancer<ServiceInstance> loadBalancer(ObjectProvider<ServiceInstanceListSupplier> suppliers) {
        return new LeastWorkBalancer(suppliers);
    }
}
