package com.jk.explore.repositoryspringdata;

import com.jk.explore.repositoryspringdata.repository.CustomerRepository;
import com.jk.explore.repositoryspringdata.service.LeakDemo;
import com.jk.explore.repositoryspringdata.service.MarketingService;
import com.jk.explore.repositoryspringdata.service.Seeder;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ConfigurableApplicationContext;
import org.springframework.data.repository.query.parser.PartTree;

import java.lang.reflect.Method;
import java.util.Arrays;

/**
 * Six acts. The partner project, Repository, built two implementations by
 * hand. Here there are none: the interface is enough. Every statement count
 * comes from Hibernate's statistics.
 */
@SpringBootApplication
public class CustomerApplication {

    public static void main(String[] args) {
        System.out.println("REPOSITORY WITH SPRING DATA — an interface with no implementation\n");
        try (ConfigurableApplicationContext context = SpringApplication.run(CustomerApplication.class, args)) {
            Seeder seeder = context.getBean(Seeder.class);
            actOne(context);
            actTwo(context, seeder);
            actThree(context, seeder);
            actFour(context, seeder);
            actFive(context, seeder);
            actSix();
        }
    }

    private static void actOne(ConfigurableApplicationContext context) {
        System.out.println("ONE. An interface with no implementation.");
        CustomerRepository repository = context.getBean(CustomerRepository.class);
        System.out.println("  CustomerRepository is an interface, and this project has no class that implements it.");
        System.out.println("  the object Spring injected is a " + (java.lang.reflect.Proxy.isProxyClass(repository.getClass())
                ? "generated proxy" : "class"));
        System.out.println("  save, findById, findAll, delete: all there, and none of them written.\n");
    }

    private static void actTwo(ConfigurableApplicationContext context, Seeder seeder) {
        System.out.println("TWO. A query generated from the method's own name.");
        seeder.reset();
        CustomerRepository repository = context.getBean(CustomerRepository.class);
        System.out.println("  findDistinctByCityAndOrdersDayGreaterThan(\"London\", 70): "
                + repository.findDistinctByCityAndOrdersDayGreaterThan("London", 70).stream().map(c -> c.name()).sorted().toList());
        System.out.println("  statements issued: " + seeder.statements() + ". no query was written by hand.");
        seeder.reset();
        System.out.println("  the partner's MarketingService, unchanged, gives: "
                + context.getBean(MarketingService.class).londonCustomersWhoOrderedLastMonth());
        System.out.println("  the partner had two implementation classes. this project has none, and the application runs.\n");
    }

    private static void actThree(ConfigurableApplicationContext context, Seeder seeder) {
        System.out.println("THREE. The bill — a method per question, and a name that can be wrong.");
        Arrays.stream(CustomerRepository.class.getDeclaredMethods()).map(Method::getName).filter(n -> n.startsWith("find"))
                .sorted().forEach(n -> System.out.println("    " + n));
        try {
            new PartTree("findByCiity", com.jk.explore.repositoryspringdata.domain.Customer.class);
        } catch (RuntimeException e) {
            System.out.println("  a typo in a method name, findByCiity, is caught only when Spring reads it:");
            System.out.println("  " + e.getClass().getSimpleName() + ": " + e.getMessage().substring(0, 62) + "...");
        }
        System.out.println("  the compiler cannot check a name.\n");
    }

    private static void actFour(ConfigurableApplicationContext context, Seeder seeder) {
        System.out.println("FOUR. The abstraction leaks when performance matters.");
        seeder.reset();
        LeakDemo leak = context.getBean(LeakDemo.class);
        int lazy = leak.countOrdersLazily();
        System.out.println("  counting every customer's orders, lazily: " + lazy + " orders, " + seeder.statements() + " statements.");
        seeder.clearCount();
        int graph = leak.countOrdersWithAGraph();
        System.out.println("  with @EntityGraph on the repository method: " + graph + " orders, " + seeder.statements() + " statement.");
        System.out.println("  the interface can say 'join', but only by carrying a persistence hint.\n");
    }

    private static void actFive(ConfigurableApplicationContext context, Seeder seeder) {
        System.out.println("FIVE. The managed entity that leaks.");
        seeder.reset();
        LeakDemo leak = context.getBean(LeakDemo.class);
        leak.moveFirstCustomerInsideATransaction();
        System.out.println("  a caller inside a transaction changed a customer from findAll(), and never called save.");
        System.out.println("  Ada's city in the database now: " + seeder.cityOf(1));
        seeder.reset();
        leak.moveFirstCustomerOutsideATransaction();
        System.out.println("  the same change with no transaction around it. Ada's city in the database: " + seeder.cityOf(1));
        System.out.println("  written with no save in one case, lost with no error in the other.\n");
    }

    private static void actSix() {
        System.out.println("SIX. Where you have already met this.");
        System.out.println("  this is Repository, with the framework supplying the implementation.");
        System.out.println("  and 'you can swap the database' is still claimed far more often than it is used.");
    }
}
