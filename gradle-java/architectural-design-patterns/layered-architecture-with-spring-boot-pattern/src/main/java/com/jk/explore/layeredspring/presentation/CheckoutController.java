package com.jk.explore.layeredspring.presentation;

import com.jk.explore.layeredspring.application.PlaceOrderRequest;
import com.jk.explore.layeredspring.application.PlaceOrderResult;
import com.jk.explore.layeredspring.application.PlaceOrderService;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestController;

/** The presentation layer: it talks to the application layer, and to nothing below it. */
@RestController
public class CheckoutController {

    private final PlaceOrderService service;

    public CheckoutController(PlaceOrderService service) {
        this.service = service;
    }

    @PostMapping("/orders")
    @ResponseStatus(HttpStatus.CREATED)
    public PlaceOrderResult place(@RequestBody PlaceOrderRequest request) {
        return service.place(request);
    }
}
