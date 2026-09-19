package com.jk.explore.registryspring;

import com.jk.explore.registryspring.app.InjectedCheckout;
import com.jk.explore.registryspring.app.LocatorStyleCheckout;
import com.jk.explore.registryspring.app.Settings;
import com.jk.explore.registryspring.domain.Notifier;
import com.jk.explore.registryspring.domain.PaymentGateway;
import com.jk.explore.registryspring.domain.RecordingGateway;
import com.jk.explore.registryspring.domain.RecordingNotifier;
import com.jk.explore.registryspring.domain.SmsNotifier;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.BeanCreationException;
import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.context.ApplicationContext;
import org.springframework.context.annotation.AnnotationConfigApplicationContext;
import org.springframework.context.support.PropertySourcesPlaceholderConfigurer;
import org.springframework.core.env.Environment;
import org.springframework.test.annotation.DirtiesContext;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertInstanceOf;
import static org.junit.jupiter.api.Assertions.assertNull;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(classes = RegistrySpringApplication.class, properties = "test.context=behaviour")
@DirtiesContext(classMode = DirtiesContext.ClassMode.AFTER_CLASS)
class RegistryBehaviourTest {

    @Autowired ApplicationContext context;
    @Autowired Environment environment;

    @Test
    void theContextIsARegistryKeyedByType() {
        assertInstanceOf(RecordingGateway.class, context.getBean(PaymentGateway.class));
        assertEquals(1, context.getBeanNamesForType(PaymentGateway.class).length);
    }

    @Test
    void theLocatorStyleClassHasAZeroArgumentConstructorAndFailsWithoutSpring() {
        assertEquals(0, LocatorStyleCheckout.class.getConstructors()[0].getParameterCount());
        assertThrows(NullPointerException.class, () -> new LocatorStyleCheckout().place(10_000));
    }

    @Test
    void theInjectedClassStatesItsDependenciesInItsSignature() {
        assertEquals(3, InjectedCheckout.class.getConstructors()[0].getParameterCount());
    }

    @Test
    void anUntypedPropertyLookupWithATypoIsSilentlyNull() {
        assertEquals("GBP", environment.getProperty("checkout.currency"));
        assertNull(environment.getProperty("checkout.curency"));
    }

    @Test
    void aRequiredValueWithTheSameTypoFailsWhenTheContextStarts() {
        AnnotationConfigApplicationContext broken = new AnnotationConfigApplicationContext();
        broken.register(PropertySourcesPlaceholderConfigurer.class, Settings.class);
        BeanCreationException e = assertThrows(BeanCreationException.class, broken::refresh);
        Throwable root = e;
        while (root.getCause() != null) {
            root = root.getCause();
        }
        assertTrue(root.getMessage().contains("checkout.curency"), root.getMessage());
    }

    @Test
    void askingByTypeIsAmbiguousWithTwoBeansAndFailsAtTheCallSite() {
        try (AnnotationConfigApplicationContext ctx = new AnnotationConfigApplicationContext(RecordingNotifier.class, SmsNotifier.class)) {
            NoUniqueBeanDefinitionException e = assertThrows(NoUniqueBeanDefinitionException.class, () -> ctx.getBean(Notifier.class));
            assertEquals(2, e.getNumberOfBeansFound());
        }
    }
}
