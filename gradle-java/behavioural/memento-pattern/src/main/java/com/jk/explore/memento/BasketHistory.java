package com.jk.explore.memento;

import java.util.ArrayDeque;
import java.util.Deque;

/**
 * The undo stack — the caretaker.
 *
 * <p>Read this class looking for something it cannot do. It holds snapshots,
 * it stacks them up, and it hands them back. It never reads one, because the
 * methods that would let it are not visible from a class that only has the
 * public interface in view. Undo works here without this class knowing that a
 * basket contains lines, or a voucher, or anything else.
 *
 * <p>Snapshots are capped, because they are complete copies and a shopper who
 * spends an hour on a basket should not accumulate an hour of them.
 */
public class BasketHistory {

    private static final int MAX_UNDO_STEPS = 20;

    private final Deque<BasketSnapshot> undoStack = new ArrayDeque<>();

    /** Call this <em>before</em> the change described by {@code label}. */
    public void record(Basket basket, String label) {
        undoStack.push(basket.save(label));
        if (undoStack.size() > MAX_UNDO_STEPS) {
            undoStack.removeLast();
        }
    }

    public boolean canUndo() {
        return !undoStack.isEmpty();
    }

    public int size() {
        return undoStack.size();
    }

    /** Steps the basket back one change, and says which one it undid. */
    public String undo(Basket basket) {
        if (undoStack.isEmpty()) {
            throw new IllegalStateException("nothing to undo");
        }
        BasketSnapshot snapshot = undoStack.pop();
        basket.restore(snapshot);
        return snapshot.label();
    }
}
