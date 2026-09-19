package com.jk.explore.chainspring;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

/**
 * The chain. Spring injects every {@link ScreeningCheck} already sorted by {@code @Order}, and
 * this class walks the list. A link that throws is treated as a referral, and if nobody answers
 * a named fallback does.
 */
@Component
public class ScreeningChain {

    private final List<ScreeningCheck> checks;
    private final Outcome fallback;

    public ScreeningChain(List<ScreeningCheck> checks, @Value("${screening.fallback:APPROVED}") Outcome fallback) {
        this.checks = List.copyOf(checks);
        this.fallback = fallback;
    }

    public List<String> order() {
        return checks.stream().map(ScreeningCheck::name).toList();
    }

    public Decision screen(CheckoutRequest request) {
        for (int i = 0; i < checks.size(); i++) {
            ScreeningCheck link = checks.get(i);
            StringBuilder reason = new StringBuilder();
            Optional<Outcome> answer;
            try {
                answer = link.check(request, reason);
            } catch (RuntimeException e) {
                return new Decision(Outcome.REFERRED, link.name(), link.name() + " check failed: " + e.getMessage(), notRun(i + 1));
            }
            if (answer.isPresent()) {
                return new Decision(answer.get(), link.name(), reason.toString(), notRun(i + 1));
            }
        }
        return new Decision(fallback, "fallback", "no check had an opinion", List.of());
    }

    private List<String> notRun(int from) {
        List<String> names = new ArrayList<>();
        for (int i = from; i < checks.size(); i++) {
            names.add(checks.get(i).name());
        }
        return names;
    }
}
