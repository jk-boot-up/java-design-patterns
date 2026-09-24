package com.jk.explore.idempotentconsumerkafka;

/**
 * Stands in for the process disappearing at an exact line. In real life there is no catch
 * block; the demo catches this only so it can go on and show what the next copy is handed.
 */
public class ProcessDied extends RuntimeException {

    public ProcessDied(String where) {
        super("the process died " + where);
    }
}
