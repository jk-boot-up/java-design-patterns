package com.jk.explore.pagecontrollermvc;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

/**
 * The product page's own controller: its input, its logic, its errors.
 */
@RestController
public class ProductController {

    @GetMapping("/product")
    public String product(@RequestParam String sku) {
        if (!Catalog.NAMES.containsKey(sku)) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, "no product " + sku);
        }
        return Catalog.price(sku);
    }
}
