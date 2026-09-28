# Identity Map with JPA Pattern — Video Narration Script

## 1. Identity Map with JPA

Hello, and welcome. This video explains the Identity Map pattern, in Java, using J P A, Java's standard for storing objects in databases. This video is presented by Jayasekhar Konduru. First, a simple definition. An identity map keeps one object for each database row, for as long as one session lasts. Think of a hotel's key desk. While you are staying, there is one key for your room. Ask again, and you are handed the same key, not a new one. This is the framework version of the Identity Map video, with the same customer and order. We will hear why loading the same customer twice gives the same object. Why two sessions give two objects. And what happens to a change made to an object whose session has closed.

## 2. The Partner Project

Before we start, a quick note. This video has a partner: the hand-built Identity Map video. That one builds the map by hand, in plain Java, and shows why one row should be one object. Here, we use the very same customer, number seven, and the very same order, number one hundred. We will not teach the pattern again. Instead, we ask what J P A does with it.

## 3. Before The First Annotation

Two things are new in this project. First, Hibernate, the most widely used implementation of J P A. You mark your classes with annotations, and it turns work on those objects into database commands. Second, H2, a database that runs in memory, inside the test, so nothing needs installing. And one promise. If you skip this video, you lose none of the pattern. This one only shows you where you have already met it.

## 4. Two Annotations

The customer class from the partner project gets two annotations. At Entity says: this class is stored in the database. At Id says: this field is its identity. Nothing else about the class changed. Not one line of its logic.

## 5. One Persistence Context

First demo, and here is the key moment. Ask the entity manager for customer seven, twice. Are the two the same object? Yes. And only one database query was made. That is the identity map from the hand-built project. You did not write it. It is called the persistence context, and every entity manager has one.

## 6. The Order's Customer

Second demo: the order's customer. Load order one hundred, and ask it for its customer. Then ask for customer seven by I D. The same object again. And just one database query for all of it: the order, and its customer, fetched once. Everything from the hand-built project, now done for you.

## 7. Both Changes Are Kept

Third demo: both changes are kept. Remember the bug from the hand-built project? One route moves the customer to York. Another changes her email. Without a map, one of those changes vanished. Here, both are kept. There is only one object, so the second change cannot overwrite the first. And when the transaction commits, Hibernate writes one single update, carrying both changes.

## 8. The Failure Of Its Own: Two Contexts

Fourth demo: this project's own failure, two contexts. The map belongs to one persistence context. Open a second one, and ask for customer seven again. It has its own map. Is it the same object as the first context's? No. Equal by I D, but two separate objects, each free to disagree. The problem from the hand-built project is back, just by opening a second context.

## 9. A Detached Change Is Not Saved

And worse. When a context closes, every object it loaded becomes detached. Now change a detached customer's address. Then open a new context, and look at the stored address. It still says twelve Mill Lane, Leeds. The change was silently not saved. Nothing tracks a detached object. And there was no error at all.

## 10. Cost: The Context Is A Cache

Fifth demo: the context is a cache. Another context saves a new email address for the customer. This context still sees the old one. It has no reason to look again. The cure is a method called refresh, which reloads the object from the database. After refresh, it sees the new email.

## 11. Cost: It Holds References

Last demo: the context holds on to everything. After loading one thousand customers, the context holds all one thousand. Until a method called clear is called. So how long a context lives really matters. In a Spring application, it normally lives for one transaction, or one request. That is why it does not grow forever.

## 12. Where You Have Met This

Where have you met this before? Every J P A developer has used an identity map, often without knowing it. If a second lookup ever did not touch the database, this was why. And if an entity ever failed to see another transaction's change, this was why too.

## 13. What Was Used

For the record, here are the versions. Hibernate seven point four point five. And H2 two point four point two forty. These versions come from Spring Boot four point one point one's list of tested libraries. But Spring Boot itself is not used here.

## 14. What Is Real Here

A quick, honest note about this demo. Everything here is real. The persistence context is Hibernate's own. And the query counts come from Hibernate's own statistics. The only stand-in is the database, which is H2, in memory.

## 15. When This Is Too Much

So, when is this too much? If you use J P A, you already have an identity map, and you cannot turn it off. The lesson is simply knowing that it is there.

## 16. Thanks for Watching

That's the Identity Map, in J P A. If you remember one sentence, make it this one. The persistence context is an identity map, and it belongs to one entity manager. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Use the merge method to save the detached change. And look closely at what merge returns. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
