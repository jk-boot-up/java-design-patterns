package com.jk.explore.externalisedconfig;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

import java.time.Duration;
import java.time.LocalDateTime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

/**
 * The cost of the naive version, in hours.
 *
 * <p>These are the numbers the video says out loud, so they are pinned here. If
 * the pipeline's shape ever changes, this test is what stops the narration from
 * quoting a figure the program no longer produces.
 */
class ReleasePipelineTest {

    private static final LocalDateTime FRIDAY_1630 = LocalDateTime.of(2025, 3, 7, 16, 30);
    private static final LocalDateTime SATURDAY_0900 = LocalDateTime.of(2025, 3, 8, 9, 0);

    private final ReleasePipeline pipeline = ReleasePipeline.typical();

    @Test
    @DisplayName("the five steps add up to two hours and fifteen minutes of work")
    void theStepsAddUp() {
        assertEquals(5, pipeline.steps().size());
        assertEquals(Duration.ofMinutes(135), pipeline.totalWork());
        assertEquals("2 hours 15 minutes", ReleasePipeline.inWords(pipeline.totalWork()));
    }

    @Test
    @DisplayName("a Friday afternoon request goes live on Monday morning")
    void aFridayRequestLandsOnMonday() {
        LocalDateTime live = pipeline.liveAt(FRIDAY_1630);

        assertEquals(LocalDateTime.of(2025, 3, 10, 10, 45), live);
        assertEquals("Mon 10 Mar 10:45", ReleasePipeline.inWords(live));
    }

    @Test
    @DisplayName("the weekend promotion is late by two days and nearly two hours")
    void theWeekendPromotionIsLate() {
        Duration late = pipeline.lateBy(SATURDAY_0900, FRIDAY_1630);

        assertEquals(Duration.ofMinutes(2 * 24 * 60 + 105), late);
        assertEquals("2 days 1 hour 45 minutes", ReleasePipeline.inWords(late));
    }

    @Test
    @DisplayName("the clock only runs inside the weekday release window")
    void workOnlyHappensInTheWindow() {
        // The code review starts on Friday and finishes on Monday, because the
        // window closes at five and does not reopen until the weekend is over.
        var schedule = pipeline.schedule(FRIDAY_1630);

        assertEquals(LocalDateTime.of(2025, 3, 7, 16, 45), schedule.get(0).finishedAt());
        assertEquals(LocalDateTime.of(2025, 3, 10, 9, 30), schedule.get(1).finishedAt());
        assertTrue(schedule.get(1).asLine().contains("code review"));
    }

    @Test
    @DisplayName("a request first thing on a weekday morning is live the same day")
    void aMondayMorningRequestIsLiveTheSameDay() {
        LocalDateTime mondayNine = LocalDateTime.of(2025, 3, 10, 9, 0);

        assertEquals(LocalDateTime.of(2025, 3, 10, 11, 15), pipeline.liveAt(mondayNine));
    }

    @Test
    @DisplayName("a change that is ready before the promised start is not late at all")
    void readyEarlyIsNotLate() {
        LocalDateTime mondayNine = LocalDateTime.of(2025, 3, 10, 9, 0);
        LocalDateTime nextFriday = LocalDateTime.of(2025, 3, 14, 9, 0);

        assertEquals(Duration.ZERO, pipeline.lateBy(nextFriday, mondayNine));
    }
}
