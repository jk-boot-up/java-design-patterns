package com.explore.jk.design.patterns.chainofresponsibility.v1;

public  abstract class AbstractHandler implements IHandler {

    protected IHandler nextHandler;

    @Override
    public void handleRequest(Request request, Response response) {
        if(getNextHandler() != null) {
            getNextHandler().handleRequest(request, response);
        }
    }

    @Override
    public IHandler getNextHandler() {
        return nextHandler;
    }
}
