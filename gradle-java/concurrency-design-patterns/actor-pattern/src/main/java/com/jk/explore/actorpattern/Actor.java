package com.jk.explore.actorpattern;

import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.TimeUnit;
import java.util.concurrent.atomic.AtomicInteger;

/**
 * An actor: state that only it touches, a mailbox, and one thread that takes messages from the mailbox one at a
 * time. Other code cannot call its methods. It can only send a message, and wait for a reply message if it asks for one.
 * If handling a message throws, the actor's supervisor decides what to do: here, it is restarted with fresh state.
 */
public abstract class Actor implements AutoCloseable {

    /** A message and, if the sender wants an answer, where to put it. */
    protected record Envelope(Object message, CompletableFuture<Object> replyTo) {
    }

    private final BlockingQueue<Envelope> mailbox = new LinkedBlockingQueue<>();
    private final Thread thread;
    private final AtomicInteger restarts = new AtomicInteger();
    private final AtomicInteger handled = new AtomicInteger();
    private volatile boolean running = true;

    protected Actor(String name) {
        thread = new Thread(this::loop, name);
    }

    /** Starts the actor's thread. Called once, after the subclass is fully built. */
    public final void start() {
        thread.start();
    }

    /** Sends and carries on. */
    public final void tell(Object message) {
        mailbox.add(new Envelope(message, null));
    }

    /** Sends, and returns a promise of the reply. */
    public final CompletableFuture<Object> ask(Object message) {
        CompletableFuture<Object> reply = new CompletableFuture<>();
        mailbox.add(new Envelope(message, reply));
        return reply;
    }

    /** Handles one message, on the actor's own thread. The return value is the reply, if one was asked for. */
    protected abstract Object receive(Object message);

    /** Called when handling a message threw: put the actor's state back to how it starts. */
    protected abstract void restart();

    private void loop() {
        while (running) {
            Envelope e;
            try {
                e = mailbox.poll(20, TimeUnit.MILLISECONDS);
            } catch (InterruptedException ex) {
                return;
            }
            if (e == null) {
                continue;
            }
            try {
                Object reply = receive(e.message());
                handled.incrementAndGet();
                if (e.replyTo() != null) {
                    e.replyTo().complete(reply);
                }
            } catch (RuntimeException ex) {
                restarts.incrementAndGet();
                restart();
                if (e.replyTo() != null) {
                    e.replyTo().completeExceptionally(ex);
                }
            }
        }
    }

    public final int restarts() {
        return restarts.get();
    }

    public final int handled() {
        return handled.get();
    }

    public final int mailboxSize() {
        return mailbox.size();
    }

    @Override
    public void close() {
        running = false;
        thread.interrupt();
        try {
            thread.join();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }
}
