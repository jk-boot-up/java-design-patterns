package com.jk.explore.futurepromise.pattern;

import java.util.Arrays;
import java.util.List;
import java.util.concurrent.Callable;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Future;

/**
 * <strong>Exceptions move.</strong> A task that throws does not throw
 * where it was called — it throws, silently, on whatever worker thread
 * happened to run it, and the failure only surfaces later, wrapped, when
 * something calls {@link Future#get()}. The exception's own stack trace,
 * captured at the moment it was thrown, belongs entirely to the worker
 * thread that ran the task; no frame from the calling thread — the one
 * blocked in {@code get()} — is or can be part of it.
 */
public final class AsyncFailure {

    private AsyncFailure() {
    }

    public record Outcome(String causeMessage, String stackTop, List<String> stackFrameMethodNames) {

        /** True if no frame in the cause's own trace belongs to the given method. */
        public boolean traceOmits(String methodName) {
            return stackFrameMethodNames.stream().noneMatch(m -> m.equals(methodName));
        }
    }

    public static Outcome attempt(ExecutorService pool, Callable<?> doomedTask) {
        Future<?> future = pool.submit(doomedTask);
        try {
            future.get();
            throw new IllegalStateException("expected the doomed task to throw");
        } catch (ExecutionException e) {
            Throwable cause = e.getCause();
            StackTraceElement[] trace = cause.getStackTrace();
            List<String> methodNames = Arrays.stream(trace)
                    .map(StackTraceElement::getMethodName)
                    .toList();
            return new Outcome(cause.getMessage(), trace[0].toString(), methodNames);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException("interrupted waiting on the future", e);
        }
    }
}
