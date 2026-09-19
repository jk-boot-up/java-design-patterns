package com.jk.explore.dependencyinjection.domain;

/**
 * <strong>The deep constructor chain.</strong> Six classes, and the gateway is
 * handed down through every one. Only the last, {@code Charger}, uses it. The
 * other five exist to forward it. This is real friction, and it is what makes
 * a registry tempting.
 */
public final class ForwardChain {

    private ForwardChain() {
    }

    public static final class Storefront {
        private final CartService next;

        public Storefront(PaymentGateway gateway) {
            this.next = new CartService(gateway);
        }

        public String checkout(long pence) {
            return next.checkout(pence);
        }
    }

    public static final class CartService {
        private final OrderCoordinator next;

        CartService(PaymentGateway gateway) {
            this.next = new OrderCoordinator(gateway);
        }

        String checkout(long pence) {
            return next.checkout(pence);
        }
    }

    public static final class OrderCoordinator {
        private final PricingStage next;

        OrderCoordinator(PaymentGateway gateway) {
            this.next = new PricingStage(gateway);
        }

        String checkout(long pence) {
            return next.checkout(pence);
        }
    }

    public static final class PricingStage {
        private final PaymentStage next;

        PricingStage(PaymentGateway gateway) {
            this.next = new PaymentStage(gateway);
        }

        String checkout(long pence) {
            return next.checkout(pence);
        }
    }

    public static final class PaymentStage {
        private final Charger next;

        PaymentStage(PaymentGateway gateway) {
            this.next = new Charger(gateway);
        }

        String checkout(long pence) {
            return next.charge(pence);
        }
    }

    public static final class Charger {
        private final PaymentGateway gateway;

        Charger(PaymentGateway gateway) {
            this.gateway = gateway;
        }

        String charge(long pence) {
            return gateway.charge(pence);
        }
    }
}
