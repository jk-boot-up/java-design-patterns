package com.jk.explore.mvcspring;

import java.util.List;

public record Order(String id, String customer, List<Line> lines) {
}
