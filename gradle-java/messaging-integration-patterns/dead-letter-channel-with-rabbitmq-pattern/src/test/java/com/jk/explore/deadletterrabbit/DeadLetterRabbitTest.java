package com.jk.explore.deadletterrabbit;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.nio.charset.StandardCharsets;
import java.time.Duration;
import java.util.Set;
import org.junit.jupiter.api.Test;

class DeadLetterRabbitTest {

    @Test
    void shippingRefusesAnAddressNothingCanRead() {
        Shipping shipping = new Shipping(Set.of());
        Order garbled = Order.of("ORD-1002", "ship to ??? ?? ?????, card ending 9930");
        assertEquals("cannot read the address of ORD-1002",
                assertThrows(IllegalStateException.class, () -> shipping.accept(garbled)).getMessage());
    }

    @Test
    void aGatewayTimeoutFailsOnceAndThenWorks() {
        Shipping shipping = new Shipping(Set.of("ORD-1003"));
        Order order = Order.of("ORD-1003", "ship to 4 Harbour Road, Cork, card ending 2261");
        assertThrows(IllegalStateException.class, () -> shipping.accept(order));
        shipping.accept(order);
    }

    @Test
    void afterTheParserIsFixedTheSameOrderGoesThrough() {
        Shipping shipping = new Shipping(Set.of());
        Order garbled = Order.of("ORD-1002", "ship to ??? ?? ?????, card ending 9930");
        assertThrows(IllegalStateException.class, () -> shipping.accept(garbled));
        shipping.fixTheAddressParser();
        shipping.accept(garbled);
    }

    @Test
    void anOrderReadBackOffTheQueueIsTheOrderThatWasSent() {
        Order sent = Order.of("ORD-1001", "ship to 12 Mill Lane, Leeds, card ending 4417");
        Order read = Order.fromBody(sent.body().getBytes(StandardCharsets.UTF_8));
        assertEquals(sent, read);
        assertEquals("ORD-1001", read.id());
    }

    @Test
    void withNoContainerRuntimeTheDemoSaysWhatToDoAboutIt() {
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("container runtime"), Broker.NO_RUNTIME_ADVICE);
        assertTrue(Broker.NO_RUNTIME_ADVICE.contains("./gradlew run again"), Broker.NO_RUNTIME_ADVICE);
        assertTrue(Broker.NO_BROKER_ADVICE.contains(Broker.IMAGE), Broker.NO_BROKER_ADVICE);
        assertTrue(Broker.NO_BROKER_ADVICE.contains("./gradlew run again"), Broker.NO_BROKER_ADVICE);
    }

    @Test
    void aWaitThatNeverComesTrueFailsInsteadOfHanging() {
        String message = assertThrows(IllegalStateException.class,
                () -> Broker.waitUntil("something impossible", Duration.ofMillis(100), () -> false)).getMessage();
        assertTrue(message.contains("something impossible"), message);
        assertTrue(message.contains("gave up waiting"), message);
    }

    @Test
    void theSixActsRunAgainstARealRabbitMq() throws Exception {
        assumeTrue(Broker.dockerAvailable(), "needs a container runtime and the RabbitMQ image");
        String out = Demo.output();

        assertTrue(out.contains("handled: [ORD-1001]. still waiting: 3. deliveries of ORD-1002: 11."), out);
        assertTrue(out.contains("handled: [ORD-1001, ORD-1003, ORD-1004]. still waiting: 0. parked: 1. deliveries in all: 7."), out);
        assertTrue(out.contains("ORD-1002: reason rejected, from queue orders.work, died 1 time."), out);
        assertTrue(out.contains("the order itself is exactly as the shop sent it: ORD-1002 ship to ??? ?? ?????, card ending 9930"), out);
        assertTrue(out.contains("reason expired, from queue orders.slow."), out);
        assertTrue(out.contains("pushed the oldest out: ORD-1006, reason maxlen. still waiting there: 2."), out);
        assertTrue(out.contains("handled: [ORD-1001, ORD-1003, ORD-1004, ORD-1002]. parked: 0."), out);
        assertTrue(out.contains("20 parked, 20 shipped"), out);
        assertTrue(out.contains("the working queue reports 0 waiting"), out);
        assertTrue(out.contains("declared 11 queues and 1 exchange in 1 RabbitMQ container"), out);
    }
}
