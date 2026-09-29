package com.jk.explore.leaderfollowers;

/**
 * An incoming order message, and how long its handling takes.
 */
public record Message(String id, int workMs) {

    public static final Message STOP = new Message("STOP", 0);
}
