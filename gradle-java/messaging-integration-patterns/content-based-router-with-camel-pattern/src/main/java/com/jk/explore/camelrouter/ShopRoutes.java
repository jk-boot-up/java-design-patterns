package com.jk.explore.camelrouter;

import java.util.concurrent.atomic.AtomicInteger;
import org.apache.camel.Exchange;
import org.apache.camel.Predicate;
import org.apache.camel.builder.RouteBuilder;

/**
 * The routes, written out as rules rather than as an if chain inside a receiver.
 *
 * <p>Four words from Apache Camel appear here, and each one is an ordinary idea with a short name. A
 * <em>route</em> is a written description of where messages come from, what is decided about them, and
 * where they go. An <em>endpoint</em> is one end of a route: a queue to read from, or a queue to write to.
 * An <em>exchange</em>, in Camel's sense, is the message while it is travelling, together with anything
 * learned about it on the way. A <em>predicate</em> is a yes-or-no question asked about that message.
 *
 * <p>Every route below reads from the same orders queue and asks the same kind of question: not who sent
 * this, but what is inside it.
 */
public final class ShopRoutes {

    private ShopRoutes() {
    }

    /** The queue the router reads from. */
    public static String inbox() {
        return "spring-rabbitmq:" + Broker.EXCHANGE + "?queues=" + Broker.ORDERS + "&autoDeclare=false";
    }

    /** A queue the router can send to. */
    public static String to(String queue) {
        return "spring-rabbitmq:" + Broker.EXCHANGE + "?routingKey=" + queue + "&autoDeclare=false";
    }

    private static Order order(Exchange exchange) {
        return Order.parse(exchange.getIn().getBody(String.class));
    }

    /** Worth a fraud officer's time: one thousand pounds or more. */
    public static final Predicate HIGH_VALUE = exchange -> order(exchange).pence() >= 100_000;

    /** Nothing to put in a box: a gift card, a download, a licence key. */
    public static final Predicate DIGITAL = exchange -> order(exchange).kind().equals("digital");

    /** The customer paid for it to go out today. */
    public static final Predicate EXPRESS = exchange -> order(exchange).shipping().equals("express");

    /** Something the warehouse can pick, pack and post. */
    public static final Predicate PHYSICAL = exchange -> order(exchange).kind().equals("physical");

    /** Bought from inside the European Union, so the tax has to be worked out before it ships. */
    public static final Predicate EU = exchange -> order(exchange).region().equals("EU");

    /**
     * The shop's router. Four questions are asked in order, and the first one answered yes decides the
     * destination. Anything none of them claims goes to the manual review queue, which is the branch
     * Camel calls otherwise.
     */
    public static RouteBuilder standard() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from(inbox())
                        .routeId("order-router")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(HIGH_VALUE).to(to("fraud-review"))
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                        .otherwise().to(to("manual-review"))
                        .end();
            }
        };
    }

    /**
     * The same four questions, with the high-value one asked last instead of first. Nothing else changes,
     * and some orders come out somewhere else.
     */
    public static RouteBuilder highValueLast() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from(inbox())
                        .routeId("order-router-high-value-last")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                            .when(HIGH_VALUE).to(to("fraud-review"))
                        .otherwise().to(to("manual-review"))
                        .end();
            }
        };
    }

    /** The same four questions, with no otherwise branch at all. */
    public static RouteBuilder noOtherwise() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from(inbox())
                        .routeId("order-router-no-otherwise")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(HIGH_VALUE).to(to("fraud-review"))
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                        .end();
            }
        };
    }

    /** An otherwise branch that names the problem: a queue for orders no question claimed. */
    public static RouteBuilder otherwiseUnclaimed() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from(inbox())
                        .routeId("order-router-unclaimed")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(HIGH_VALUE).to(to("fraud-review"))
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                        .otherwise().to(to("unclaimed"))
                        .end();
            }
        };
    }

    /** The shop's router with a fifth question added for European Union orders, asked after the other four. */
    public static RouteBuilder withEuVat() {
        return new RouteBuilder() {
            @Override
            public void configure() {
                from(inbox())
                        .routeId("order-router-with-eu-vat")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(HIGH_VALUE).to(to("fraud-review"))
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                            .when(EU).to(to("eu-vat-check"))
                        .otherwise().to(to("manual-review"))
                        .end();
            }
        };
    }

    /**
     * The shop's router with one branch that cannot finish its work: the fraud check is broken. Camel is
     * told to try each failing message three times in all and then put it on an errors queue, so that a
     * message which cannot be handled is kept rather than lost.
     */
    public static RouteBuilder fraudCheckBroken(AtomicInteger attempts) {
        return new RouteBuilder() {
            @Override
            public void configure() {
                errorHandler(deadLetterChannel(to("router-errors"))
                        .maximumRedeliveries(2)
                        .redeliveryDelay(0)
                        .logExhausted(false)
                        .logRetryAttempted(false)
                        .logHandled(false));

                from(inbox())
                        .routeId("order-router-broken-fraud-check")
                        .convertBodyTo(String.class)
                        .choice()
                            .when(HIGH_VALUE)
                                .process(exchange -> {
                                    attempts.incrementAndGet();
                                    throw new IllegalStateException("the fraud scoring service is not answering");
                                })
                            .when(DIGITAL).to(to("digital-delivery"))
                            .when(EXPRESS).to(to("express-shipping"))
                            .when(PHYSICAL).to(to("standard-shipping"))
                        .otherwise().to(to("manual-review"))
                        .end();
            }
        };
    }

    /** How many questions the shop's router asks today. */
    public static int questions() {
        return 4;
    }
}
