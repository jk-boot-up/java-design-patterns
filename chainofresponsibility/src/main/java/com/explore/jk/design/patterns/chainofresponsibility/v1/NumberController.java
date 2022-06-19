package com.explore.jk.design.patterns.chainofresponsibility.v1;

import lombok.Getter;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("design-patterns/chain-of-responsibility/v1/numbers")
@Getter
public class NumberController {

    @Autowired
    @Qualifier("negativeNumberHandler")
    private IHandler handler;

    @GetMapping(value = "/{number}", produces = "application/json")
    public @ResponseBody Response printNumber(@PathVariable("number") Integer number) {
        Request request = Request.of(number);
        Response response = new Response();
        getHandler().handleRequest(request, response);
        return response;
    }




}
