package com.jk.explore.copyonwrite;

import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

/**
 * The pattern, written out: readers use the current array with no lock; a writer copies it, changes the copy, and swaps it in.
 *
 * <p>The array is never changed once published, so a reader half-way through
 * it can never be disturbed. Java's own {@code CopyOnWriteArrayList} works
 * the same way.
 */
public final class CowList<T> implements Iterable<T> {

    private volatile Object[] items = new Object[0];
    private long elementsCopied;

    /** Writers take turns, and each makes a whole new array. */
    public synchronized void add(T item) {
        Object[] next = Arrays.copyOf(items, items.length + 1);
        elementsCopied += items.length;
        next[items.length] = item;
        items = next;
    }

    public synchronized void remove(T item) {
        Object[] current = items;
        for (int i = 0; i < current.length; i++) {
            if (current[i].equals(item)) {
                Object[] next = new Object[current.length - 1];
                System.arraycopy(current, 0, next, 0, i);
                System.arraycopy(current, i + 1, next, i, current.length - i - 1);
                elementsCopied += current.length - 1;
                items = next;
                return;
            }
        }
    }

    /** Readers take the array as it is right now: a snapshot nobody will change. */
    @Override
    @SuppressWarnings("unchecked")
    public Iterator<T> iterator() {
        return (Iterator<T>) List.of(items).iterator();
    }

    public int size() {
        return items.length;
    }

    public long elementsCopied() {
        return elementsCopied;
    }
}
