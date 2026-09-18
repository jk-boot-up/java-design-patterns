package com.jk.explore.externalisedconfig;

import java.time.DayOfWeek;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.LocalTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

/**
 * What it costs to change a number that lives in the source code.
 *
 * <p>This class is the honest half of the naive version. It is easy to argue that
 * a hard-coded constant is fine because changing it is only one line — and it is
 * only one line. What it is not is only one line's worth of <em>time</em>. The
 * line has to be written, reviewed by a second person, built and tested, approved
 * for release, and deployed, and none of those steps is unreasonable. Added up
 * they come to {@link #totalWork()}.
 *
 * <p>The part that really bites is not the total, though. It is the working
 * window. Deployments happen on weekdays between {@link #WINDOW_OPENS} and
 * {@link #WINDOW_CLOSES}, because that is when the people who review, approve and
 * watch a release are at their desks, and because a change freeze over the weekend
 * is the sane policy and not a failure of nerve. So a request that arrives late on
 * a Friday afternoon does not take two hours; it takes until Monday morning. A
 * promotion that was supposed to start on Saturday goes live after the weekend it
 * was for.
 *
 * <p>Nothing in this class is a criticism of the pipeline. The pipeline is the
 * right shape for changes to how the shop <em>works</em>. It is the wrong shape
 * for changes to what the shop <em>charges</em>, and telling those two kinds of
 * change apart is the judgement this pattern asks of you.
 */
public final class ReleasePipeline {

    /** The earliest a release step can be worked on. */
    public static final LocalTime WINDOW_OPENS = LocalTime.of(9, 0);

    /** The latest a release step can be worked on. */
    public static final LocalTime WINDOW_CLOSES = LocalTime.of(17, 0);

    private static final DateTimeFormatter STAMP =
            DateTimeFormatter.ofPattern("EEE dd MMM HH:mm");

    /**
     * One stage of getting a change into production.
     *
     * @param name what happens
     * @param takes how long it takes, working hours only
     */
    public record Step(String name, Duration takes) {
    }

    /**
     * A step with the moment it finishes, once the working window is taken into
     * account.
     *
     * @param step the stage
     * @param finishedAt when it is done
     */
    public record ScheduledStep(Step step, LocalDateTime finishedAt) {

        /** One line for the demo's table. */
        public String asLine() {
            return String.format("  %-24s %3d min   done %s",
                    step.name(), step.takes().toMinutes(), STAMP.format(finishedAt));
        }
    }

    private final List<Step> steps;

    /** The pipeline this shop actually runs. */
    public static ReleasePipeline typical() {
        return new ReleasePipeline(List.of(
                new Step("edit the constant", Duration.ofMinutes(15)),
                new Step("code review", Duration.ofMinutes(45)),
                new Step("build and test", Duration.ofMinutes(25)),
                new Step("release approval", Duration.ofMinutes(30)),
                new Step("deploy and watch", Duration.ofMinutes(20))));
    }

    public ReleasePipeline(List<Step> steps) {
        this.steps = List.copyOf(steps);
    }

    /** The stages, in order. */
    public List<Step> steps() {
        return steps;
    }

    /** The stages added up, ignoring weekends and nights. */
    public Duration totalWork() {
        return steps.stream().map(Step::takes).reduce(Duration.ZERO, Duration::plus);
    }

    /**
     * Every stage with the moment it finishes, starting from a request.
     *
     * <p>This is what the demo prints, because the interesting number is not the
     * total at the bottom but the place in the middle where the clock jumps from
     * Friday evening to Monday morning.
     */
    public List<ScheduledStep> schedule(LocalDateTime requestedAt) {
        List<ScheduledStep> scheduled = new ArrayList<>();
        LocalDateTime at = requestedAt;
        for (Step step : steps) {
            at = advance(at, step.takes());
            scheduled.add(new ScheduledStep(step, at));
        }
        return scheduled;
    }

    /** When the change is finally live, starting from a request. */
    public LocalDateTime liveAt(LocalDateTime requestedAt) {
        List<ScheduledStep> scheduled = schedule(requestedAt);
        return scheduled.get(scheduled.size() - 1).finishedAt();
    }

    /**
     * How late the change is against a promised start, or zero if it made it.
     *
     * <p>Zero rather than a negative duration, because a change that is ready
     * early is not early in any way the shop can spend.
     */
    public Duration lateBy(LocalDateTime promisedStart, LocalDateTime requestedAt) {
        Duration late = Duration.between(promisedStart, liveAt(requestedAt));
        return late.isNegative() ? Duration.ZERO : late;
    }

    /** Moves a number of working minutes forward from a moment. */
    private LocalDateTime advance(LocalDateTime from, Duration work) {
        LocalDateTime at = nextWorkingMoment(from);
        long remaining = work.toMinutes();
        while (true) {
            LocalDateTime closing = at.toLocalDate().atTime(WINDOW_CLOSES);
            long availableToday = Duration.between(at, closing).toMinutes();
            if (availableToday >= remaining) {
                return at.plusMinutes(remaining);
            }
            remaining -= availableToday;
            at = nextWorkingMoment(closing);
        }
    }

    /** The first moment at or after this one that release work can happen. */
    private LocalDateTime nextWorkingMoment(LocalDateTime from) {
        LocalDateTime at = from;
        while (true) {
            DayOfWeek day = at.getDayOfWeek();
            if (day == DayOfWeek.SATURDAY || day == DayOfWeek.SUNDAY) {
                at = at.toLocalDate().plusDays(1).atTime(WINDOW_OPENS);
            } else if (at.toLocalTime().isBefore(WINDOW_OPENS)) {
                at = at.toLocalDate().atTime(WINDOW_OPENS);
            } else if (!at.toLocalTime().isBefore(WINDOW_CLOSES)) {
                at = at.toLocalDate().plusDays(1).atTime(WINDOW_OPENS);
            } else {
                return at;
            }
        }
    }

    /** A duration written the way a person would say it. */
    public static String inWords(Duration duration) {
        long days = duration.toDays();
        long hours = duration.toHours() % 24;
        long minutes = duration.toMinutes() % 60;
        StringBuilder words = new StringBuilder();
        if (days > 0) {
            words.append(days).append(days == 1 ? " day " : " days ");
        }
        if (hours > 0 || days > 0) {
            words.append(hours).append(hours == 1 ? " hour " : " hours ");
        }
        words.append(minutes).append(minutes == 1 ? " minute" : " minutes");
        return words.toString();
    }

    /** A moment written the way a person would say it. */
    public static String inWords(LocalDateTime moment) {
        return STAMP.format(moment);
    }
}
