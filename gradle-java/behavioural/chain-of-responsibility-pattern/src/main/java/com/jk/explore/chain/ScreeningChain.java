package com.jk.explore.chain;

import java.util.ArrayList;
import java.util.List;

/**
 * An assembled chain: some links, in an order, and an answer to fall back on
 * when none of them speaks up.
 *
 * <p>The fallback is a required constructor argument. That is deliberate. An
 * order really can travel past every link and come out the far end with nobody
 * having decided anything, and in most codebases that shows up as a silent
 * {@code null}. Here the wiring has to say out loud what "nobody objected"
 * means for this chain.
 */
public final class ScreeningChain {

    private final String name;
    private final ScreeningHandler first;
    private final List<String> linkNames;
    private final Decision fallback;

    /**
     * @param fallback what this chain concludes when no link answers
     * @param links    the links, in the order they should run
     */
    public ScreeningChain(String name, Decision fallback, ScreeningHandler... links) {
        if (links.length == 0) {
            throw new IllegalArgumentException("a chain needs at least one link");
        }
        this.name = name;
        this.fallback = fallback;
        this.first = links[0];
        this.linkNames = new ArrayList<>();
        for (int i = 0; i < links.length; i++) {
            linkNames.add(links[i].name());
            links[i].linkTo(i + 1 < links.length ? links[i + 1] : null);
        }
    }

    /**
     * Hands the order to the first link and reports what came back.
     *
     * <p>Notice what is not here: no loop over the links, no index, no count.
     * The chain hands the order to the first link and does not see it again
     * until somebody answers. That is what makes reordering the checks a change
     * to this one line of wiring rather than a change to any check.
     */
    public ScreeningReport screen(CheckoutRequest request) {
        List<String> consulted = new ArrayList<>();
        Decision decision = first.screen(request, consulted).orElse(fallback);

        List<String> neverRan = new ArrayList<>(linkNames);
        neverRan.removeAll(consulted);
        return new ScreeningReport(name, decision, consulted, neverRan);
    }

    public String name() {
        return name;
    }

    /** The links in order — the first thing to look at when a verdict surprises you. */
    public List<String> linkNames() {
        return List.copyOf(linkNames);
    }

    @Override
    public String toString() {
        return name + ": " + String.join(" -> ", linkNames)
                + " -> [" + fallback.outcome() + " by default]";
    }
}
