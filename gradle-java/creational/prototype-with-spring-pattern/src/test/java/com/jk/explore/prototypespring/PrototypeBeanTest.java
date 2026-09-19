package com.jk.explore.prototypespring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import static org.junit.jupiter.api.Assertions.*;

class PrototypeBeanTest {

    @Test
    void everyRequestBuildsANewOne() {
        try (ConfigurableApplicationContext ctx = ListingApplication.builder().run()) {
            assertNotSame(ctx.getBean(Listing.class), ctx.getBean(Listing.class));
            assertEquals("Untitled", ctx.getBean(Listing.class).title());
        }
    }

    @Test
    void copiesAreIndependent() {
        try (ConfigurableApplicationContext ctx = ListingApplication.builder().run()) {
            Listing a = ctx.getBean(Listing.class);
            Listing b = ctx.getBean(Listing.class);
            a.images().add("x.png");
            assertEquals(1, b.images().size());
        }
    }

    @Test
    void containerDoesNotCopyAnEditedDraft() {
        try (ConfigurableApplicationContext ctx = ListingApplication.builder().run()) {
            Listing draft = ctx.getBean(Listing.class);
            draft.setTitle("Blue Mug");
            assertEquals("Untitled", ctx.getBean(Listing.class).title());
            assertEquals("Blue Mug", draft.copy().title());
            draft.copy().images().add("other.png");
            assertEquals(1, draft.images().size());
        }
    }

    @Test
    void injectedOnceIsTheSameObjectForever() {
        try (ConfigurableApplicationContext ctx = ListingApplication.builder().run()) {
            Storefront shop = ctx.getBean(Storefront.class);
            assertSame(shop.draftInjectedOnce(), shop.draftInjectedOnce());
        }
    }

    @Test
    void providerBuildsANewOneEachCall() {
        try (ConfigurableApplicationContext ctx = ListingApplication.builder().run()) {
            Storefront shop = ctx.getBean(Storefront.class);
            assertNotSame(shop.freshDraft(), shop.freshDraft());
        }
    }

    @Test
    void prototypesAreNotDestroyedButSingletonsAre() {
        Listing.DESTROYED.set(0);
        Storefront.DESTROYED.set(0);
        ConfigurableApplicationContext ctx = ListingApplication.builder().run();
        ctx.getBean(Listing.class);
        ctx.getBean(Listing.class);
        ctx.close();
        assertEquals(0, Listing.DESTROYED.get());
        assertEquals(1, Storefront.DESTROYED.get());
    }
}
