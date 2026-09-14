package com.jk.explore.saga;

import java.util.ArrayList;
import java.util.List;

/**
 * The orchestrator: one place that knows the order of the steps and what to do when one of
 * them fails.
 *
 * The whole algorithm is in {@link #run}, and it is short. Walk the steps forward, keeping a
 * list of the ones that succeeded. If one throws, stop, and walk that list backwards calling
 * {@code compensate} on each. That is a saga.
 *
 * <p>Two details are what separate this from a {@code try/catch} that happens to work.
 *
 * <p><b>Compensation runs in reverse.</b> Not for tidiness — because later steps can depend
 * on earlier ones. The order has to be cancelled before the payment is refunded, or finance
 * is briefly looking at a confirmed order with no money against it.
 *
 * <p><b>A compensation can itself fail.</b> When it does, this class does not swallow it and
 * does not abandon the rest of the unwinding either: it records the step it could not undo,
 * carries on compensating the others, and reports
 * {@link SagaOutcome.Status#NEEDS_HUMAN_HELP}. In a real shop that outcome is a row in a
 * queue that a person works through, and building the saga without one is choosing not to
 * find out when the shop has taken money it cannot return.
 *
 * <p><b>Orchestration versus choreography.</b> This class is the orchestrator: it holds the
 * sequence, so the sequence can be read in one place and tested in one place, at the price of
 * every service knowing the orchestrator exists. The alternative, choreography, has each
 * service publish an event and the next react to it — nothing is in charge, which couples the
 * services less and means nobody can answer "what happens when an order is placed" without
 * reading five codebases. For a flow this important, being able to read it in one file is
 * usually worth more.
 */
public final class SagaOrchestrator {

    private final List<SagaStep> steps;
    private final CallLog log;

    public SagaOrchestrator(List<SagaStep> steps, CallLog log) {
        this.steps = List.copyOf(steps);
        this.log = log;
    }

    /** Runs the saga, compensating in reverse if a step fails. Never throws. */
    public SagaOutcome run(SagaContext context) {
        List<SagaStep> done = new ArrayList<>();

        for (SagaStep step : steps) {
            try {
                step.execute(context);
                done.add(step);
                log.note("Saga", "STEP-OK", step.name());
            } catch (RuntimeException failure) {
                log.note("Saga", "STEP-FAILED", step.name() + ": " + failure.getMessage());
                return unwind(context, step, done);
            }
        }

        log.note("Saga", "COMPLETED", context.orderId() + " for " + context.total());
        return new SagaOutcome(context.orderId(), SagaOutcome.Status.COMPLETED, null,
                List.of(), List.of());
    }

    private SagaOutcome unwind(SagaContext context, SagaStep failed, List<SagaStep> done) {
        List<String> compensated = new ArrayList<>();
        List<String> couldNot = new ArrayList<>();

        for (int i = done.size() - 1; i >= 0; i--) {
            SagaStep step = done.get(i);
            if (!step.canBeCompensated()) {
                couldNot.add(step.name());
                log.note("Saga", "NO-UNDO", step.name() + " cannot be undone at all");
                continue;
            }
            try {
                step.compensate(context);
                compensated.add(step.name());
                log.note("Saga", "UNDONE", step.name());
            } catch (RuntimeException alsoFailed) {
                couldNot.add(step.name());
                log.note("Saga", "UNDO-FAILED",
                        step.name() + ": " + alsoFailed.getMessage());
            }
        }

        if (couldNot.isEmpty()) {
            log.note("Saga", "COMPENSATED", "everything undone, customer owes nothing");
            return new SagaOutcome(context.orderId(), SagaOutcome.Status.COMPENSATED,
                    failed.name(), List.copyOf(compensated), List.of());
        }

        log.note("Saga", "NEEDS-HUMAN", "could not undo " + couldNot);
        return new SagaOutcome(context.orderId(), SagaOutcome.Status.NEEDS_HUMAN_HELP,
                failed.name(), List.copyOf(compensated), List.copyOf(couldNot));
    }
}
