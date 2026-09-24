package com.jk.explore.transactionaloutboxdebezium;

/**
 * Stands in for a process disappearing at an exact line. In real life there is no catch
 * block; the demo catches this only so it can go on and show what was left behind.
 */
public class ProcessDied extends RuntimeException {

    public ProcessDied(String where) {
        super("the process died " + where);
    }
}
