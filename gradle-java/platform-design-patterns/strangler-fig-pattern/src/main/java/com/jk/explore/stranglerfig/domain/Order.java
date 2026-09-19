package com.jk.explore.stranglerfig.domain;

import java.util.List;

public record Order(int id, List<Line> lines) {

    public long subtotalPence() {
        return lines.stream().mapToLong(Line::linePence).sum();
    }
}
