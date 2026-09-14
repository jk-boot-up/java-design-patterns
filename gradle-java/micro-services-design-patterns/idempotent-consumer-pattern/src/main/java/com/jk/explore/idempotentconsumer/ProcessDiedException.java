package com.jk.explore.idempotentconsumer;

/**
 * The process stopping mid-method, for a reason nothing in this codebase controls.
 *
 * In real life there is no exception and no catch block, because the JVM is gone. It is
 * modelled as one only so that a demo can carry on afterwards and show you what was left
 * behind.
 */
public class ProcessDiedException extends RuntimeException {

    public ProcessDiedException(String where) {
        super("the process died " + where);
    }
}
