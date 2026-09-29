# Scheduler Pattern — Video Narration Script

## 1. Scheduler

Hello, and welcome. This video explains the Scheduler pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When many threads wait for one shared resource, a scheduler decides whose turn comes next. It follows a policy, such as most urgent first. And the policy can be swapped, without touching anything else. Think of the triage nurse in a hospital's emergency department. Patients are not seen in the order they walked in. The nurse decides, by urgency. And someone who has waited a very long time is eventually moved up. In this video, the domain is an online shop's warehouse. Six packing stations share one label printer. Express orders must catch the afternoon van. By the end, you will hear why a lock alone serves the wrong job first. How a scheduler fixes it. How to swap the policy. And how to make sure nobody waits for ever.

## 2. The Scenario

Here is the scenario. The warehouse has one label printer, and six packing stations. Some orders are express, and must catch the afternoon van. The printer was guarded by a fair lock. A fair lock serves whoever arrived first.

## 3. Act One — A fair lock

First demo: a fair lock, first come, first served. The printer is busy with a bulk job. Three standard jobs arrive. Then three express jobs. The lock serves them in the order they arrived. Standard one, two, three. Then express one, two, three. The express orders waited behind every standard order, and may miss the van.

## 4. Act Two — Express first

Second demo: a scheduler, with an express-first policy. Each station asks the scheduler for its turn, and waits. When the printer is free, the policy chooses who goes next. Express one, two, three. Then standard one, two, three.

## 5. Act Three — A replaceable policy

Third demo: the policy is replaceable. Swap in a different rule: smallest job first. The jobs with the fewest labels print first, whatever their type. One line changed. The stations and the printer did not.

## 6. Act Four — Nobody waits for ever

Fourth demo: nobody waits for ever. One standard job arrives. Then a rush of five express jobs. With express first alone, the standard job goes last. In a longer rush, it would never print. Now add a rule: a job overtaken three times moves to the front. The standard job prints fourth.

## 7. Act Five — The bill

Fifth demo: the bill. Someone has to decide, every time. Each job takes the scheduler's lock, joins its list, and is woken to check whether it is next. And every priority rule needs a guard, so the jobs it does not favour are never starved.

## 8. The Pattern

Let's name the pattern. Each thread asks the scheduler for its turn, and waits. When the resource is free, the policy picks who goes next. The policy is a simple rule, kept in one place. And long waiters are aged, so nobody is starved.

## 9. Who Does What

Here is who does what. The scheduler keeps the waiting list. Stations call enter, and done. The policy is a comparator: express first, or smallest first. A print job knows if it is express, how many labels it has, and how often it has been overtaken. The printer is the shared resource. And the fair lock is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Your operating system schedules which program runs on the processor next. A priority blocking queue in front of one worker thread does the same job. Print queues and build servers schedule their jobs. And Kubernetes schedules containers by priority.

## 11. When To Use It

So, when should you use it? When the order of access to a shared resource matters, and may change. Keep the policy in one comparator. Age long waiters, so nobody starves. And when callers do not need to wait for their turn, a priority queue and one worker thread is simpler.

## 12. Thanks for Watching

That's the Scheduler pattern. If you remember one sentence, make it this one. Let a policy decide who goes next, and make sure nobody waits for ever. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Give each job a deadline, and print the one closest to its deadline first. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
