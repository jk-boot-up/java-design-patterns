package com.jk.explore.railway;

import java.util.function.Function;

/**
 * The two tracks: a step either succeeds with a value, or fails with a reason. Once on the failure
 * track, the remaining steps are skipped.
 */
public sealed interface Result<T> permits Result.Success, Result.Failure {

    record Success<T>(T value) implements Result<T> {
    }

    record Failure<T>(String step, String reason) implements Result<T> {
    }

    static <T> Result<T> success(T value) {
        return new Success<>(value);
    }

    static <T> Result<T> failure(String step, String reason) {
        return new Failure<>(step, reason);
    }

    /** Runs the next step only if still on the success track. The step itself may fail. */
    default <R> Result<R> flatMap(Function<T, Result<R>> next) {
        return switch (this) {
            case Success<T> s -> next.apply(s.value());
            case Failure<T> f -> new Failure<>(f.step(), f.reason());
        };
    }

    /** Applies a plain function that cannot fail, only on the success track. */
    default <R> Result<R> map(Function<T, R> plain) {
        return flatMap(value -> success(plain.apply(value)));
    }

    /** Offers a way back onto the success track after a failure. */
    default Result<T> recover(Function<Failure<T>, Result<T>> fallback) {
        return this instanceof Failure<T> f ? fallback.apply(f) : this;
    }

    /** Leaves the railway: every caller must say what to do with both tracks. */
    default <R> R fold(Function<T, R> onSuccess, Function<Failure<T>, R> onFailure) {
        return switch (this) {
            case Success<T> s -> onSuccess.apply(s.value());
            case Failure<T> f -> onFailure.apply(f);
        };
    }
}
