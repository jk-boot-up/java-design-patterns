package com.jk.explore.proxyspring;

import org.springframework.aop.support.AopUtils;
import org.springframework.boot.WebApplicationType;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

@SpringBootApplication
public class ImageApplication {

    static SpringApplicationBuilder builder() {
        return new SpringApplicationBuilder(ImageApplication.class).web(WebApplicationType.NONE);
    }

    public static void main(String[] args) {
        try (ConfigurableApplicationContext ctx = builder().run()) {
            one(ctx);
            two(ctx);
            three();
            four(ctx);
            five(ctx);
            six(ctx);
        }
    }

    static String attempt(java.util.function.Supplier<String> call) {
        try {
            return call.get();
        } catch (AccessDenied e) {
            return "refused: " + e.getMessage();
        }
    }

    static void one(ConfigurableApplicationContext ctx) {
        System.out.println("ONE. The bean is not your class.");
        ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
        System.out.println("  is a generated proxy: " + AopUtils.isAopProxy(catalogue));
        System.out.println("  its class is a subclass of ImageCatalogue: " + (catalogue.getClass() != ImageCatalogue.class
                && ImageCatalogue.class.isAssignableFrom(catalogue.getClass())));
        System.out.println("  the class Spring wrapped: " + AopUtils.getTargetClass(catalogue).getSimpleName());
    }

    static void two(ConfigurableApplicationContext ctx) {
        System.out.println("TWO. Protection, written once.");
        ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
        Session session = ctx.getBean(Session.class);
        session.actAs(Role.CATALOG_ADMIN);
        System.out.println("  admin: " + attempt(() -> catalogue.render("MUG-BLUE")));
        session.actAs(Role.SHOPPER);
        System.out.println("  shopper: " + attempt(() -> catalogue.render("MUG-BLUE")));
    }

    static void three() {
        System.out.println("THREE. Lazy loading.");
        HighResolutionImage.LOADS.set(0);
        try (ConfigurableApplicationContext ctx = builder().run()) {
            ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
            System.out.println("  after startup: " + HighResolutionImage.LOADS.get() + " images loaded.");
            System.out.println("  a cheap question, owner(): " + catalogue.owner() + ". images loaded: " + HighResolutionImage.LOADS.get() + ".");
            ctx.getBean(Session.class).actAs(Role.CATALOG_ADMIN);
            catalogue.render("MUG-BLUE");
            System.out.println("  after the first render: " + HighResolutionImage.LOADS.get() + " image loaded.");
        }
    }

    static void four(ConfigurableApplicationContext ctx) {
        System.out.println("FOUR. One aspect, three screens.");
        Session session = ctx.getBean(Session.class);
        session.actAs(Role.SHOPPER);
        ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
        OrderExport export = ctx.getBean(OrderExport.class);
        RefundDesk refunds = ctx.getBean(RefundDesk.class);
        System.out.println("  catalogue: " + attempt(() -> catalogue.render("MUG-BLUE")));
        System.out.println("  export: " + attempt(export::exportAll));
        System.out.println("  refunds: " + attempt(() -> refunds.refund("ORD-000001")));
        System.out.println("  the check was written once, in RoleAspect.");
    }

    static void five(ConfigurableApplicationContext ctx) {
        System.out.println("FIVE. A call on this skips the proxy.");
        ctx.getBean(Session.class).actAs(Role.SHOPPER);
        ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
        System.out.println("  render, called from outside: " + attempt(() -> catalogue.render("MUG-BLUE")));
        System.out.println("  renderThroughThis, a shopper: " + attempt(() -> catalogue.renderThroughThis("MUG-BLUE")));
        System.out.println("  the shopper got the image. nothing was logged.");
    }

    static void six(ConfigurableApplicationContext ctx) {
        System.out.println("SIX. A final method is not proxied.");
        ctx.getBean(Session.class).actAs(Role.SHOPPER);
        ImageCatalogue catalogue = ctx.getBean(ImageCatalogue.class);
        System.out.println("  renderFinal, a shopper: " + attempt(() -> {
            try {
                return catalogue.renderFinal("MUG-BLUE");
            } catch (NullPointerException e) {
                return "NullPointerException: the proxy instance has no fields of its own";
            }
        }));
    }
}
