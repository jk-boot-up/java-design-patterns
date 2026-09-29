package com.jk.explore.requestreply;

import java.util.Map;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * The pattern: every request gets a unique ID and a return address; every reply names the request it answers.
 *
 * <p>The requester keeps a table of requests waiting for an answer. A
 * listener takes each reply from this requester's own reply queue, looks up its
 * correlation ID, and completes the matching request, whatever order replies
 * arrive in.
 */
public final class Requester implements AutoCloseable {

    private final String name;
    private final BlockingQueue<Message> requests;
    private final BlockingQueue<Message> myReplies = new LinkedBlockingQueue<>();
    private final Map<String, CompletableFuture<String>> pending = new ConcurrentHashMap<>();
    private final AtomicInteger next = new AtomicInteger();
    private final Thread listener;

    public Requester(String name, BlockingQueue<Message> requests) {
        this.name = name;
        this.requests = requests;
        listener = new Thread(() -> {
            try {
                while (true) {
                    Message reply = myReplies.take();
                    CompletableFuture<String> waiting = pending.remove(reply.correlationId());
                    if (waiting != null) {
                        waiting.complete(reply.body());
                    }
                }
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        });
        listener.setDaemon(true);
        listener.start();
    }

    /** Sends a request and returns its ID and a future answer. */
    public Sent send(String body) {
        String id = name + "-" + next.incrementAndGet();
        CompletableFuture<String> answer = new CompletableFuture<>();
        pending.put(id, answer);
        requests.add(new Message(id, null, myReplies, body));
        return new Sent(id, answer);
    }

    public record Sent(String id, CompletableFuture<String> answer) {
        public String await(long ms) {
            try {
                return answer.get(ms, TimeUnit.MILLISECONDS);
            } catch (java.util.concurrent.TimeoutException e) {
                return "no reply after " + ms + " ms";
            } catch (Exception e) {
                return "failed";
            }
        }
    }

    public int pending() {
        return pending.size();
    }

    public void forget(String id) {
        pending.remove(id);
    }

    @Override
    public void close() {
        listener.interrupt();
    }
}
