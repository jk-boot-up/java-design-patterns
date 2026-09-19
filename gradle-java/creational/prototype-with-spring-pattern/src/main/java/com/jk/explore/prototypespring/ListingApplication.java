package com.jk.explore.prototypespring;

import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class ListingApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(ListingApplication.class).web(WebApplicationType.NONE);
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static void one() {
        System.out.println("ONE. A new one each time.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Listing a = ctx.getBean(Listing.class);
            Listing b = ctx.getBean(Listing.class);
            System.out.println("  same object: " + (a == b) + ". both are titled '" + a.title() + "'.");
        }
    }

    static void two() {
        System.out.println("TWO. Independent.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Listing a = ctx.getBean(Listing.class);
            Listing b = ctx.getBean(Listing.class);
            a.setTitle("Blue Mug");
            a.images().add("mug-front.png");
            System.out.println("  a: '" + a.title() + "' with " + a.images().size() + " images.");
            System.out.println("  b: '" + b.title() + "' with " + b.images().size() + " image.");
        }
    }

    static void three() {
        System.out.println("THREE. A definition, not a draft.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Listing draft = ctx.getBean(Listing.class);
            draft.setTitle("Blue Mug");
            draft.images().add("mug-front.png");
            Listing fromContainer = ctx.getBean(Listing.class);
            Listing copied = draft.copy();
            System.out.println("  asked the container again: '" + fromContainer.title() + "' with " + fromContainer.images().size() + " image.");
            System.out.println("  asked the draft to copy(): '" + copied.title() + "' with " + copied.images().size() + " images.");
        }
    }

    static void four() {
        System.out.println("FOUR. A prototype inside a singleton.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Storefront shop = ctx.getBean(Storefront.class);
            Listing first = shop.draftInjectedOnce();
            first.setTitle("Blue Mug");
            Listing second = shop.draftInjectedOnce();
            System.out.println("  two calls, same object: " + (first == second) + ".");
            System.out.println("  the second caller sees the first caller's title: '" + second.title() + "'.");
        }
    }

    static void five() {
        System.out.println("FIVE. Ask each time.");
        try (ConfigurableApplicationContext ctx = builder().run()) {
            Storefront shop = ctx.getBean(Storefront.class);
            Listing first = shop.freshDraft();
            first.setTitle("Blue Mug");
            Listing second = shop.freshDraft();
            System.out.println("  two calls, same object: " + (first == second) + ".");
            System.out.println("  the second caller sees: '" + second.title() + "'.");
        }
    }

    static void six() {
        System.out.println("SIX. Nobody cleans up.");
        Listing.BUILT.set(0);
        Listing.DESTROYED.set(0);
        Storefront.DESTROYED.set(0);
        ConfigurableApplicationContext ctx = builder().run();
        Listing.BUILT.set(0); // the storefront took one at startup; count only what is asked for now
        for (int i = 0; i < 3; i++) {
            ctx.getBean(Listing.class);
        }
        int built = Listing.BUILT.get();
        ctx.close();
        System.out.println("  listings built: " + built + ". listings destroyed on close: " + Listing.DESTROYED.get() + ".");
        System.out.println("  the singleton's destroy method ran " + Storefront.DESTROYED.get() + " time on close.");
        System.out.println("  Spring builds a prototype and lets go of it. Cleaning up is the caller's job.");
    }
}
