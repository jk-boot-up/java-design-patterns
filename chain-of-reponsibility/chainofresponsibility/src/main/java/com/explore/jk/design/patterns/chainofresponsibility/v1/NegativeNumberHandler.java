package com.explore.jk.design.patterns.chainofresponsibility.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component("negativeNumberHandler")
public class NegativeNumberHandler extends AbstractHandler {

    @Autowired
    public NegativeNumberHandler(@Qualifier("zeroNumberHandler") IHandler nextHandler) {
        super.nextHandler = nextHandler;
    }

    @Override
    public void handleRequest(Request request, Response response) {
        if(request.getNumber() < 0) {
            String responseString = String.format("Number is negative: %d", request.getNumber());
            response.setResponse(String.format("Number is negative: %d", request.getNumber()));
            System.out.println(responseString);
        }
        super.handleRequest(request, response);
    }

}
