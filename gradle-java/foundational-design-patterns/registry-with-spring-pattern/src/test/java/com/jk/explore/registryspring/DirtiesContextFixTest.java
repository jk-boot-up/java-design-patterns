package com.jk.explore.registryspring;

import com.jk.explore.registryspring.app.InjectedCheckout;
import com.jk.explore.registryspring.domain.RecordingGateway;
import org.junit.jupiter.api.MethodOrderer;
import org.junit.jupiter.api.Order;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestMethodOrder;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.annotation.DirtiesContext;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** The fix: {@code @DirtiesContext} throws the cached context away, at the price of starting Spring again. */
@SpringBootTest(classes = RegistrySpringApplication.class, properties = "test.context=dirties")
@TestMethodOrder(MethodOrderer.OrderAnnotation.class)
class DirtiesContextFixTest {

    @Autowired InjectedCheckout checkout;
    @Autowired RecordingGateway gateway;

    @Test
    @Order(1)
    @DirtiesContext(methodMode = DirtiesContext.MethodMode.AFTER_METHOD)
    void aChargesAndThenDirtiesTheContext() {
        checkout.place(10_000);
        assertEquals(1, gateway.charges().size());
    }

    @Test
    @Order(2)
    void bGetsAFreshContextAndACleanGateway() {
        assertEquals(0, gateway.charges().size());
    }
}
