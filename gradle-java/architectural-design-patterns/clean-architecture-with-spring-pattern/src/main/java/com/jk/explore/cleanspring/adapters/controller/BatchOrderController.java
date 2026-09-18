package com.jk.explore.cleanspring.adapters.controller;

import com.jk.explore.cleanspring.usecases.PlaceOrderInput;
import com.jk.explore.cleanspring.usecases.PlaceOrderInput.RequestedLine;
import com.jk.explore.cleanspring.usecases.PlaceOrderInputBoundary;
import com.jk.explore.cleanspring.usecases.PlaceOrderOutput;

import java.util.ArrayList;
import java.util.List;

/**
 * <strong>Half of the forced change: an entirely new delivery mechanism.</strong>
 * Reads one or more CSV-shaped lines — the kind a nightly batch import
 * would hand in — and places one order per line. It depends on
 * {@link PlaceOrderInputBoundary}, exactly as {@link CheckoutController}
 * does, and {@code PlaceOrderInteractor} needed no change at all to accept
 * a second caller.
 */
public class BatchOrderController {

    private final PlaceOrderInputBoundary placeOrder;

    public BatchOrderController(PlaceOrderInputBoundary placeOrder) {
        this.placeOrder = placeOrder;
    }

    /** One CSV row: {@code customerId,contact,SKU:qty|SKU:qty}. */
    public List<String> importBatch(List<String> csvRows) {
        List<String> results = new ArrayList<>();
        for (String row : csvRows) {
            String[] fields = row.split(",", 3);
            String[] rawLines = fields[2].split("\\|");
            RequestedLine[] lines = new RequestedLine[rawLines.length];
            for (int i = 0; i < rawLines.length; i++) {
                String[] skuAndQty = rawLines[i].split(":");
                lines[i] = new RequestedLine(skuAndQty[0], Integer.parseInt(skuAndQty[1]));
            }
            PlaceOrderOutput output = placeOrder.execute(
                    PlaceOrderInput.of(fields[0], fields[1], lines));
            results.add(output.placed()
                    ? "IMPORTED " + output.orderId() + " " + output.total()
                    : "SKIPPED " + output.reason());
        }
        return results;
    }
}
