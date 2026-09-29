# Private Class Data Pattern — Video Narration Script

## 1. Private Class Data

Hello, and welcome. This video explains the Private Class Data pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. Private class data moves the values a class must never change into a separate, private data object. That object cannot be changed. So not even the class's own methods can overwrite those values. Think of a museum exhibit in a glass case. The staff clean the glass and count the visitors every day. But nobody, not even the staff, can pick up the exhibit and alter it. In this video, the domain is an online shop. It prints invoices, and staff sometimes print one with a staff discount shown. By the end, you will hear how a class can damage its own data. How a private data object stops it. How working state can still change. And when this is just ceremony.

## 2. The Scenario

Here is the scenario. Invoice seven is for one hundred pounds. Staff can print it with a ten percent staff discount shown, for their own records. The print method took a shortcut. Let's see what that did.

## 3. Act One — A method changes its own figures

First demo: the invoice's own method changes its figures. Invoice seven is for one hundred pounds. It is printed with a ten percent staff discount shown. The print method takes a shortcut. It takes the discount off the stored total, then prints it. First print: ninety pounds. Second print: eighty-one pounds. The invoice itself now says eighty-one pounds. It was issued for one hundred.

## 4. Act Two — Private class data

Second demo: the figures live in a private data object. The invoice's number, customer, and total move into a small record. The invoice keeps that record privately. Now the print method works out the discount in a local variable. It cannot change the stored total. Print it three times. Ninety pounds, every time. And the invoice still says one hundred.

## 5. Act Three — Nothing can write

Third demo: nothing can write the figures, not even the invoice itself. The data record has no setters. Its fields are final, which means they are set once, and never again. So the shortcut from the first demo would not even compile. The mistake is stopped before the program ever runs.

## 6. Act Four — Working state beside the data

Fourth demo: working state can still change, beside the data. The invoice counts how many times it was printed. That counter is an ordinary field, and it says three. The figures in the data object have not moved. Still one hundred pounds. Like the museum case: the visitor count changes, the exhibit does not.

## 7. Act Five — The bill

Fifth demo: the bill. There is one more class, the data record. And every read takes one more hop, through the data object. For a small class with no risky methods, that is just ceremony. Final fields alone would be enough.

## 8. The Pattern

Let's name the pattern. Find the values that must never change after the object is made. Move them into a small data object, with final fields and no setters. Keep it private. Values that are meant to change, such as a counter, stay ordinary fields beside it. The class can read its data. It cannot write it.

## 9. Who Does What

Here is who does what. The invoice prints itself, and counts how often. Invoice data is a record holding the number, the customer, and the total. Set once, never changed. Times printed is the ordinary field beside it. And loose invoice is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Any class holding a private final field of some data type, and reading from it, is using it. Read-only configuration objects passed into a service are the same idea. And records kept inside services and entities, to group the values that must not change.

## 11. When To Use It

So, when should you use it? When a class holds important figures alongside working state that must change. Or when you want to lock down a group of fields in older code, without rewriting the class. And when every value should be fixed, skip this. Make the whole object immutable instead.

## 12. Thanks for Watching

That's the Private Class Data pattern. If you remember one sentence, make it this one. Protect the figures that must not change, even from their own class. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Inside the invoice, try to change the stored total. And read what the compiler says. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
