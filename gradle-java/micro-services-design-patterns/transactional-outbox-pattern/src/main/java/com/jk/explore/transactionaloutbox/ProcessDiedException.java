package com.jk.explore.transactionaloutbox;

/**
 * The process stopping, mid-method, for a reason nothing in this codebase controls.
 *
 * A deploy rolls the pod. The machine runs out of memory. Somebody's laptop closes on the
 * cable. This is not an error the code can catch and handle sensibly — in real life the
 * catch block never runs at all, because the JVM is gone. It is modelled as an exception
 * only because a demo has to keep running afterwards to show you what was left behind.
 *
 * <p>Every "it works on my machine" bug in this project is this exception landing between
 * two lines that looked like one.
 */
public class ProcessDiedException extends RuntimeException {

    public ProcessDiedException(String where) {
        super("the process died " + where);
    }
}
