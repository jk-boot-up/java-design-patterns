package com.explore.jk.design.patterns.chainofresponsibility.v1;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component("zeroNumberHandler")
public class ZeroNumberHandler extends AbstractHandler {

    @Autowired
    public ZeroNumberHandler(@Qualifier("positiveNumberHandler") IHandler nextHandler) {
        super.nextHandler = nextHandler;
    }

    @Override
    public void handleRequest(Request request, Response response) {
        if(request.getNumber() == 0) {
            String responseString = String.format("Number is zero: %d", request.getNumber());
            response.setResponse(String.format("Number is zero: %d", request.getNumber()));
            System.out.println(responseString);
        }
        super.handleRequest(request, response);
    }

}
