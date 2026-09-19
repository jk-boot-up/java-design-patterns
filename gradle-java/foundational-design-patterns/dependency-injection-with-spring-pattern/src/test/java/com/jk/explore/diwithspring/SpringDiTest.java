package com.jk.explore.diwithspring;

import com.jk.explore.diwithspring.app.Auditor;
import com.jk.explore.diwithspring.app.CheckoutService;
import com.jk.explore.diwithspring.app.ReceiptPrinter;
import com.jk.explore.diwithspring.app.Storefront;
import com.jk.explore.diwithspring.container.Chicken;
import com.jk.explore.diwithspring.container.Egg;
import com.jk.explore.diwithspring.domain.DiscountPolicy;
import com.jk.explore.diwithspring.domain.LoyaltyPolicy;
import com.jk.explore.diwithspring.domain.Notifier;
import com.jk.explore.diwithspring.domain.PaymentGateway;
import com.jk.explore.diwithspring.domain.RecordingGateway;
import com.jk.explore.diwithspring.domain.RecordingNotifier;
import com.jk.explore.diwithspring.forms.FieldInjectedCheckout;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.BeanCreationException;
import org.springframework.beans.factory.BeanCurrentlyInCreationException;
import org.springframework.beans.factory.UnsatisfiedDependencyException;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;

import java.util.List;

import static org.junit.jupiter.api.Assertions.assertArrayEquals;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

class SpringDiTest {

    private AnnotationConfigApplicationContext fullContext() {
        return new AnnotationConfigApplicationContext(LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class,
                CheckoutService.class, ReceiptPrinter.class, Auditor.class, Storefront.class);
    }

    @Test
    void theSignatureIsStillTheDependencyListAndTheConstructorIsUntouched() {
        assertArrayEquals(new Class<?>[]{DiscountPolicy.class, PaymentGateway.class, Notifier.class},
                CheckoutService.class.getConstructors()[0].getParameterTypes());
    }

    @Test
    void springBuildsTheSameGraphTheHandWiringBuilt() {
        try (AnnotationConfigApplicationContext context = fullContext()) {
            context.getBean(Storefront.class).order(10_000);
            assertEquals(List.of(9_000L), context.getBean(RecordingGateway.class).charges());
            assertEquals(3, context.getBean(RecordingNotifier.class).sent().size());
        }
    }

    @Test
    void aSingleConstructorNeedsNoAutowiredAnnotation() {
        assertEquals(0, java.util.Arrays.stream(CheckoutService.class.getConstructors()[0].getAnnotations()).count());
    }

    @Test
    void aMissingBeanIsAStartUpFailureNamingTheParameter() {
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
        context.register(LoyaltyPolicy.class, RecordingGateway.class, CheckoutService.class);
        UnsatisfiedDependencyException e = assertThrows(UnsatisfiedDependencyException.class, context::refresh);
        assertTrue(e.getMessage().contains("constructor parameter 2"), e.getMessage());
        assertTrue(e.getMessage().contains("Notifier"), e.getMessage());
    }

    @Test
    void aCircularDependencyIsRefusedAtStartUp() {
        AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext();
        context.register(Chicken.class, Egg.class);
        BeanCreationException e = assertThrows(BeanCreationException.class, context::refresh);
        Throwable root = e;
        while (root.getCause() != null) {
            root = root.getCause();
        }
        assertInstanceOf(BeanCurrentlyInCreationException.class, root);
    }

    @Test
    void fieldInjectionIsFilledBySpringAndInvalidWithout() {
        assertThrows(NullPointerException.class, () -> new FieldInjectedCheckout().place(10_000));
        try (AnnotationConfigApplicationContext context = new AnnotationConfigApplicationContext(
                LoyaltyPolicy.class, RecordingGateway.class, RecordingNotifier.class, FieldInjectedCheckout.class)) {
            assertEquals("receipt-1", context.getBean(FieldInjectedCheckout.class).place(10_000));
        }
    }

    @Test
    void aCheckoutBuiltWithFakesNeedsNoSpringAtAll() {
        RecordingGateway gateway = new RecordingGateway();
        new CheckoutService(new LoyaltyPolicy(), gateway, new RecordingNotifier()).place(10_000);
        assertEquals(List.of(9_000L), gateway.charges());
    }
}
