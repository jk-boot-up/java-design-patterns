package com.jk.explore.stijpa;

import com.jk.explore.stijpa.perclass.BookItem;
import com.jk.explore.stijpa.perclass.CatalogItem;
import com.jk.explore.stijpa.perclass.ElectronicsItem;
import com.jk.explore.stijpa.perclass.FoodItem;
import com.jk.explore.stijpa.single.Book;
import com.jk.explore.stijpa.single.Electronics;
import com.jk.explore.stijpa.single.Food;
import com.jk.explore.stijpa.single.GiftCard;
import com.jk.explore.stijpa.single.Product;
import jakarta.persistence.EntityManager;
import jakarta.persistence.EntityManagerFactory;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;
import org.springframework.boot.builder.SpringApplicationBuilder;
import org.springframework.context.ConfigurableApplicationContext;

/**
 * The five acts, with JPA annotations and the SQL Hibernate writes for them.
 */
public final class JpaSingleTableDemo {

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();
        try (ConfigurableApplicationContext ctx = new SpringApplicationBuilder(ShopApp.class)
                .properties("spring.main.banner-mode=off", "logging.level.root=OFF",
                        "spring.datasource.url=jdbc:h2:mem:shop", "spring.jpa.hibernate.ddl-auto=create",
                        "spring.jpa.open-in-view=false",
                        "spring.jpa.properties.hibernate.session_factory.statement_inspector=" + SqlLog.class.getName())
                .run()) {
            EntityManagerFactory emf = ctx.getBean(EntityManagerFactory.class);
            inTransaction(emf, em -> {
                em.persist(new BookItem("BOOK-1", "cook book", 1500, "978-1-00"));
                em.persist(new ElectronicsItem("LAMP-1", "desk lamp", 900, 1));
                em.persist(new FoodItem("TEA-1", "breakfast tea", 450, "2027-03-01"));
                em.persist(new Book("BOOK-1", "cook book", 1500, "978-1-00"));
                em.persist(new Electronics("KETTLE-1", "kettle", 3000, 2));
                em.persist(new Electronics("LAMP-1", "desk lamp", 900, 1));
                em.persist(new Food("TEA-1", "breakfast tea", 450, "2027-03-01"));
            });

            out.add("ONE. A table for every class: @Inheritance(TABLE_PER_CLASS).");
            SqlLog.STATEMENTS.clear();
            List<String> cheap = names(emf, "select i from CatalogItem i where i.pence < 1000 order by i.name");
            String sql = SqlLog.STATEMENTS.get(0);
            out.add("  everything under £10: " + cheap);
            out.add("  Hibernate's SQL: one query that " + (sql.contains("union") ? "UNIONs " + (count(sql, " from ") - 1)
                    + " tables together" : "reads one table"));
            out.add("  a fourth product class means a fourth table, and the union grows");

            out.add("");
            out.add("TWO. One table: @Inheritance(SINGLE_TABLE) with a type column.");
            SqlLog.STATEMENTS.clear();
            cheap = names(emf, "select p from Product p where p.pence < 1000 order by p.name");
            sql = SqlLog.STATEMENTS.get(0);
            out.add("  everything under £10: " + cheap);
            out.add("  Hibernate's SQL: " + (sql.contains("union") || sql.contains("join") ? "a union or join"
                    : "one plain select from the product table"));

            out.add("");
            out.add("THREE. Each row comes back as its own class.");
            inTransaction(emf, em -> em.createQuery("select p from Product p order by p.sku", Product.class).getResultList()
                    .forEach(p -> out.add("  " + p.getSku() + " -> " + p.getClass().getSimpleName() + ": " + p.detail())));
            out.add("  the type column holds: " + column(emf, "select distinct type from product order by type"));

            out.add("");
            out.add("FOUR. A new type: one class and one new column.");
            inTransaction(emf, em -> em.persist(new GiftCard("GIFT-1", "gift card", 5000, 5000)));
            inTransaction(emf, em -> {
                Product gift = em.find(Product.class, "GIFT-1");
                out.add("  GIFT-1 -> " + gift.getClass().getSimpleName() + ": " + gift.detail());
            });
            out.add("  the product table's columns: " + column(emf,
                    "select lower(column_name) from information_schema.columns where table_name = 'PRODUCT' order by ordinal_position"));

            out.add("");
            out.add("FIVE. The bill: empty cells, and rules the database cannot keep.");
            List<String> nulls = column(emf, "select (case when isbn is null then 1 else 0 end) + (case when warranty_years is null then 1 else 0 end)"
                    + " + (case when best_before is null then 1 else 0 end) + (case when value_pence is null then 1 else 0 end) from product");
            int empty = nulls.stream().mapToInt(Integer::parseInt).sum();
            out.add("  " + empty + " of " + nulls.size() * 4 + " type-specific cells are empty (NULL)");
            String notNull;
            try {
                inTransaction(emf, em -> em.createNativeQuery("alter table product alter column isbn set not null").executeUpdate());
                notNull = "accepted";
            } catch (RuntimeException e) {
                notNull = "refused: the kettle, lamp, tea and gift card rows have no ISBN";
            }
            out.add("  make isbn NOT NULL, as every book needs one: " + notNull);
            inTransaction(emf, em -> em.persist(new Book("BOOK-2", "notebook", 300, null)));
            out.add("  so a book with no ISBN is saved: " + (column(emf, "select count(*) from product where sku = 'BOOK-2'").get(0)
                    .equals("1") ? "BOOK-2 stored" : "not stored"));
            out.add("  (and @Column(nullable = false) on Book.isbn would stop every kettle and tea from being saved at all)");
            out.add("  so the rule must live in Java, for example with Bean Validation's @NotNull");
        }
        return out;
    }

    private static void inTransaction(EntityManagerFactory emf, Consumer<EntityManager> work) {
        EntityManager em = emf.createEntityManager();
        try {
            em.getTransaction().begin();
            work.accept(em);
            em.getTransaction().commit();
        } finally {
            if (em.getTransaction().isActive()) {
                em.getTransaction().rollback();
            }
            em.close();
        }
    }

    private static List<String> names(EntityManagerFactory emf, String jpql) {
        List<String> out = new ArrayList<>();
        inTransaction(emf, em -> em.createQuery(jpql, Object.class).getResultList().forEach(o ->
                out.add(o instanceof Product p ? p.getName() : ((CatalogItem) o).getName())));
        return out;
    }

    private static List<String> column(EntityManagerFactory emf, String sql) {
        List<String> out = new ArrayList<>();
        inTransaction(emf, em -> em.createNativeQuery(sql).getResultList().forEach(o -> out.add(String.valueOf(o))));
        return out;
    }

    private static int count(String text, String part) {
        return text.split(part, -1).length - 1;
    }

    private JpaSingleTableDemo() {
    }
}
