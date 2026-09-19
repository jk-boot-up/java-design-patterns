package com.jk.explore.locatorconsul;

import com.jk.explore.locatorconsul.consul.Address;
import com.jk.explore.locatorconsul.consul.ConsulAgent;
import com.jk.explore.locatorconsul.consul.ConsulClient;
import com.jk.explore.locatorconsul.gateway.ServiceInstance;
import com.jk.explore.locatorconsul.pattern.CachingLocator;
import com.jk.explore.locatorconsul.pattern.ConsulLocator;
import com.jk.explore.locatorconsul.pattern.Discovery;
import com.jk.explore.locatorconsul.pattern.LocatorCheckout;
import com.jk.explore.locatorconsul.pattern.NoHealthyInstance;
import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.net.http.HttpClient;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

/** Runs against a real Consul agent. Skipped, not failed, when the {@code consul} binary is not installed. */
class ConsulLocatorTest {

    private static ConsulAgent agent;
    private static ConsulClient consul;
    private static ServiceInstance gateway1;
    private static ServiceInstance gateway2;
    private static ServiceInstance notifier;

    @BeforeAll
    static void startEverything() throws Exception {
        Assumptions.assumeTrue(ConsulAgent.available(), "consul is not installed");
        agent = ConsulAgent.start();
        consul = new ConsulClient(agent.baseUrl());
        gateway1 = new ServiceInstance("gateway-1");
        gateway2 = new ServiceInstance("gateway-2");
        notifier = new ServiceInstance("notifier-1");
    }

    @AfterAll
    static void stopEverything() {
        for (ServiceInstance s : new ServiceInstance[]{gateway1, gateway2, notifier}) {
            if (s != null) {
                s.close();
            }
        }
        if (agent != null) {
            agent.close();
        }
    }

    @BeforeEach
    void registerAllThree() {
        consul.register("payment-gateway", "gateway-1", gateway1.port());
        consul.register("payment-gateway", "gateway-2", gateway2.port());
        consul.register("notifier", "notifier-1", notifier.port());
        Discovery.use(new ConsulLocator(consul));
    }

    @Test
    void consulReportsTheTwoHealthyGatewaysWithTheirRealPorts() {
        List<Address> healthy = consul.healthy("payment-gateway");
        assertEquals(2, healthy.size());
        assertTrue(healthy.stream().anyMatch(a -> a.port() == gateway1.port()));
        assertTrue(healthy.stream().anyMatch(a -> a.port() == gateway2.port()));
    }

    @Test
    void theLocatorRotatesThroughTheHealthyInstances() {
        int before1 = gateway1.hits();
        int before2 = gateway2.hits();
        LocatorCheckout checkout = new LocatorCheckout();
        for (int i = 0; i < 4; i++) {
            checkout.place(10_000);
        }
        assertEquals(2, gateway1.hits() - before1);
        assertEquals(2, gateway2.hits() - before2);
    }

    @Test
    void anInstanceWhoseCheckFailsIsNoLongerReturnedAndRecoversWhenItPasses() {
        consul.fail("gateway-1");
        assertEquals(1, consul.healthy("payment-gateway").size());
        int before = gateway1.hits();
        for (int i = 0; i < 3; i++) {
            new LocatorCheckout().place(10_000);
        }
        assertEquals(before, gateway1.hits(), "the failing instance received nothing");
        consul.pass("gateway-1");
        assertEquals(2, consul.healthy("payment-gateway").size());
    }

    @Test
    void aTypoInAServiceNameCompilesAndFailsAtRunTime() {
        NoHealthyInstance e = assertThrows(NoHealthyInstance.class, () -> Discovery.find("payment-gatway"));
        assertTrue(e.getMessage().contains("payment-gatway"));
    }

    @Test
    void aMissingNotifierIsFoundOnlyAfterThePaymentWasTaken() {
        consul.deregister("notifier-1");
        int before = gateway1.hits() + gateway2.hits();
        assertThrows(NoHealthyInstance.class, () -> new LocatorCheckout().place(10_000));
        assertEquals(1, gateway1.hits() + gateway2.hits() - before, "the charge had already gone through");
    }

    @Test
    void aCachingLocatorKeepsHandingOutAnAddressAfterTheInstanceIsGone() throws Exception {
        try (ServiceInstance doomed = new ServiceInstance("doomed")) {
            consul.deregister("gateway-1");
            consul.deregister("gateway-2");
            consul.register("payment-gateway", "doomed", doomed.port());
            CachingLocator caching = new CachingLocator(consul);
            Address cached = caching.find("payment-gateway");
            assertEquals(doomed.port(), cached.port());
            doomed.stop();
            consul.fail("doomed");
            assertEquals(cached, caching.find("payment-gateway"), "still the dead address");
            assertThrows(IllegalStateException.class,
                    () -> LocatorCheckout.call(HttpClient.newHttpClient(), caching.find("payment-gateway"), "/charge?pence=1"));
            assertEquals(1, caching.timesConsulWasAsked());
            consul.deregister("doomed");
            caching.refresh();
            assertThrows(NoHealthyInstance.class, () -> caching.find("payment-gateway"));
        }
    }
}
