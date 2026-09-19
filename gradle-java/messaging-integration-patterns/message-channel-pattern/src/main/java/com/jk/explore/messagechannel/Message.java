package com.jk.explore.messagechannel;

import java.util.Map;

/** An envelope and its contents: headers that say what it is and who it is for, and a body that says what happened. */
public record Message<T>(String id, String type, Map<String, String> headers, T body) {

    public static <T> Message<T> of(String id, String type, T body) {
        return new Message<>(id, type, Map.of(), body);
    }
}
