package com.jk.explore.datamapper.naive;

import com.jk.explore.datamapper.toydb.Database;
import com.jk.explore.datamapper.toydb.Row;
import com.jk.explore.datamapper.toydb.Table;

/**
 * <strong>Active Record: the object saves itself.</strong> For a simple
 * application this is the right answer. One class, one table, one place to
 * look, and {@code customer.save()} reads like what it does. It is shown
 * here working well before its cost appears.
 *
 * <p>It also shows the cost: this class knows the table name, the column
 * names and the database, so the domain object cannot exist without them.
 */
public class ActiveRecordCustomer {

    public static final String TABLE = "customers";

    private final Database database;
    private final int id;
    private String name;
    private String email;
    private String street;
    private String city;
    private String postcode;

    public ActiveRecordCustomer(Database database, int id, String name, String email,
                                String street, String city, String postcode) {
        this.database = database;
        this.id = id;
        this.name = name;
        this.email = email;
        this.street = street;
        this.city = city;
        this.postcode = postcode;
    }

    public static ActiveRecordCustomer find(Database database, int id) {
        Row row = database.table(TABLE).select(id);
        if (row == null) {
            return null;
        }
        return new ActiveRecordCustomer(database, id, row.text("name"), row.text("email"),
                row.text("street"), row.text("city"), row.text("postcode"));
    }

    public void save() {
        Table table = database.table(TABLE);
        Row row = Row.of("name", name, "email", email,
                "street", street, "city", city, "postcode", postcode);
        if (table.peek(id) == null) {
            table.insert(id, row);
        } else {
            table.update(id, row);
        }
    }

    public int id() {
        return id;
    }

    public String name() {
        return name;
    }

    public String email() {
        return email;
    }

    public void changeEmail(String newEmail) {
        if (!newEmail.contains("@")) {
            throw new IllegalArgumentException("not an email address: " + newEmail);
        }
        this.email = newEmail;
    }

    public String city() {
        return city;
    }
}
