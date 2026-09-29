package com.jk.explore.plugin;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;

import java.util.List;
import org.junit.jupiter.api.Test;

class PluginFactoryTest {

    @Test
    void prodGetsTheRealOnes() {
        PluginFactory f = new PluginFactory("prod");
        assertInstanceOf(Implementations.CardGateway.class, f.get(Services.PaymentGateway.class));
        assertInstanceOf(Implementations.SmtpEmailer.class, f.get(Services.Emailer.class));
    }

    @Test
    void stagingNeverTouchesRealCustomers() {
        PluginFactory f = new PluginFactory("staging");
        assertInstanceOf(Implementations.FakeGateway.class, f.get(Services.PaymentGateway.class));
        assertInstanceOf(Implementations.SandboxEmailer.class, f.get(Services.Emailer.class));
    }

    @Test
    void everyRealEnvironmentPassesTheStartupCheck() {
        for (String env : List.of("dev", "staging", "prod")) {
            assertEquals(List.of(), new PluginFactory(env).check(Services.PaymentGateway.class, Services.Emailer.class));
        }
    }

    @Test
    void misspeltClassIsReported() {
        assertEquals(1, new PluginFactory("demo").check(Services.PaymentGateway.class, Services.Emailer.class).size());
    }

    @Test
    void missingFileFails() {
        assertThrows(IllegalStateException.class, () -> new PluginFactory("nowhere"));
    }
}
