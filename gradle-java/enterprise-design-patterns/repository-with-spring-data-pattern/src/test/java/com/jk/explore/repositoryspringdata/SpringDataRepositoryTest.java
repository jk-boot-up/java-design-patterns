package com.jk.explore.repositoryspringdata;

import com.jk.explore.repositoryspringdata.domain.Customer;
import com.jk.explore.repositoryspringdata.repository.CustomerRepository;
import com.jk.explore.repositoryspringdata.service.LeakDemo;
import com.jk.explore.repositoryspringdata.service.MarketingService;
import com.jk.explore.repositoryspringdata.service.Seeder;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.data.repository.query.parser.PartTree;

import java.lang.reflect.Proxy;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

@SpringBootTest(classes = CustomerApplication.class, properties = "spring.datasource.url=jdbc:h2:mem:sd-test;DB_CLOSE_DELAY=-1")
class SpringDataRepositoryTest {

    @Autowired CustomerRepository repository;
    @Autowired MarketingService marketing;
    @Autowired LeakDemo leak;
    @Autowired Seeder seeder;

    @BeforeEach
    void reset() {
        seeder.reset();
    }

    @Test
    void theRepositoryIsAnInterfaceWithNoImplementationAndSpringInjectsAProxy() {
        assertTrue(CustomerRepository.class.isInterface());
        assertTrue(Proxy.isProxyClass(repository.getClass()));
        assertEquals(6, repository.count());
    }

    @Test
    void aQueryIsGeneratedFromTheMethodNameInOneStatement() {
        List<String> names = repository.findDistinctByCityAndOrdersDayGreaterThan("London", 70).stream()
                .map(Customer::name).sorted().toList();
        assertEquals(List.of("Ada", "Grace"), names);
        assertEquals(1, seeder.statements());
    }

    @Test
    void thePartnersServiceGivesThePartnersAnswerWithNoImplementationClass() {
        assertEquals(List.of("Ada", "Grace"), marketing.londonCustomersWhoOrderedLastMonth());
    }

    @Test
    void aTypoInAMethodNameIsOnlyCaughtWhenSpringReadsIt() {
        assertThrows(RuntimeException.class, () -> new PartTree("findByCiity", Customer.class));
        new PartTree("findByCity", Customer.class);
    }

    @Test
    void touchingEachCustomersLazyOrdersCostsSevenStatementsAndAGraphCostsOne() {
        seeder.clearCount();
        assertEquals(7, leak.countOrdersLazily());
        assertEquals(7, seeder.statements());
        seeder.clearCount();
        assertEquals(7, leak.countOrdersWithAGraph());
        assertEquals(1, seeder.statements());
    }

    @Test
    void aChangeToAnEntityInsideATransactionIsWrittenWithNoSaveCall() {
        leak.moveFirstCustomerInsideATransaction();
        assertEquals("Manchester", seeder.cityOf(1));
    }

    @Test
    void theSameChangeOutsideATransactionIsSilentlyLost() {
        leak.moveFirstCustomerOutsideATransaction();
        assertEquals("London", seeder.cityOf(1));
    }
}
