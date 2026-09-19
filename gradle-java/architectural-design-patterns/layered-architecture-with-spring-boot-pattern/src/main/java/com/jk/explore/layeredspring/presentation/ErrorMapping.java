package com.jk.explore.layeredspring.presentation;

import com.jk.explore.layeredspring.domain.CheckoutRefused;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.RestControllerAdvice;

/** Turns a business refusal into an HTTP status. The domain names the reason; only this class knows the numbers. */
@RestControllerAdvice
public class ErrorMapping {

    @ExceptionHandler(CheckoutRefused.class)
    ResponseEntity<String> refused(CheckoutRefused e) {
        HttpStatus status = e.reason() == CheckoutRefused.Reason.PAYMENT_DECLINED
                ? HttpStatus.PAYMENT_REQUIRED : HttpStatus.UNPROCESSABLE_CONTENT;
        return ResponseEntity.status(status).body(e.getMessage());
    }
}
