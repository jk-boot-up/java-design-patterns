package com.jk.explore.chain;

import java.util.List;
import java.util.Optional;

/**
 * One link in the screening chain. This class is the pattern.
 *
 * <p>A handler knows two things and no more: how to look at one order, and who
 * comes after it. It does not know how many links there are, which one is
 * first, or whether it is the last. That ignorance is the point — it is what
 * lets the same checks be put in a different order without any of them being
 * edited.
 *
 * <p>To write a link you fill in {@link #check}. Return a {@link Decision} to
 * say "I am answering this, stop here", or return {@code Optional.empty()} to
 * say "no objection from me, ask the next one".
 */
public abstract class ScreeningHandler {

    /** The link that runs after this one, or null if this is the last. */
    private ScreeningHandler next;

    /** The name that appears in the report, so a decision can be traced. */
    public abstract String name();

    /**
     * Look at the order.
     *
     * @return the decision this link is making, or empty to pass the order on
     */
    protected abstract Optional<Decision> check(CheckoutRequest request);

    /**
     * Runs this link, and the rest of the chain behind it.
     *
     * <p>This method is {@code final} on purpose. In the textbook version every
     * handler writes {@code if (canHandle) ... else next.handle(request)} for
     * itself, and the bug everybody eventually hits is a handler that declines
     * and forgets the {@code else} — the order vanishes with nothing thrown.
     * Writing it once, here, makes that impossible.
     *
     * @param consulted collects the names of the links that actually ran
     * @return the decision that stopped the chain, or empty if nobody decided
     */
    final Optional<Decision> screen(CheckoutRequest request, List<String> consulted) {
        consulted.add(name());
        Optional<Decision> mine = check(request);
        if (mine.isPresent()) {
            return mine;
        }
        return next == null ? Optional.empty() : next.screen(request, consulted);
    }

    /** Package-private: only {@link ScreeningChain} joins links together. */
    final void linkTo(ScreeningHandler next) {
        this.next = next;
    }

    @Override
    public String toString() {
        return name();
    }
}
