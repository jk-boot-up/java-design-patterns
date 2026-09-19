package com.jk.explore.unitofworkspring;

import com.jk.explore.unitofworkspring.domain.StockFailure;
import com.jk.explore.unitofworkspring.domain.StockFailureChecked;
import com.jk.explore.unitofworkspring.service.CheckedFailurePlacement;
import com.jk.explore.unitofworkspring.service.FlushNobodyWrote;
import com.jk.explore.unitofworkspring.service.SelfInvocation;
import com.jk.explore.unitofworkspring.service.SelfSavingPlacement;
import com.jk.explore.unitofworkspring.service.Shelf;
import com.jk.explore.unitofworkspring.service.TransactionalPlacement;
import jakarta.persistence.TransactionRequiredException;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * Six acts. The partner project, Unit of Work, built the mechanism by hand:
 * register changes, write at commit, roll back to nothing. Here the same order
 * goes through {@code @Transactional}, and the failures are Spring's own.
 */
@SpringBootApplication
public class OrderApplication {

    public static void main(String[] args) {
        System.out.println("UNIT OF WORK WITH SPRING — the flush you did not write\n");
        try (ConfigurableApplicationContext context = SpringApplication.run(OrderApplication.class, args)) {
            Shelf shelf = context.getBean(Shelf.class);
            actOne(context, shelf);
            actTwo(context, shelf);
            actThree(context, shelf);
            actFour(context, shelf);
            actFive(context, shelf);
            actSix(context, shelf);
        }
    }

    private static void actOne(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("ONE. No transaction around the order — every step commits alone.");
        shelf.reset();
        try {
            context.getBean(SelfSavingPlacement.class).place();
        } catch (StockFailure e) {
            System.out.println("  the third stock update failed: " + e.getMessage());
        }
        System.out.println("  committed: " + shelf.committed().describe());
        System.out.println("  the partner's first act, with Spring: half an order.\n");
    }

    private static void actTwo(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("TWO. @Transactional — the unit of work is one annotation.");
        shelf.reset();
        long[] beforeCommit = context.getBean(TransactionalPlacement.class).placeGoodOrderReportingWrites(shelf);
        System.out.println("  inside the method, after changing three objects: inserts written " + beforeCommit[0]
                + ", updates written " + beforeCommit[1] + ".");
        System.out.println("  after the method returned: inserts written " + shelf.insertsIssued() + ", updates written "
                + shelf.updatesIssued() + ".");
        System.out.println("  the writes appeared at commit, not where the code is.");
        shelf.reset();
        try {
            context.getBean(TransactionalPlacement.class).place();
        } catch (StockFailure e) {
            System.out.println("  the same failure as act one, now under @Transactional:");
        }
        System.out.println("  committed: " + shelf.committed().describe());
        System.out.println("  all of the order, or none of it.\n");
    }

    private static void actThree(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("THREE. The exception nobody expected to matter.");
        shelf.reset();
        try {
            context.getBean(CheckedFailurePlacement.class).place();
        } catch (StockFailureChecked e) {
            System.out.println("  the same failure, declared as a checked exception: " + e.getMessage());
        }
        System.out.println("  committed: " + shelf.committed().describe());
        System.out.println("  under @Transactional, and half an order committed anyway.");
        System.out.println("  Spring rolls back on unchecked exceptions and errors. on checked ones it commits.\n");
    }

    private static void actFour(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("FOUR. The one-line fix: rollbackFor.");
        shelf.reset();
        try {
            context.getBean(CheckedFailurePlacement.class).placeWithRollbackFor();
        } catch (StockFailureChecked e) {
            System.out.println("  @Transactional(rollbackFor = StockFailureChecked.class), same failure:");
        }
        System.out.println("  committed: " + shelf.committed().describe());
        System.out.println("  the default has to be overridden, in the annotation, by someone who knows.\n");
    }

    private static void actFive(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("FIVE. A flush nobody wrote.");
        shelf.reset();
        long[] updates = context.getBean(FlushNobodyWrote.class).changeThenQuery(shelf);
        System.out.println("  updates written before changing anything: " + updates[0]);
        System.out.println("  after changing a product's stock:         " + updates[1] + " (held back until commit)");
        System.out.println("  after running an unrelated query:         " + updates[2] + " (Hibernate wrote it first)");
        System.out.println("  the write happened at a line that says nothing about writing.\n");
    }

    private static void actSix(ConfigurableApplicationContext context, Shelf shelf) {
        System.out.println("SIX. The annotation that does nothing.");
        shelf.reset();
        try {
            context.getBean(SelfInvocation.class).placeViaThis();
        } catch (TransactionRequiredException e) {
            System.out.println("  placeViaThis() called placeLines(), which is @Transactional, through this. it threw:");
            System.out.println("  " + e.getClass().getSimpleName() + ": " + e.getMessage().substring(0, 55) + "...");
        }
        System.out.println("  committed: " + shelf.committed().describe());
        System.out.println("  the annotation was never seen. @Transactional works through a proxy, and a call on this skips it.");
        System.out.println("  where you have met this: every @Transactional method in a Spring application.");
    }
}
