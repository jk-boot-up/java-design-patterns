package com.jk.explore.prototype;

/**
 * Something that can produce a fully independent copy of itself.
 *
 * <p>This is the Gang of Four Prototype role, written as an ordinary
 * interface with an ordinary method name rather than as Java's built-in
 * {@code Cloneable}. <i>Effective Java</i>, Item 13, is blunt about why:
 * {@code Cloneable} carries no method of its own, {@code Object.clone()} is
 * protected and throws a checked {@code CloneNotSupportedException} for no
 * good reason, and the copy it produces is shallow whether that is safe or
 * not. A plain {@code copy()} method has none of that baggage — it is just
 * a method, so it can be typed, tested, and documented like any other.
 *
 * @param <T> the concrete type being copied
 */
public interface Prototype<T> {

    /**
     * Returns a new, fully independent instance with the same state as this
     * one. "Fully independent" means mutating the copy — or continuing to
     * mutate the original — must never be visible through the other one.
     */
    T copy();
}
