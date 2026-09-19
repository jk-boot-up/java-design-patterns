package com.jk.explore.pipesfilters;

import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/** Filters joined end to end. Items flow through one at a time, so a stage never holds the whole batch. */
public class Pipeline<I, O> {

    public record Result<O>(List<O> out, List<String> rejects, int peakItemsHeld) {
    }

    private final List<Filter<Object, Object>> stages;

    private Pipeline(List<Filter<Object, Object>> stages) {
        this.stages = stages;
    }

    public static <A, B> Pipeline<A, B> start(Filter<A, B> first) {
        List<Filter<Object, Object>> l = new ArrayList<>();
        l.add(cast(first));
        return new Pipeline<>(l);
    }

    @SuppressWarnings("unchecked")
    private static Filter<Object, Object> cast(Filter<?, ?> f) {
        return (Filter<Object, Object>) f;
    }

    public <P> Pipeline<I, P> then(Filter<O, P> next) {
        List<Filter<Object, Object>> l = new ArrayList<>(stages);
        l.add(cast(next));
        return new Pipeline<>(l);
    }

    public List<String> stageNames() {
        return stages.stream().map(Filter::name).toList();
    }

    /** Streaming: each item goes all the way through before the next is taken. */
    @SuppressWarnings("unchecked")
    public Result<O> run(List<I> input) {
        List<String> rejects = new ArrayList<>();
        List<O> out = new ArrayList<>();
        input.forEach(item -> {
            Object current = item;
            for (Filter<Object, Object> stage : stages) {
                var next = stage.apply(current, rejects);
                if (next.isEmpty()) {
                    return;
                }
                current = next.get();
            }
            out.add((O) current);
        });
        return new Result<>(out, rejects, 1);
    }

    /** Eager: every stage finishes the whole batch before the next stage starts, so a whole batch is held at each step. */
    @SuppressWarnings("unchecked")
    public Result<O> runStageByStage(List<I> input) {
        List<String> rejects = new ArrayList<>();
        List<Object> batch = new ArrayList<>(input);
        int peak = batch.size();
        for (Filter<Object, Object> stage : stages) {
            List<Object> next = new ArrayList<>();
            for (Object item : batch) {
                stage.apply(item, rejects).ifPresent(next::add);
            }
            peak = Math.max(peak, batch.size() + next.size());
            batch = next;
        }
        return new Result<>((List<O>) (List<?>) batch, rejects, peak);
    }
}
