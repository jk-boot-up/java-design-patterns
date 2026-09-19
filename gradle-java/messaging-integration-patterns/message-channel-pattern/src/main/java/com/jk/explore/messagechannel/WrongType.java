package com.jk.explore.messagechannel;

public class WrongType extends RuntimeException {
    public WrongType(String channel, String expected, String got) {
        super("channel " + channel + " carries " + expected + " but was given " + got);
    }
}
