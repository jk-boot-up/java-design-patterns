package com.jk.explore.hexagonalspring.adapter.driving;

import com.jk.explore.hexagonalspring.core.port.PlaceOrder;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/** A second driving adapter, for the same port: a file of lines placed one after another. */
@Component
public class CsvBatch {

    private final PlaceOrder placeOrder;

    public CsvBatch(PlaceOrder placeOrder) {
        this.placeOrder = placeOrder;
    }

    public List<String> run(List<String> lines) {
        List<String> results = new ArrayList<>();
        for (String line : lines) {
            String[] parts = line.split(",");
            try {
                results.add(placeOrder.place(parts[0], parts[1], Integer.parseInt(parts[2])).orderId());
            } catch (RuntimeException e) {
                results.add("refused");
            }
        }
        return results;
    }
}
