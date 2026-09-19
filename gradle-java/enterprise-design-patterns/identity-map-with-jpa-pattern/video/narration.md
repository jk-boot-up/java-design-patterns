# Identity Map with JPA Pattern — Video Narration Script

## 1. Identity Map with JPA

Hello, and welcome. This video explains the Identity Map pattern inside J P A, in Java, and it is written and presented by Jayasekhar Konduru. It is the framework version of the Identity Map video. That one built the pattern by hand. This one shows the very same customer and order inside J P A, where you did not write the map. The plain definition, in short: keep one object for each database row, for as long as one session lasts. By the end you will see why loading the same customer twice gives the same object, why two sessions give two objects, and what happens to a change made to an object whose session has closed.

## 2. The Partner Project

This video assumes the Identity Map video. If you have not seen it, start there. It builds an identity map by hand, from plain Java, and shows why one row should be one object. This one uses the very same customer, number seven, and the very same order, number one hundred. It does not teach the pattern again. It shows what J P A does with it.

## 3. Before The First Annotation

Before the first annotation, two new things. Hibernate is the most widely used implementation of J P A. You mark your classes, and it turns operations on them into S Q L. H two is a database that runs inside the test, in memory, so nothing needs installing. And a promise: skipping this video loses none of the pattern. The hand-built one teaches all of it. This one only shows you where you have already met it.

## 4. Two Annotations

The customer class from the partner project gets two annotations. At entity says this class is stored. At id says which field is its identity. Nothing else about the class changed. Not one line of the logic.

## 5. One Persistence Context

Here is the moment. Ask the entity manager for customer seven, twice. Are the two the same object? True. And only one S Q L statement was issued. That is the identity map from the last project. You did not write it. It is called the persistence context, and every entity manager has one.

## 6. The Order's Customer

Load order one hundred, and ask it for its customer. Then ask for customer seven by id. Same object again. True. And one S Q L statement for the whole lot: the order and its customer, fetched once. Everything you saw in the hand-built project, now done for you.

## 7. Both Changes Are Kept

Now the bug from the hand-built project. One route moves her to York. Another changes her email. In the hand-built version, without a map, one of those changes vanished. Here, both are kept. There is only one object, so the second change cannot overwrite the first. And at commit, Hibernate writes a single update carrying both.

## 8. The Failure Of Its Own: Two Contexts

Now the failure of this project's own. The map belongs to one persistence context. Open a second one, and ask for customer seven. It has its own map. Is it the same object as the first context's? False. Equal by I D, but two objects. Each is free to disagree. The problem from the hand-built project, back again, just by opening a second context.

## 9. A Detached Change Is Not Saved

And worse. Close a context, and every object it loaded is detached. Change one. Move the customer to nowhere in particular. Then open a new context and look at the stored address. Still twelve Mill Lane, Leeds. The change was silently not saved. Nothing tracks a detached object. And there was no error at all.

## 10. Cost: The Context Is A Cache

The costs are the partner's, in framework clothes. First, the context is a cache. Another context commits a new email. This one still sees the old one, because it has no reason to look. The cure is refresh, which reloads the object from the database.

## 11. Cost: It Holds References

Second cost. The context holds every entity it loads. After loading one thousand customers, it holds one thousand entities, until clear is called. So its scope matters. In a Spring application the context normally lives for one transaction, or one request, which is why it does not grow forever.

## 12. Where You Have Met This

This is where you have already met it. Every J P A developer has used an identity map without knowing it. If a second find ever did not hit the database, or an entity failed to pick up another transaction's change, this was the reason.

## 13. What Was Used

For the record. Hibernate O R M seven point four point five, and H two two point four point two forty. The versions come from Spring Boot four point one point one's bill of materials, so they are ones that release was tested together. Spring Boot itself is not used in this video.

## 14. What Is Real Here

The same honest admission as everywhere in this course, and for once it is short. Everything here is real. The persistence context is Hibernate's. The S Q L counts come from Hibernate's own statistics. The only stand-in is the database, which is H two in memory.

## 15. When This Is Too Much

So when is it too much? If you use J P A, you already have it, and cannot turn it off. The lesson is simply knowing it is there.

## 16. Thanks for Watching

That's the Identity Map, in J P A. If you take one sentence away, take this one: the persistence context is an identity map, and it belongs to one entity manager. The full source, the written notes, the diagrams and an animated walkthrough are all in the repository. If you try one exercise, use merge to save the detached change, and look at what it returns. If this helped, a like genuinely does help other people find it, and subscribe if you would like the rest of the series. Thanks for watching.
