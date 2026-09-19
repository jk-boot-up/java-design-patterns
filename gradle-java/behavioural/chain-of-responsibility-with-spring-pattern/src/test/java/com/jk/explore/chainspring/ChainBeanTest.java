package com.jk.explore.chainspring;

import org.junit.jupiter.api.Test;
import org.springframework.context.ConfigurableApplicationContext;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class ChainBeanTest {

    @Test
    void springOrdersTheChainByOrderAnnotation() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().run()) {
            assertEquals(List.of("address", "stock", "fraud", "payment-limit"), ctx.getBean(ScreeningChain.class).order());
        }
    }

    @Test
    void firstLinkThatAnswersStopsTheChainAndTheRestNeverRun() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().run()) {
            Decision d = ctx.getBean(ScreeningChain.class).screen(ScreeningApplication.NO_STOCK);
            assertEquals(Outcome.REJECTED, d.outcome());
            assertEquals("stock", d.by());
            assertEquals(List.of("fraud", "payment-limit"), d.notRun());
        }
    }

    @Test
    void referralAndApprovalPaths() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().run()) {
            ScreeningChain chain = ctx.getBean(ScreeningChain.class);
            assertEquals(Outcome.REJECTED, chain.screen(ScreeningApplication.RISKY).outcome());
            assertEquals(Outcome.REFERRED, chain.screen(ScreeningApplication.BIG).outcome());
            Decision ok = chain.screen(ScreeningApplication.GOOD);
            assertEquals(Outcome.APPROVED, ok.outcome());
            assertEquals("fallback", ok.by());
        }
    }

    @Test
    void reverseOrderCostsMoreFraudCalls() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().run()) {
            ScreeningChain chain = ctx.getBean(ScreeningChain.class);
            FraudScoreCheck.CALLS.set(0);
            ScreeningApplication.ALL.forEach(chain::screen);
            int inOrder = FraudScoreCheck.CALLS.get();
            List<ScreeningCheck> reversed = new ArrayList<>(ctx.getBeansOfType(ScreeningCheck.class).values());
            reversed.sort((a, b) -> b.name().compareTo(a.name()));
            List<ScreeningCheck> fraudFirst = new ArrayList<>(reversed);
            fraudFirst.sort((a, b) -> Boolean.compare(!a.name().equals("fraud"), !b.name().equals("fraud")));
            FraudScoreCheck.CALLS.set(0);
            ScreeningChain backwards = new ScreeningChain(fraudFirst, Outcome.APPROVED);
            ScreeningApplication.ALL.forEach(backwards::screen);
            assertTrue(FraudScoreCheck.CALLS.get() > inOrder);
        }
    }

    @Test
    void aThrowingLinkBecomesAReferral() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().run()) {
            ctx.getBean(FraudScoreCheck.class).serviceDown(true);
            Decision d = ctx.getBean(ScreeningChain.class).screen(ScreeningApplication.GOOD);
            assertEquals(Outcome.REFERRED, d.outcome());
            assertEquals("fraud", d.by());
        }
    }

    @Test
    void propertyRemovesALinkWithoutACodeChange() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().properties("screening.fraud.enabled=false").run()) {
            ScreeningChain chain = ctx.getBean(ScreeningChain.class);
            assertEquals(List.of("address", "stock", "payment-limit"), chain.order());
            assertEquals(Outcome.APPROVED, chain.screen(ScreeningApplication.RISKY).outcome());
        }
    }

    @Test
    void fallbackIsConfigurable() {
        try (ConfigurableApplicationContext ctx = ScreeningApplication.builder().properties("screening.fallback=REFERRED").run()) {
            assertEquals(Outcome.REFERRED, ctx.getBean(ScreeningChain.class).screen(ScreeningApplication.GOOD).outcome());
        }
    }
}
