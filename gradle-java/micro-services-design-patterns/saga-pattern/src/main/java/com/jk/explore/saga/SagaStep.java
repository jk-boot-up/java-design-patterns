package com.jk.explore.saga;

/**
 * One step of a saga, together with the action that cancels it out.
 *
 * If this looks familiar, it should: {@link #execute} and {@link #compensate} are Command's
 * {@code execute} and {@code undo} under different names. The structure is the same, and so
 * is the reason for it — an operation that carries its own reversal can be sequenced,
 * logged and unwound by code that knows nothing about what any particular one does.
 *
 * <p>There is one difference, and everything difficult about sagas lives in it. An
 * in-memory {@code undo} always works. A compensation is a call to somebody else's service
 * over a network, so it can be slow, it can be refused, and it can fail outright. A saga
 * has to have an answer for that, and the honest answer usually involves a human.
 *
 * <p>The second difference is subtler and worth saying plainly: compensation is not
 * rollback. A rollback leaves no trace. A refund is a new fact — the charge stays on the
 * customer's statement with the refund beside it, and the bank may keep its fee.
 */
public interface SagaStep {

    /** What this step is called, for the log and for the humans reading it. */
    String name();

    /**
     * Does the step. Commits on its own, immediately, with nothing holding it open.
     *
     * @throws ServiceUnavailableException if the service could not be reached
     */
    void execute(SagaContext context);

    /**
     * Cancels out {@link #execute}, as far as anything can be cancelled out.
     *
     * Only called for steps that actually succeeded, and only in reverse order. May throw,
     * and the orchestrator has to cope when it does.
     */
    void compensate(SagaContext context);

    /**
     * Whether this step can be cancelled out at all.
     *
     * Most can. Sending an email cannot: once it is in somebody's inbox there is no
     * calling it back, and a saga that pretends otherwise is lying to itself. Steps like
     * that belong at the very end of a saga, after everything that might fail.
     */
    default boolean canBeCompensated() {
        return true;
    }
}
