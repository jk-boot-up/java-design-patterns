package com.jk.explore.proxyspring;

import org.junit.jupiter.api.Test;
import org.springframework.aop.support.AopUtils;
import org.springframework.context.ConfigurableApplicationContext;

import static org.junit.jupiter.api.Assertions.*;

class ProxyBeanTest {

    @Test
    void theBeanIsAGeneratedSubclass() {
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            ImageCatalogue c = ctx.getBean(ImageCatalogue.class);
            assertTrue(AopUtils.isAopProxy(c));
            assertNotSame(ImageCatalogue.class, c.getClass());
        }
    }

    @Test
    void shopperIsRefusedAndAdminIsNot() {
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            ImageCatalogue c = ctx.getBean(ImageCatalogue.class);
            Session s = ctx.getBean(Session.class);
            s.actAs(Role.CATALOG_ADMIN);
            assertTrue(c.render("A").contains("A"));
            s.actAs(Role.SHOPPER);
            assertThrows(AccessDenied.class, () -> c.render("A"));
        }
    }

    @Test
    void oneAspectProtectsEveryBean() {
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            assertThrows(AccessDenied.class, () -> ctx.getBean(OrderExport.class).exportAll());
            assertThrows(AccessDenied.class, () -> ctx.getBean(RefundDesk.class).refund("X"));
        }
    }

    @Test
    void lazyImageLoadsOnFirstRender() {
        HighResolutionImage.LOADS.set(0);
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            ImageCatalogue c = ctx.getBean(ImageCatalogue.class);
            assertEquals(0, HighResolutionImage.LOADS.get());
            c.owner();
            assertEquals(0, HighResolutionImage.LOADS.get());
            ctx.getBean(Session.class).actAs(Role.CATALOG_ADMIN);
            c.render("A");
            assertEquals(1, HighResolutionImage.LOADS.get());
        }
    }

    @Test
    void callOnThisSkipsTheCheck() {
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            ImageCatalogue c = ctx.getBean(ImageCatalogue.class);
            assertThrows(AccessDenied.class, () -> c.render("A"));
            assertDoesNotThrow(() -> c.renderThroughThis("A"));
        }
    }

    @Test
    void finalMethodIsNotChecked() {
        try (ConfigurableApplicationContext ctx = ImageApplication.builder().run()) {
            ImageCatalogue c = ctx.getBean(ImageCatalogue.class);
            assertThrows(NullPointerException.class, () -> c.renderFinal("A"));
        }
    }
}
