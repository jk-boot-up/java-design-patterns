package com.jk.explore.blackboard;

/**
 * One independent check. It says when it has what it needs, and then adds what it knows to the board.
 */
public interface KnowledgeSource {

    String name();

    /** How long this check takes, in milliseconds. */
    int costMs();

    /** True when the facts this check needs are on the board and its own answer is not there yet. */
    boolean ready(Blackboard board);

    void contribute(Blackboard board);
}
