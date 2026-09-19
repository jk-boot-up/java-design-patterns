package com.jk.explore.futurepromise.pattern;

import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import java.util.function.Supplier;

/**
 * <strong>The two halves beginners conflate, made explicit.</strong> A
 * {@link CompletableFuture} is both at once, which is exactly why the
 * distinction is easy to miss: the <em>reader</em> holds it and calls
 * {@link CompletableFuture#get()} — that half is the Future. The
 * <em>writer</em> holds the very same object and calls
 * {@link CompletableFuture#complete}, on its own thread, whenever its work
 * finishes — that half is the Promise. Neither side needs to know how the
 * other is implemented; they only share the one object standing between
 * them.
 */
public final class FutureAndPromise {

    private FutureAndPromise() {
    }

    /**
     * Runs {@code writerWork} on a brand new thread — the writer, holding
     * the Promise half — while this method itself blocks on
     * {@code future.get()} — the reader, holding the Future half. One
     * piece of code completes exactly what the other piece is waiting on.
     */
    public static <T> T handOff(Supplier<T> writerWork) {
        CompletableFuture<T> future = new CompletableFuture<>();

        Thread writer = new Thread(() -> {
            T result = writerWork.get();
            future.complete(result);
        }, "writer");
        writer.start();

        try {
            return future.get();
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted waiting on the future", e);
        } catch (ExecutionException e) {
            throw new IllegalStateException("the writer's work failed", e);
        } finally {
            try {
                writer.join();
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
    }
}
