package com.jk.explore.chainspring;

import java.util.List;

/** The answer, who gave it, and which links never ran. */
public record Decision(Outcome outcome, String by, String reason, List<String> notRun) {
}
