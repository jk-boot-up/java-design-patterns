package com.jk.explore.registryspring;

import com.jk.explore.registryspring.app.InjectedCheckout;
import com.jk.explore.registryspring.domain.RecordingGateway;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;

import static org.junit.jupiter.api.Assertions.assertEquals;

/**
 * <strong>Spring's test support caches the ApplicationContext and reuses it, so a
 * singleton's state leaks from one test to the next.</strong> The second test
 * passes only because the first ran before it. Run alone, it would fail: the
 * hand-built registry's order dependence, in Spring.
 */
@SpringBootTest(classes = RegistrySpringApplication.class, properties = "test.context=leak")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class SharedContextLeakTest {

    @Autowired InjectedCheckout checkout;
    @Autowired RecordingGateway gateway;

    @Test
    @Order(1)
    void aChargesTheSingletonGateway() {
        checkout.place(10_000);
        assertEquals(1, gateway.charges().size());
    }

    @Test
    @Order(2)
    void bSeesWhatAWroteOnlyBecauseTheContextWasShared() {
        assertEquals(1, gateway.charges().size(), "a leftover from test A: pass, only in this order");
    }
}
