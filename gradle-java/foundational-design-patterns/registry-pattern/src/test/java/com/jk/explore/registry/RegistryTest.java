package com.jk.explore.registry;

import com.jk.explore.registry.domain.DiscountPolicy;
import com.jk.explore.registry.domain.LoyaltyPolicy;
import com.jk.explore.registry.domain.Notifier;
import com.jk.explore.registry.domain.PaymentGateway;
import com.jk.explore.registry.domain.RecordingGateway;
import com.jk.explore.registry.domain.RecordingNotifier;
import com.jk.explore.registry.naive.PassedDownCheckout;
import com.jk.explore.registry.pattern.OrderDependence;
import com.jk.explore.registry.pattern.OrderDependence.NamedTest;
import com.jk.explore.registry.pattern.Registry;
import com.jk.explore.registry.pattern.RegistryCheckout;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Constructor;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class RegistryTest {

    @BeforeEach
    @AfterEach
    void cleanTheGlobalState() {
        Registry.clear();
    }

    @Test
    void passingItDownWorksAndTheGatewayGoesThroughSixClasses() {
        RecordingGateway gateway = new RecordingGateway();
        RecordingNotifier notifier = new RecordingNotifier();
        new PassedDownCheckout(new LoyaltyPolicy(), gateway, notifier).place(10_000);
        assertEquals(List.of(9_000L), gateway.charges());
        assertEquals(1, notifier.sent().size());
    }

    @Test
    void fiveOfTheSixChainClassesOnlyForwardTheGateway() {
        int users = 0;
        Class<?>[] chain = com.jk.explore.registry.domain.ForwardChain.class.getDeclaredClasses();
        assertEquals(6, chain.length);
        for (Class<?> c : chain) {
            boolean hasGatewayField = java.util.Arrays.stream(c.getDeclaredFields())
                    .anyMatch(f -> f.getType() == PaymentGateway.class);
            if (hasGatewayField) {
                users++;
            }
        }
        assertEquals(1, users, "only Charger holds the gateway; the other five forward it");
    }

    @Test
    void theRegistryCheckoutTakesNothingInItsConstructor() throws Exception {
        Constructor<?>[] constructors = RegistryCheckout.class.getConstructors();
        assertEquals(1, constructors.length);
        assertEquals(0, constructors[0].getParameterCount());
    }

    @Test
    void itWorksOnceThreeThingsAreRegistered() {
        RecordingGateway gateway = new RecordingGateway();
        Registry.register(DiscountPolicy.class, new LoyaltyPolicy());
        Registry.register(PaymentGateway.class, gateway);
        Registry.register(Notifier.class, new RecordingNotifier());
        new RegistryCheckout().place(10_000);
        assertEquals(List.of(9_000L), gateway.charges());
    }

    @Test
    void withNothingRegisteredItCompilesAndConstructsButFailsOnFirstUse() {
        RegistryCheckout checkout = new RegistryCheckout();
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> checkout.place(10_000));
        assertTrue(e.getMessage().contains("nothing is registered for DiscountPolicy"), e.getMessage());
    }

    private static NamedTest usesTheRealGateway() {
        return new NamedTest("uses", () -> {
            Registry.register(DiscountPolicy.class, new LoyaltyPolicy());
            Registry.register(Notifier.class, new RecordingNotifier());
            if (!Registry.contents().contains("PaymentGateway")) {
                Registry.register(PaymentGateway.class, new RecordingGateway());
            }
            new RegistryCheckout().place(10_000);
            long total = ((RecordingGateway) Registry.get(PaymentGateway.class)).charges().size();
            if (total != 1) {
                throw new AssertionError("expected exactly one charge in total, saw " + total);
            }
        });
    }

    private static NamedTest leavesAGatewayBehind() {
        return new NamedTest("leaves", () -> {
            RecordingGateway g = new RecordingGateway();
            g.charge(500);
            Registry.register(PaymentGateway.class, g);
        });
    }

    @Test
    void theSameTwoTestsPassInOneOrderAndOneFailsInTheOther() {
        List<String> one = OrderDependence.run(List.of(usesTheRealGateway(), leavesAGatewayBehind()));
        List<String> two = OrderDependence.run(List.of(leavesAGatewayBehind(), usesTheRealGateway()));
        assertEquals(List.of("uses: passed", "leaves: passed"), one);
        assertEquals("leaves: passed", two.get(0));
        assertTrue(two.get(1).startsWith("uses: FAILED"), two.get(1));
    }

    @Test
    void whatIsInTheRegistryDependsOnWhatHasRunSoFar() {
        assertEquals(List.of(), Registry.contents());
        Registry.register(Notifier.class, new RecordingNotifier());
        assertEquals(List.of("Notifier"), Registry.contents());
    }
}
