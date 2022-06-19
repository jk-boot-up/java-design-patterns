package com.explore.jk.design.patterns.chainofresponsibility.v1;

import org.springframework.stereotype.Component;

@Component("positiveNumberHandler")
public class PositiveNumberHandler extends AbstractHandler {

    public PositiveNumberHandler() {
        // nextHandler is null;
    }

    @Override
    public void handleRequest(Request request, Response response) {
        if(request.getNumber() > 0) {
            String responseString = String.format("Number is positive: %d", request.getNumber());
            response.setResponse(String.format("Number is positive: %d", request.getNumber()));
            System.out.println(responseString);
        }
        super.handleRequest(request, response);
    }

}
