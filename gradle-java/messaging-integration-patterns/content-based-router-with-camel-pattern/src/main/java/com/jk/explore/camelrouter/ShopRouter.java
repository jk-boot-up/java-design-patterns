package com.jk.explore.camelrouter;

import org.apache.camel.builder.RouteBuilder;
import org.apache.camel.component.springrabbit.SpringRabbitMQComponent;
import org.apache.camel.impl.DefaultCamelContext;
import org.springframework.amqp.rabbit.connection.CachingConnectionFactory;

/**
 * The running router: an Apache Camel context with one route installed in it, connected to the broker.
 *
 * <p>A Camel context is the thing that holds routes and keeps them running. Starting it makes the route
 * begin reading from the orders queue; closing it makes the route stop. Nothing in the shop's senders or
 * receivers knows this class exists.
 */
public class ShopRouter implements AutoCloseable {

    private final CachingConnectionFactory connectionFactory;
    private final DefaultCamelContext context;

    public ShopRouter(Broker broker, RouteBuilder route) {
        this.connectionFactory = new CachingConnectionFactory(broker.connectionFactory());
        this.context = new DefaultCamelContext();
        SpringRabbitMQComponent rabbit = new SpringRabbitMQComponent();
        rabbit.setConnectionFactory(connectionFactory);
        context.addComponent("spring-rabbitmq", rabbit);
        try {
            context.addRoutes(route);
        } catch (Exception e) {
            throw new IllegalStateException("the route would not install", e);
        }
        context.start();
    }

    /** How many routes this context is running. */
    public int routes() {
        return context.getRoutes().size();
    }

    /** The name the route was given, which is what Camel logs and reports it under. */
    public String routeId() {
        return context.getRoutes().get(0).getRouteId();
    }

    @Override
    public void close() {
        context.stop();
        connectionFactory.destroy();
    }
}
