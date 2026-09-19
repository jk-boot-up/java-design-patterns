package com.jk.explore.servicelocator;

import com.jk.explore.servicelocator.domain.DiscountPolicy;
import com.jk.explore.servicelocator.domain.LoyaltyPolicy;
import com.jk.explore.servicelocator.domain.Notifier;
import com.jk.explore.servicelocator.domain.PaymentGateway;
import com.jk.explore.servicelocator.domain.RecordingGateway;
import com.jk.explore.servicelocator.domain.RecordingNotifier;
import com.jk.explore.servicelocator.pattern.LocatorCheckout;
import com.jk.explore.servicelocator.pattern.ServiceLocator;
import com.jk.explore.servicelocator.plugin.PaymentMethod;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;
import java.util.ServiceLoader;
import java.util.concurrent.atomic.AtomicInteger;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotSame;
import static org.junit.jupiter.api.Assertions.assertSame;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class ServiceLocatorTest {

    @BeforeEach
    @AfterEach
    void cleanTheGlobalState() {
        ServiceLocator.reset();
    }

    @Test
    void aSingletonIsCreatedLazilyAndOnlyOnce() {
        AtomicInteger made = new AtomicInteger();
        ServiceLocator.singleton(PaymentGateway.class, () -> {
            made.incrementAndGet();
            return new RecordingGateway();
        });
        assertEquals(0, made.get(), "nothing is created until it is asked for");
        assertSame(ServiceLocator.find(PaymentGateway.class), ServiceLocator.find(PaymentGateway.class));
        assertEquals(1, made.get());
    }

    @Test
    void aPrototypeIsANewInstanceEveryTime() {
        ServiceLocator.prototype(Notifier.class, RecordingNotifier::new);
        assertNotSame(ServiceLocator.find(Notifier.class), ServiceLocator.find(Notifier.class));
    }

    @Test
    void theLocatorCanBeReconfiguredForATestWithNoChangeToTheCheckout() {
        RecordingGateway fake = new RecordingGateway();
        ServiceLocator.singleton(DiscountPolicy.class, LoyaltyPolicy::new);
        ServiceLocator.singleton(PaymentGateway.class, () -> fake);
        ServiceLocator.singleton(Notifier.class, RecordingNotifier::new);
        new LocatorCheckout().place(10_000);
        assertEquals(List.of(9_000L), fake.charges());
    }

    @Test
    void aMissingRegistrationIsOnlyFoundAtRunTimeAfterTheCustomerWasCharged() {
        RecordingGateway gateway = new RecordingGateway();
        ServiceLocator.singleton(DiscountPolicy.class, LoyaltyPolicy::new);
        ServiceLocator.singleton(PaymentGateway.class, () -> gateway);
        LocatorCheckout checkout = new LocatorCheckout();
        IllegalStateException e = assertThrows(IllegalStateException.class, () -> checkout.place(10_000));
        assertTrue(e.getMessage().contains("Notifier"), e.getMessage());
        assertEquals(List.of(9_000L), gateway.charges(), "the money had already moved");
    }

    @Test
    void theCheckoutTakesNothingSoNothingInItsSignatureSaysWhatItNeeds() {
        assertEquals(0, LocatorCheckout.class.getConstructors()[0].getParameterCount());
    }

    @Test
    void threeClassesDependOnTheLocatorAndAnyOfThemNeedsItConfigured() {
        assertEquals(List.of("Auditor", "LocatorCheckout", "ReceiptPrinter"), LocatorDemo.classesUsingTheLocator());
        assertThrows(IllegalStateException.class, () -> new com.jk.explore.servicelocator.pattern.Auditor().audit("x"));
    }

    @Test
    void javasOwnServiceLoaderFindsPluginsListedInMetaInfServices() {
        List<String> names = new ArrayList<>();
        ServiceLoader.load(PaymentMethod.class).forEach(m -> names.add(m.name()));
        assertEquals(List.of("card", "bank transfer"), names);
    }
}
