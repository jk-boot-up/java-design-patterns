package com.jk.explore.command;

import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.Objects;

/**
 * The invoker: runs commands against one cart and remembers them.
 *
 * <p>Read this class looking for the names of the commands. There are none.
 * It has never heard of coupons or quantities; it holds
 * {@link CartCommand}s, and the only two things it knows how to do with one
 * are execute it and undo it. That is why adding a fifth kind of edit does
 * not touch this file.
 *
 * <p>The two stacks are the whole of undo and redo. Executing something new
 * clears the redo stack, because once you have taken a different branch the
 * old future is not reachable any more — the same rule every text editor in
 * the world follows.
 */
public final class CartHistory {

    private final Cart cart;
    private final Deque<CartCommand> done = new ArrayDeque<>();
    private final Deque<CartCommand> undone = new ArrayDeque<>();

    public CartHistory(Cart cart) {
        this.cart = Objects.requireNonNull(cart, "cart");
    }

    /**
     * Runs a command and records it.
     *
     * <p>If the command throws, it is not recorded: a command that failed
     * halfway is not on the undo stack, because undoing it would apply the
     * reverse of something that never fully happened.
     */
    public void execute(CartCommand command) {
        Objects.requireNonNull(command, "command").execute(cart);
        done.push(command);
        undone.clear();
    }

    /** Reverses the most recent command. Returns false when there is nothing to undo. */
    public boolean undo() {
        if (done.isEmpty()) {
            return false;
        }
        CartCommand command = done.pop();
        command.undo(cart);
        undone.push(command);
        return true;
    }

    /** Re-runs the most recently undone command. Returns false when there is nothing to redo. */
    public boolean redo() {
        if (undone.isEmpty()) {
            return false;
        }
        CartCommand command = undone.pop();
        command.execute(cart);
        done.push(command);
        return true;
    }

    public boolean canUndo() {
        return !done.isEmpty();
    }

    public boolean canRedo() {
        return !undone.isEmpty();
    }

    /**
     * What has been done, oldest first — the audit trail the pattern gives
     * away for free, because every edit is already an object that can say
     * what it is.
     */
    public List<String> log() {
        List<String> entries = new ArrayList<>();
        for (CartCommand command : done) {
            entries.add(0, command.describe());
        }
        return List.copyOf(entries);
    }

    /** How many commands can still be undone. */
    public int undoDepth() {
        return done.size();
    }
}
