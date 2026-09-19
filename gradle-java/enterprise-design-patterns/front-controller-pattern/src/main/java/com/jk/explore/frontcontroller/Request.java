package com.jk.explore.frontcontroller;

public record Request(String method, String path, String token) {

    public static Request get(String path, String token) {
        return new Request("GET", path, token);
    }
}
