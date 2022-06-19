package com.explore.jk.design.patterns.chainofresponsibility.v1;

public class Client {

    private IHandler handler;

    public Client() {}

    public void handle(Request request, Response response) {
        handler.handleRequest(request, response);
    }

}
