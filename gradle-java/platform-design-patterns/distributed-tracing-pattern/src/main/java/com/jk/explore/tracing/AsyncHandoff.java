package com.jk.explore.tracing;

import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;

/**
 * The second item on the bill: context lost when work moves to another thread.
 *
 * <p>This is the failure that catches everybody, including people who have used
 * tracing for years, and the reason is that real tracing libraries are helpful.
 * They keep the current context in a thread-local so that your method signatures
 * do not have to carry it. That works beautifully right up until the work moves
 * to a different thread — a thread pool, a {@code CompletableFuture}, a
 * scheduled job — because a thread-local belongs to a thread, and the new thread
 * has its own, which is empty.
 *
 * <p>The code that breaks looks exactly like the code that works. There is no
 * error. There is no warning. There is simply a span with no parent, sitting on
 * its own, and a trace that stops one level short of wherever the time actually
 * went.
 *
 * <p>This class shows it both ways round. {@link #withThreadLocalContext()}
 * loses the trace; {@link #withExplicitContext()} keeps it, by doing the one
 * thing that always works: capturing the context on the calling thread and
 * handing it to the task as an ordinary value.
 */
public final class AsyncHandoff {

    /**
     * The helpful thread-local that is about to be unhelpful.
     *
     * <p>A real library's version of this is more sophisticated and fails in
     * precisely the same way.
     */
    private static final ThreadLocal<TraceContext> CURRENT = new ThreadLocal<>();

    private AsyncHandoff() {
    }

    /**
     * Fetch the recommendations strip on a worker thread, relying on the
     * thread-local to carry the context.
     *
     * <p>It does not carry. The worker thread's {@code CURRENT} was never set,
     * so the strip's span is created with no parent, and the trace comes back
     * with two roots — the page, and an orphan that belongs to nobody.
     *
     * @return the trace, which will be missing its link
     */
    public static Trace withThreadLocalContext() {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer("trace-async-broken", clock);

        try (Tracer.Scope page = tracer.startRoot("product-page")) {
            CURRENT.set(page.context());
            try {
                runOnAnotherThread(() -> {
                    // On the worker thread this is null, because thread-locals
                    // do not travel. The code reads as though it does.
                    TraceContext inherited = CURRENT.get();

                    if (inherited == null) {
                        try (Tracer.Scope orphan = tracer.startRoot("recommendations")) {
                            clock.advance(ProductPage.RECOMMENDATIONS_MS);
                        }
                    } else {
                        try (Tracer.Scope strip = tracer.start(inherited, "recommendations")) {
                            clock.advance(ProductPage.RECOMMENDATIONS_MS);
                        }
                    }
                });
            } finally {
                CURRENT.remove();
            }
        }
        return tracer.trace();
    }

    /**
     * The same handoff, with the context passed as a value.
     *
     * <p>The fix is unglamorous and total: read the context on the thread that
     * has it, close over it, and hand it to the task. A value does not care
     * which thread reads it. Every real tracing library offers a wrapper that
     * does this for you, and the reason to see it written out once is so that
     * the wrapper stops being magic.
     */
    public static Trace withExplicitContext() {
        Clock.Scripted clock = new Clock.Scripted();
        Tracer tracer = new Tracer("trace-async-fixed", clock);

        try (Tracer.Scope page = tracer.startRoot("product-page")) {

            // Captured here, on the thread that actually has it.
            TraceContext captured = page.context();

            runOnAnotherThread(() -> {
                try (Tracer.Scope strip = tracer.start(captured, "recommendations")) {
                    clock.advance(ProductPage.RECOMMENDATIONS_MS);
                }
            });
        }
        return tracer.trace();
    }

    /**
     * Run the task on a different thread and wait for it.
     *
     * <p>Waiting keeps the demo deterministic — the scripted clock is not
     * thread-safe, and this project would rather be readable than concurrent.
     * The trace still breaks exactly as it would under a real thread pool,
     * because what breaks it is the thread change, not the parallelism.
     */
    private static void runOnAnotherThread(Runnable task) {
        try (ExecutorService worker = Executors.newSingleThreadExecutor()) {
            Future<?> done = worker.submit(task);
            done.get();
        } catch (InterruptedException interrupted) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted waiting for the worker", interrupted);
        } catch (java.util.concurrent.ExecutionException failed) {
            throw new IllegalStateException("the worker failed", failed.getCause());
        }
    }
}
