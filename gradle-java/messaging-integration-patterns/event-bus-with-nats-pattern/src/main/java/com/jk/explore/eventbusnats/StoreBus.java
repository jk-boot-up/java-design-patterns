package com.jk.explore.eventbusnats;

import static java.nio.charset.StandardCharsets.UTF_8;

import io.nats.client.Connection;
import io.nats.client.Dispatcher;
import io.nats.client.ErrorListener;
import io.nats.client.Message;
import io.nats.client.Nats;
import io.nats.client.Options;
import java.time.Duration;
import java.util.concurrent.CancellationException;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.TimeoutException;
import java.util.function.Consumer;

/**
 * One store service's link to the bus.
 *
 * <p>Publishing hands an event to the server under a name and returns at once. The publisher is never told
 * who was listening, or whether anybody was. Subscribing asks the server to send this link every event
 * published under a name, from that moment on. Nothing earlier is available, because nothing is kept.
 */
public class StoreBus implements AutoCloseable {

    private final String name;
    private final Connection connection;

    public StoreBus(String name, String url) throws Exception {
        this.name = name;
        this.connection = Nats.connect(new Options.Builder()
                .server(url)
                .connectionTimeout(Duration.ofSeconds(30))
                .noReconnect()
                // A subscriber that throws is act four's whole point, so the client's own logging of it is
                // turned off here and the demo reports it instead.
                .errorListener(new ErrorListener() {
                })
                .build());
    }

    public String name() {
        return name;
    }

    /** Puts one event on the bus under a name, and returns without waiting for anybody. */
    public void publish(String subject, String event) {
        connection.publish(subject, event.getBytes(UTF_8));
    }

    /**
     * Asks the server to start sending this link every event published under a name, and waits until the
     * server has actually agreed. Without that wait an event published a moment later can arrive before
     * the request to listen does, and be lost.
     */
    public StoreSubscriber subscribe(String listener, String subject) throws Exception {
        StoreSubscriber subscriber = new StoreSubscriber(listener, connection.subscribe(subject));
        settle();
        return subscriber;
    }

    /** The same, but reacting in a handler rather than waiting in a loop. */
    public void onEvent(String subject, Consumer<String> handler) throws Exception {
        Dispatcher dispatcher = connection.createDispatcher(m -> handler.accept(new String(m.getData(), UTF_8)));
        dispatcher.subscribe(subject);
        settle();
    }

    /**
     * Waits for the server to confirm everything asked of it so far. This is a real round trip, not a pause:
     * it returns as soon as the server answers, and fails rather than hanging if the server never does.
     */
    public void settle() throws Exception {
        connection.flush(Duration.ofSeconds(20));
    }

    /**
     * Asks a question under a name and waits for an answer, rather than telling and walking away.
     * When nobody is listening the server says so immediately, which is the only way this bus ever
     * admits that an event went nowhere.
     */
    public String ask(String subject, String question) {
        CompletableFuture<Message> answer = connection.request(subject, question.getBytes(UTF_8));
        try {
            return new String(answer.get(10, TimeUnit.SECONDS).getData(), UTF_8);
        } catch (CancellationException e) {
            return "no responders";
        } catch (TimeoutException e) {
            answer.cancel(true);
            return "no answer within 10 seconds";
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        } catch (Exception e) {
            throw new IllegalStateException(e);
        }
    }

    @Override
    public void close() throws Exception {
        connection.close();
    }
}
