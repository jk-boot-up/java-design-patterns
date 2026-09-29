package com.jk.explore.blackboard;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;

/**
 * The pattern's organiser: repeatedly lets the cheapest ready check add to the board, and stops as soon as it can decide.
 *
 * <p>The controller knows nothing about fraud. It only knows how to ask each
 * check whether it is ready, how much it costs, and when the risk score is
 * high enough to stop.
 */
public final class Controller {

    public static final int REJECT_AT = 60;

    private final List<KnowledgeSource> sources;
    private int spentMs;
    private int ran;

    public Controller(List<KnowledgeSource> sources) {
        this.sources = sources;
    }

    public String decide(Blackboard board) {
        List<KnowledgeSource> left = new ArrayList<>(sources);
        while (board.risk() < REJECT_AT) {
            Optional<KnowledgeSource> next = left.stream().filter(s -> s.ready(board))
                    .min(Comparator.comparingInt(KnowledgeSource::costMs));
            if (next.isEmpty()) {
                return "APPROVE";
            }
            next.get().contribute(board);
            spentMs += next.get().costMs();
            ran++;
            left.remove(next.get());
        }
        return "REJECT";
    }

    public int spentMs() {
        return spentMs;
    }

    public int ran() {
        return ran;
    }
}
