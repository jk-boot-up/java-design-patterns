package com.jk.explore.databaseperservicecontainers;

import static com.mongodb.client.model.Filters.eq;
import static com.mongodb.client.model.Filters.in;

import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.model.Aggregates;
import com.mongodb.client.model.Updates;
import java.util.ArrayList;
import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import org.bson.Document;

/**
 * The Catalog service. It owns the {@code catalog} database on MongoDB, and it holds a
 * client for that database and for nothing else.
 *
 * <p>Each product is one document in the {@code products} collection, filed under its sku.
 * Documents need not share a shape: a kettle can have a wattage and a mug a capacity, and
 * nobody has to change a table first.
 */
public class CatalogService implements AutoCloseable {

    public static final String DATABASE = "catalog";

    private final MongoClient client;
    private final MongoCollection<Document> products;
    private final RoundTrips roundTrips;

    /** The field this service's own code reads a product's name from. Its business alone. */
    private String nameField = "name";

    public CatalogService(Mongo mongo, RoundTrips roundTrips) {
        this.client = mongo.newClient();
        this.products = client.getDatabase(DATABASE).getCollection("products");
        this.roundTrips = roundTrips;
        products.drop();
    }

    /** Files one product document. Any extra fields go in as they are; there is no table to change. */
    public void add(String sku, String name, int priceInPence, int stock, Document extra) {
        Document product = new Document("_id", sku)
                .append(nameField, name)
                .append("priceInPence", priceInPence)
                .append("stock", stock);
        product.putAll(extra);
        products.insertOne(product);
    }

    /** The names of several products in one question: a single find with the skus listed. */
    public Map<String, String> namesFor(Collection<String> skus) {
        roundTrips.one();
        Map<String, String> names = new LinkedHashMap<>();
        for (Document p : products.find(in("_id", skus))) {
            names.put(p.getString("_id"), p.getString(nameField));
        }
        return names;
    }

    /** The field names one product document holds, in the order they were written. */
    public List<String> fieldsOf(String sku) {
        Document p = products.find(eq("_id", sku)).first();
        return p == null ? List.of() : new ArrayList<>(p.keySet());
    }

    /**
     * The Catalog team renames the name field in every document, and changes its own code
     * to match in the same release. Returns how many documents MongoDB changed.
     */
    public long renameNameFieldTo(String newField) {
        long changed = products.updateMany(new Document(), Updates.rename(nameField, newField)).getModifiedCount();
        nameField = newField;
        return changed;
    }

    /** Deletes a product. Returns how many documents MongoDB deleted. Nothing checks for orders. */
    public long delete(String sku) {
        return products.deleteOne(eq("_id", sku)).getDeletedCount();
    }

    public int stockOf(String sku) {
        Document p = products.find(eq("_id", sku)).first();
        return p == null ? -1 : p.getInteger("stock");
    }

    /** Takes items off the shelf. A MongoDB write, kept the moment it lands. */
    public void takeFromStock(String sku, int quantity) {
        products.updateOne(eq("_id", sku), Updates.inc("stock", -quantity));
    }

    /**
     * The old join, written MongoDB's way: for each product, look up the documents in a
     * collection called {@code orders} whose sku matches. That collection would have to be
     * in this same MongoDB database. The orders are in Postgres.
     *
     * @return for each product found, how many orders the lookup attached to it
     */
    public Map<String, Integer> tryToJoinOrders() {
        Map<String, Integer> attached = new LinkedHashMap<>();
        List<Document> joined = products.aggregate(List.of(
                Aggregates.sort(new Document("_id", 1)),
                Aggregates.lookup("orders", "_id", "sku", "orders"))).into(new ArrayList<>());
        for (Document p : joined) {
            attached.put(p.getString("_id"), p.getList("orders", Document.class).size());
        }
        return attached;
    }

    @Override
    public void close() {
        client.close();
    }
}
