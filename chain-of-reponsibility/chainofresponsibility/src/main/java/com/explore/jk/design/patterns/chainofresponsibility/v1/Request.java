package com.explore.jk.design.patterns.chainofresponsibility.v1;

import lombok.Getter;


@Getter
public class Request {

    private Integer number;

    private Request(Integer number) {
        this.number = number;
    }

    public static Request of(Integer number) {
        return new Request(number);
    }


}
