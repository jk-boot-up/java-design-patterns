package com.jk.explore.dependencyinjection;

import com.jk.explore.dependencyinjection.app.Auditor;
import com.jk.explore.dependencyinjection.app.CheckoutService;
import com.jk.explore.dependencyinjection.app.OverloadedService;
import com.jk.explore.dependencyinjection.app.ReceiptPrinter;
import com.jk.explore.dependencyinjection.app.Storefront;
import com.jk.explore.dependencyinjection.container.Chicken;
import com.jk.explore.dependencyinjection.container.ContainerFailure;
import com.jk.explore.dependencyinjection.container.Egg;
import com.jk.explore.dependencyinjection.container.Injector;
import com.jk.explore.dependencyinjection.container.MiniContainer;
import com.jk.explore.dependencyinjection.domain.DiscountPolicy;
import com.jk.explore.dependencyinjection.domain.LoyaltyPolicy;
import com.jk.explore.dependencyinjection.domain.Notifier;
import com.jk.explore.dependencyinjection.domain.PaymentGateway;
import com.jk.explore.dependencyinjection.domain.RecordingGateway;
import com.jk.explore.dependencyinjection.domain.RecordingNotifier;
import com.jk.explore.dependencyinjection.forms.FieldInjectedCheckout;
import com.jk.explore.dependencyinjection.forms.SetterInjectedCheckout;
import com.jk.explore.dependencyinjection.wiring.Wiring;
import org.junit.jupiter.api.Test;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class DependencyInjectionTest {

    @Test
    void theConstructorSignatureIsTheCompleteDependencyList() {
        assertEquals(1, CheckoutService.class.getConstructors().length);
        assertArrayEquals(new Class<?>[]{DiscountPolicy.class, PaymentGateway.class, Notifier.class},
                CheckoutService.class.getConstructors()[0].getParameterTypes());
        assertEquals("CheckoutService(DiscountPolicy, PaymentGateway, Notifier)", WiringDemo.constructorSignature());
    }

    @Test
    void aCheckoutBuiltWithFakesNeedsNoFrameworkAndNoGlobalSetup() {
        RecordingGateway gateway = new RecordingGateway();
        RecordingNotifier notifier = new RecordingNotifier();
        new CheckoutService(new LoyaltyPolicy(), gateway, notifier).place(10_000);
        assertEquals(List.of(9_000L), gateway.charges());
        assertEquals(1, notifier.sent().size());
    }

    @Test
    void handWiringBuildsTheWholeApplicationInAHandfulOfLines() {
        Wiring.Application app = Wiring.build();
        app.storefront().order(10_000);
        assertEquals(List.of(9_000L), app.gateway().charges());
        assertEquals(3, app.notifier().sent().size());
        int lines = WiringDemo.linesBetweenMarkers("src/main/java/com/jk/explore/dependencyinjection/wiring/Wiring.java",
                "// wiring begins", "// wiring ends");
        assertTrue(lines < 20, "the wiring is " + lines + " lines");
    }

    @Test
    void setterInjectionSuitsAnOptionalCollaboratorWithADefault() {
        RecordingGateway gateway = new RecordingGateway();
        SetterInjectedCheckout checkout = new SetterInjectedCheckout(new LoyaltyPolicy(), gateway);
        checkout.place(10_000);
        assertEquals(List.of(9_000L), gateway.charges(), "it worked with no notifier");
        RecordingNotifier notifier = new RecordingNotifier();
        checkout.setNotifier(notifier);
        checkout.place(10_000);
        assertEquals(1, notifier.sent().size());
    }

    @Test
    void fieldInjectionLetsYouBuildAnInvalidObjectAndNeedsReflectionToFixIt() {
        FieldInjectedCheckout invalid = new FieldInjectedCheckout();
        assertThrows(NullPointerException.class, () -> invalid.place(10_000));
        Injector.injectFields(invalid, new LoyaltyPolicy(), new RecordingGateway(), new RecordingNotifier());
        assertEquals("receipt-1", invalid.place(10_000));
    }

    @Test
    void theHandWrittenContainerBuildsTheSameGraphAsTheHandWiring() {
        MiniContainer container = MiniContainer.start(LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class,
                CheckoutService.class, ReceiptPrinter.class, Auditor.class, Storefront.class);
        container.get(Storefront.class).order(10_000);
        assertEquals(List.of(9_000L), container.get(RecordingGateway.class).charges());
        assertEquals(3, container.get(RecordingNotifier.class).sent().size());
    }

    @Test
    void theContainerFailsAtStartWhenABeanIsMissing() {
        ContainerFailure e = assertThrows(ContainerFailure.class,
                () -> MiniContainer.start(LoyaltyPolicy.class, RecordingGateway.class, CheckoutService.class));
        assertTrue(e.getMessage().contains("no bean for its parameter of type Notifier"), e.getMessage());
    }

    @Test
    void theContainerFailsAtStartOnACircularDependency() {
        ContainerFailure e = assertThrows(ContainerFailure.class, () -> MiniContainer.start(Chicken.class, Egg.class));
        assertEquals("circular dependency: Chicken -> Egg -> Chicken", e.getMessage());
    }

    @Test
    void aSevenArgumentConstructorIsADesignSmellWhateverTheInjectionStyle() {
        assertEquals(7, OverloadedService.class.getConstructors()[0].getParameterCount());
    }
}
