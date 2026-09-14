package com.jk.explore.apigateway;

/** Who is asking. Produced by checking an access token. */
public record Customer(String id) {

    @Override
    public String toString() {
        return id;
    }
}
