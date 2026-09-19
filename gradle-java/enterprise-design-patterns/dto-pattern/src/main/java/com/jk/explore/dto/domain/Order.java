package com.jk.explore.dto.domain;

import java.util.List;

public record Order(int id, int totalPence, List<OrderLine> lines) {
}
