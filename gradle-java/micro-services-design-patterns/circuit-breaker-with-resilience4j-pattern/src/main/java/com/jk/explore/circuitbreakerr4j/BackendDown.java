package com.jk.explore.circuitbreakerr4j;

public class BackendDown extends RuntimeException {
    public BackendDown() {
        super("recommendations service is not answering");
    }
}
