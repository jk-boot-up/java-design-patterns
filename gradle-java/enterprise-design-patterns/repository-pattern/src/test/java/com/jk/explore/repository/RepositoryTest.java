package com.jk.explore.repository;

import com.jk.explore.repository.domain.Customer;
import com.jk.explore.repository.domain.Shop;
import com.jk.explore.repository.pattern.CustomerRepository;
import com.jk.explore.repository.pattern.InMemoryCustomerRepository;
import com.jk.explore.repository.pattern.MarketingService;
import com.jk.explore.repository.pattern.QueryMethodGrowth;
import com.jk.explore.repository.pattern.Specification;
import com.jk.explore.repository.pattern.ToyDatabaseCustomerRepository;
import com.jk.explore.repository.toydb.Database;
import org.junit.jupiter.api.Test;

import java.lang.reflect.Field;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertNull;

class RepositoryTest {

    private CustomerRepository memory() {
        CustomerRepository repository = new InMemoryCustomerRepository();
        Shop.customers().forEach(repository::add);
        return repository;
    }

    @Test
    void theSameServiceGivesTheSameAnswerOnEitherStore() {
        List<String> inMemory = new MarketingService(memory()).londonCustomersWhoOrderedLastMonth();
        List<String> inDatabase = new MarketingService(new ToyDatabaseCustomerRepository(Shop.seeded()))
                .londonCustomersWhoOrderedLastMonth();
        assertEquals(List.of("Ada", "Grace"), inMemory);
        assertEquals(inMemory, inDatabase);
    }

    @Test
    void theServiceKnowsOnlyTheInterface() {
        assertEquals(1, MarketingService.class.getConstructors()[0].getParameterCount());
        assertEquals(CustomerRepository.class, MarketingService.class.getConstructors()[0].getParameterTypes()[0]);
        for (Field f : MarketingService.class.getDeclaredFields()) {
            assertFalse(f.getType().getName().contains("toydb"), f.getName());
        }
    }

    @Test
    void findByIdReturnsNullWhenThereIsNoSuchCustomer() {
        assertNull(memory().findById(99));
        assertNull(new ToyDatabaseCustomerRepository(Shop.seeded()).findById(99));
        assertEquals("Ada", new ToyDatabaseCustomerRepository(Shop.seeded()).findById(1).name());
    }

    @Test
    void specificationsCombineWithoutANewRepositoryMethod() {
        List<Customer> found = memory().matching(Specification.inCity("London")
                .and(Specification.orderedAfter(Shop.LAST_MONTH_STARTS))
                .and(Specification.hasOrderWithStatus("PENDING")));
        assertEquals(List.of("Grace"), found.stream().map(Customer::name).toList());
    }

    @Test
    void theInterfaceGrowsAMethodPerQuestion() {
        assertEquals(4, QueryMethodGrowth.class.getDeclaredMethods().length);
    }

    @Test
    void theDatabaseRepositoryCannotJoinSoItCostsOneQueryPerCustomer() {
        Database db = Shop.seeded();
        new MarketingService(new ToyDatabaseCustomerRepository(db)).londonCustomersWhoOrderedLastMonth();
        assertEquals(7, db.operationCount());
    }
}
