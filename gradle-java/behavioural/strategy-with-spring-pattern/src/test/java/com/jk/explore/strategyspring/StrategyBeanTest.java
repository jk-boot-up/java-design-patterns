package com.jk.explore.strategyspring;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.NoUniqueBeanDefinitionException;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.context.support.GenericApplicationContext;

import java.util.Set;

import static org.junit.jupiter.api.Assertions.*;

class StrategyBeanTest {

    @Test
    void springCollectsAllFourByBeanName() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder().run()) {
            assertEquals(Set.of("flat", "weightBanded", "distance", "freeOverThreshold"), ctx.getBean(CheckoutService.class).ruleNames());
        }
    }

    @Test
    void everyRulePricesTheSameShipmentsAsExpected() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder().run()) {
            CheckoutService c = ctx.getBean(CheckoutService.class);
            assertEquals(499, c.quote("flat", ShippingApplication.HEAVY));
            assertEquals(299, c.quote("weightBanded", ShippingApplication.LIGHT));
            assertEquals(899, c.quote("weightBanded", ShippingApplication.HEAVY));
            assertEquals(349, c.quote("distance", ShippingApplication.MIDDLE));
            assertEquals(0, c.quote("freeOverThreshold", ShippingApplication.HEAVY));
            assertEquals(499, c.quote("freeOverThreshold", ShippingApplication.MIDDLE));
        }
    }

    @Test
    void unknownNameAtRunTimeIsRefused() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder().run()) {
            assertThrows(IllegalArgumentException.class, () -> ctx.getBean(CheckoutService.class).quote("teleport", ShippingApplication.LIGHT));
        }
    }

    @Test
    void configurationChoosesTheRule() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder().properties("shipping.rule=distance").run()) {
            assertEquals(299 + 4 * 50, ctx.getBean(SelectedShipping.class).cost(ShippingApplication.HEAVY));
        }
    }

    @Test
    void unknownConfiguredNameStopsStartup() {
        assertThrows(Exception.class, () -> ShippingApplication.builder().properties("shipping.rule=teleport").run().close());
    }

    @Test
    void askingForTheInterfaceAloneIsAmbiguous() {
        Exception e = assertThrows(Exception.class, () -> ShippingApplication.builder()
                .initializers(c -> ((GenericApplicationContext) c).registerBean(NeedsOneRule.class)).run().close());
        Throwable root = e;
        while (root.getCause() != null) root = root.getCause();
        assertInstanceOf(NoUniqueBeanDefinitionException.class, root);
        assertEquals(4, ((NoUniqueBeanDefinitionException) root).getNumberOfBeansFound());
    }

    @Test
    void aFifthRuleIsFoundWithoutChangingCheckout() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder()
                .initializers(c -> ((GenericApplicationContext) c).registerBean("express", ExpressRule.class)).run()) {
            CheckoutService c = ctx.getBean(CheckoutService.class);
            assertEquals(5, c.ruleNames().size());
            assertEquals(999, c.quote("express", ShippingApplication.LIGHT));
        }
    }

    @Test
    void primaryMakesTheInterfaceInjectable() {
        try (ConfigurableApplicationContext ctx = ShippingApplication.builder().initializers(c -> {
            c.addBeanFactoryPostProcessor(bf -> bf.getBeanDefinition("flat").setPrimary(true));
            ((GenericApplicationContext) c).registerBean(NeedsOneRule.class);
        }).run()) {
            assertEquals(499, ctx.getBean(NeedsOneRule.class).cost(ShippingApplication.LIGHT));
            assertEquals(4, ctx.getBean(CheckoutService.class).ruleNames().size());
        }
    }
}
