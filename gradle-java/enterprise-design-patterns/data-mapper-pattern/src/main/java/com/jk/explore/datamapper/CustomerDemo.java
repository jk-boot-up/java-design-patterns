package com.jk.explore.datamapper;

import com.jk.explore.datamapper.domain.Address;
import com.jk.explore.datamapper.domain.Customer;
import com.jk.explore.datamapper.naive.ActiveRecordCustomer;
import com.jk.explore.datamapper.pattern.CarelessCustomerMapper;
import com.jk.explore.datamapper.pattern.CustomerMapper;
import com.jk.explore.datamapper.toydb.Database;

import java.lang.reflect.Field;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;
import java.util.List;

/**
 * Six acts. Every operation against the toy database is counted, and every
 * count quoted below comes from that counter.
 */
public final class CustomerDemo {

    private static final Address ADDRESS = new Address("12 Mill Lane", "Leeds", "LS1 4AB");

    public static void main(String[] args) {
        System.out.println("DATA MAPPER — the object that does not know it is a row\n");

        actOne();
        actTwo();
        actThree();
        actFour();
        actFive();
        actSix();
    }

    private static void actOne() {
        System.out.println("ONE. Active Record — the object saves itself, and it works well.");
        Database db = new Database();
        ActiveRecordCustomer ada = new ActiveRecordCustomer(db, 1, "Ada Lovelace", "ada@example.com",
                "12 Mill Lane", "Leeds", "LS1 4AB");
        ada.save();
        ActiveRecordCustomer loaded = ActiveRecordCustomer.find(db, 1);
        loaded.changeEmail("ada@newmail.example");
        loaded.save();
        System.out.println("  customer.save(), find(), change, save():");
        db.operations().forEach(op -> System.out.println("    " + op));
        System.out.println("  " + db.operationCount() + " operations, one class, one table. For a simple");
        System.out.println("  application this is the right answer.\n");
    }

    private static void actTwo() {
        System.out.println("TWO. The cost — the domain object cannot exist without the database.");
        System.out.println("  ActiveRecordCustomer constructor takes a Database, and names its own table:");
        System.out.println("    table \"" + ActiveRecordCustomer.TABLE + "\", columns name, email, street, city, postcode");
        Customer plain = new Customer(1, "Ada Lovelace", "ada@example.com", ADDRESS, 0);
        plain.changeEmail("ada@newmail.example");
        System.out.println("  a plain Customer changed its email with no database anywhere: "
                + plain.email() + "\n");
    }

    private static void actThree() {
        System.out.println("THREE. The shape Active Record has no answer for.");
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(new Customer(1, "Ada Lovelace", "ada@example.com", ADDRESS, 10));
        mapper.insert(new Customer(2, "Grace Hopper", "grace@example.com",
                new Address("4 Navy Yard", "Arlington", "VA 22202"), 20));
        db.clearLog();
        mapper.find(1);
        System.out.println("  one customer, stored across two tables:");
        db.operations().forEach(op -> System.out.println("    " + op));
        db.clearLog();
        int count = mapper.summaries().size();
        System.out.println("  one table, feeding a second, smaller object: " + count + " summaries, from");
        db.operations().forEach(op -> System.out.println("    " + op));
        System.out.println("  one class per table cannot say either of these.\n");
    }

    private static void actFour() {
        System.out.println("FOUR. The pattern — the mapper knows the rows; the customer does not.");
        Database db = new Database();
        CustomerMapper mapper = new CustomerMapper(db);
        mapper.insert(new Customer(1, "Ada Lovelace", "ada@example.com", ADDRESS, 10));
        Customer loaded = mapper.find(1);
        System.out.println("  loaded back: " + loaded.name() + ", " + loaded.address().city() + ", "
                + loaded.loyaltyPoints() + " points");
        System.out.println("  Customer's fields:");
        Arrays.stream(Customer.class.getDeclaredFields()).map(Field::getName).sorted()
                .forEach(f -> System.out.println("    " + f));
        List<String> methods = new ArrayList<>();
        Arrays.stream(Customer.class.getDeclaredMethods()).map(Method::getName)
                .sorted(Comparator.naturalOrder()).forEach(methods::add);
        System.out.println("  Customer's methods: " + methods);
        System.out.println("  no table, no column, no SQL, no database.\n");
    }

    private static void actFive() {
        System.out.println("FIVE. The bill — a hand-written mapping can lose a field silently.");
        Database db = new Database();
        CustomerMapper careless = new CarelessCustomerMapper(db);
        careless.insert(new Customer(1, "Ada Lovelace", "ada@example.com", ADDRESS, 10));
        Customer back = careless.find(1);
        System.out.println("  saved postcode:  " + ADDRESS.postcode());
        System.out.println("  loaded postcode: " + back.address().postcode());
        System.out.println("  every call succeeded. nothing threw. the field is simply gone.\n");
    }

    private static void actSix() {
        System.out.println("SIX. Where you have already met this.");
        System.out.println("  a JPA entity is the domain object; the EntityManager is the mapper.");
        System.out.println("  Hibernate writes the mapping code that act five shows can go wrong.");
        System.out.println("  the cost is the same: a layer to understand before you can debug.");
        System.out.println("  and Data Mapper writes a second class for every entity: here that is");
        System.out.println("  CustomerMapper next to Customer, and it is where the mapping bugs live.");
    }
}
