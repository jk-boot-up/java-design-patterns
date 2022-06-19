package com.explore.jk.design.patterns.chainofresponsibility.v1;

public interface IHandler {

    void handleRequest(Request request, Response response);

    IHandler getNextHandler();

}
