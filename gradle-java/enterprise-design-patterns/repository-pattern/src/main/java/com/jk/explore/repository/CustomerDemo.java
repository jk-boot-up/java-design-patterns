package com.jk.explore.repository;

import com.jk.explore.repository.domain.Customer;
import com.jk.explore.repository.domain.Shop;
import com.jk.explore.repository.naive.SqlInTheService;
import com.jk.explore.repository.pattern.CustomerRepository;
import com.jk.explore.repository.pattern.InMemoryCustomerRepository;
import com.jk.explore.repository.pattern.MarketingService;
import com.jk.explore.repository.pattern.QueryMethodGrowth;
import com.jk.explore.repository.pattern.Specification;
import com.jk.explore.repository.pattern.ToyDatabaseCustomerRepository;
import com.jk.explore.repository.toydb.Database;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

/** Six acts. Every count comes from the toy database's own operation counter. */
public final class CustomerDemo {

    public static void main(String[] args) {
        System.out.println("REPOSITORY — query the collection, not the table\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. SQL in the service — the same question, asked three ways.");
        SqlInTheService services = new SqlInTheService(Shop.seeded());
        System.out.println("  marketing: " + services.marketingList());
        System.out.println("  support:   " + services.supportList());
        System.out.println("  reports:   " + services.reportList());
        System.out.println("  three answers to one question. support is off by one day.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. A schema change — every string that names a column.");
        Database db = Shop.seeded();
        for (var row : db.table("customers").selectAll()) {
            db.table("customers").update(row.number("id"),
                    com.jk.explore.repository.toydb.Row.of("id", row.number("id"), "name", row.text("name"), "town", row.text("city")));
        }
        SqlInTheService services = new SqlInTheService(db);
        System.out.println("  the column city is renamed to town.");
        System.out.println("  marketing: " + services.marketingList());
        System.out.println("  support:   " + services.supportList());
        System.out.println("  reports:   " + services.reportList());
        System.out.println("  nothing threw. every list is empty. each string had to be found by hand.\n");
    }

    private static void actThree() {
        System.out.println("THREE. The pattern — the service asks for customers.");
        CustomerRepository repository = new InMemoryCustomerRepository();
        Shop.customers().forEach(repository::add);
        MarketingService service = new MarketingService(repository);
        System.out.println("  " + service.londonCustomersWhoOrderedLastMonth());
        System.out.println("  MarketingService's constructor takes: "
                + MarketingService.class.getConstructors()[0].getParameterTypes()[0].getSimpleName());
        System.out.println("  it knows no database, no table, no column.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. Swap the store — the calling code does not change.");
        CustomerRepository memory = new InMemoryCustomerRepository();
        Shop.customers().forEach(memory::add);
        Database db = Shop.seeded();
        CustomerRepository database = new ToyDatabaseCustomerRepository(db);
        System.out.println("  in memory: " + new MarketingService(memory).londonCustomersWhoOrderedLastMonth());
        System.out.println("  database:  " + new MarketingService(database).londonCustomersWhoOrderedLastMonth());
        System.out.println("  the whole change is one line where the service is built:");
        System.out.println("    - new MarketingService(new InMemoryCustomerRepository())");
        System.out.println("    + new MarketingService(new ToyDatabaseCustomerRepository(db))");
        System.out.println("  MarketingService itself is untouched.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill — a method per question.");
        List<String> names = Arrays.stream(QueryMethodGrowth.class.getDeclaredMethods()).map(Method::getName).sorted().toList();
        names.forEach(n -> System.out.println("    " + n));
        System.out.println("  every new question adds a method. a specification fixes it and costs a concept:");
        CustomerRepository repository = new InMemoryCustomerRepository();
        Shop.customers().forEach(repository::add);
        List<Customer> found = repository.matching(Specification.inCity("London")
                .and(Specification.orderedAfter(Shop.LAST_MONTH_STARTS)).and(Specification.hasOrderWithStatus("PENDING")));
        System.out.println("  London, ordered last month, and has a pending order: "
                + found.stream().map(Customer::name).toList());
        System.out.println("  no new repository method was written.\n");
    }

    private static void actSix() {
        System.out.println("SIX. The abstraction leaks when performance matters.");
        Database db = Shop.seeded();
        CustomerRepository database = new ToyDatabaseCustomerRepository(db);
        new MarketingService(database).londonCustomersWhoOrderedLastMonth();
        System.out.println("  one question, against 6 customers: " + db.operationCount()
                + " database operations: one for the customers, then one per customer for their orders.");
        System.out.println("  the caller cannot say 'join' or 'fetch the orders together'.");
        System.out.println("  and 'you can swap the database' is claimed far more often than it is used.");
        System.out.println("  where you have met this: a Spring Data repository interface.");
    }
}
