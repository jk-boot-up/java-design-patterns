package com.jk.explore.servicemesh;

/** The version where each service carries its own retry code, written by its own team. */
public class LibraryClient {

    private final String owner;
    private final int retries;

    public LibraryClient(String owner, int retries) {
        this.owner = owner;
        this.retries = retries;
    }

    public String owner() {
        return owner;
    }

    public boolean call(Backend backend) {
        for (int attempt = 0; attempt <= retries; attempt++) {
            if (backend.call()) {
                return true;
            }
        }
        return false;
    }
}
