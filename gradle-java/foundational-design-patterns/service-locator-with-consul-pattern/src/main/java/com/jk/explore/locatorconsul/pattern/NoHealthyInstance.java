package com.jk.explore.locatorconsul.pattern;

/** The locator has nothing to give: nothing registered, or nothing healthy. Found at run time. */
public class NoHealthyInstance extends RuntimeException {

    public NoHealthyInstance(String serviceName) {
        super("no healthy instance of \"" + serviceName + "\"");
    }
}
