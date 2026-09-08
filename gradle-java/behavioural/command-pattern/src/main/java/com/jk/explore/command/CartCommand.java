package com.jk.explore.command;

/**
 * The command: one edit to a cart, turned into an object.
 *
 * <p>The whole pattern is the pair of methods. {@code execute} makes the
 * change; {@code undo} puts the cart back exactly as it was. A method call
 * that has already returned cannot be undone, which is the reason the
 * request has to become a thing you can hold.
 *
 * <p>Three rules the implementations here all keep, and which are worth
 * stating because breaking any of them is where undo bugs come from:
 *
 * <ul>
 *   <li><strong>A command records what it needs to reverse itself during
 *   {@code execute}, not before.</strong> Deciding "this add will merge
 *   into an existing line" when the command is constructed is a guess about
 *   the state of a cart that has not been reached yet, and by the time the
 *   command runs, an earlier undo may have made it wrong.</li>
 *   <li><strong>{@code undo} is only ever called on a command that has
 *   executed</strong>, and only when the cart is in the state that command
 *   left it in. {@link CartHistory} is what guarantees that.</li>
 *   <li><strong>Nothing is stored in the command that the cart also
 *   owns.</strong> Commands hold values — a SKU, a quantity, a coupon —
 *   never a live line the cart might have replaced underneath them.</li>
 * </ul>
 */
public interface CartCommand {

    /** What this command does, in one line, for the history and the log. */
    String describe();

    /** Applies the edit, recording whatever {@link #undo} will need. */
    void execute(Cart cart);

    /** Puts the cart back exactly as it was before {@link #execute}. */
    void undo(Cart cart);
}
