# Mediator Pattern — Video Narration Script

## 1. Mediator

Hello, and welcome. This video explains the Mediator pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. When a group of objects all affect each other, you have two choices. Connect every object to every other one. Or give them all one single object to talk to, which holds the rules. That single object is the mediator. Think of an airport control tower. Planes do not talk to each other. They all talk to the tower, and the tower tells each one what to do. In this video, we build the checkout page of an online shop. Choosing a delivery country changes the couriers, the gift wrapping, the total, and whether you may place the order at all. By the end, you will know why five controls can need nine connections, what that costs, and the one fair criticism of this pattern.

## 2. The Scenario

Here is the scenario: an online shop's checkout page, with five controls. The delivery country. The courier. A gift wrap option. The total. And the place order button. These five are connected by four rules. One. Changing the country changes the list of couriers, because different couriers serve different countries. Two. Gift wrapping is done by hand in the London warehouse, so it is only offered for UK orders. Three. The total follows the courier and the gift wrap. And four. The button may only be pressed when a country and a courier are both chosen. The rules are simple. The hard part is where they live.

## 3. Look Closely at One Click

Before any code, let's follow one click. A shopper has a UK order, with express shipping, gift wrapped, for forty-eight pounds. Then they change the country to the United States. The gift wrap option is correctly withdrawn, because the London warehouse cannot wrap this order. But the tick stays in the box. Withdrawing the option and clearing the tick were two separate steps, and only one was written. So the total is now forty-two pounds. And two pounds of that is for gift wrapping that will never happen. Nothing crashes, and nothing is logged. It looks like a normal checkout, with two pounds of pure fiction in it.

## 4. The Naive Approach — Everyone Wires Everyone

Here is why it happens. The obvious place for the rule, when the country changes, refresh the couriers, is inside the country control. So the country control is given a reference to the courier control. But gift wrap depends on the country too, so it needs that as well. And the total changes, so it needs the total. And the button might need checking, so it needs the button. That makes nine references, on a page with just five controls. Inside the country control's method, three of the four follow-up steps were remembered. The fourth, re-checking the button, was forgotten. Nobody was careless. The page is only correct if someone holds all five controls in their head, every time they change any one of them.

## 5. Why That Hurts

So what exactly is wrong? Four separate things. One. Nobody can see the whole form. What happens when the country changes is spread across three files, and no single file has the answer. Two. The bugs are missing lines. And you cannot review a line that was never written. Three. The connections grow faster than the form. Three controls can have six connections. Five controls, twenty. Ten controls, ninety. And four. No control can be built or tested alone. The country control needs four other controls just to exist.

## 6. The Mediator Pattern

Here is the pattern's definition, from the famous Gang of Four book. Define an object that encapsulates how a set of objects interact, and keep the objects from referring to each other directly. That has two halves. Keeping objects from referring to each other is the mechanism. Nine references become five. Encapsulating how they interact is the bigger benefit. After the change, there is one file, with one method, that tells you everything the page does. Nothing hides anywhere else.

## 7. An Analogy

Here is the analogy to hold on to: aircraft near an airport. Planes do not negotiate with each other about who lands first. They all talk to the control tower. The tower knows where everyone is, and tells each plane what to do. That is not because pilots cannot be trusted. It is simple arithmetic. Ten planes talking to each other means ninety conversations, and sooner or later, one is missed. Ten planes talking to one tower means just ten conversations. And all the rules are in one place. In our project, the checkout form is the tower, and the five controls are the planes.

## 8. The Roles

So here are the pieces. The Checkout Mediator interface has exactly one method, called changed. A control calls it to say, something about me changed. Controls report. They never ask. Every control extends a base class called Form Widget. It has two fields: a name, and the mediator. There is no field that could hold another control. So controls cannot tangle, even by accident. Then there are the five real controls: country, courier, gift wrap, the total, and the button. Each one knows the form. And the form knows all five. The shape is a star, not a web.

## 9. The Colleague — Notice What Is Missing

Let's look at a control, and notice what is missing. The base class has only two fields: a name, and the mediator. No field can hold another control. Now the country control. When a country is chosen, it stores the country, announces that it changed, and stops. That is the whole class. Compare it with the naive version, which had four follow-up steps, and still missed one. A control now only says, something about me is different. What that means for the rest of the page is not its business.

## 10. The Mediator — The Whole Page, in One Method

And here is the whole page, in one method, in the mediator. If the country changed, it refreshes the courier list, and sets whether gift wrap is offered. Then, whatever changed, it recalculates the total, and re-checks the button. Two things are worth noticing. First, the total and the button are refreshed after every change, with no special cases. So the mediator never needs to remember that clearing the courier affects the button. It simply checks again, every time. Simple and always right beats clever and sometimes wrong. Second, withdrawing the gift wrap offer also clears the tick, in the same method. There is no way to do only half of that. So there is nothing left to forget. One if statement. That is the entire control flow of the page.

## 11. The Tests — Asserting the Structure, Not Just the Behaviour

The project has fourteen tests. Two of them prove the pattern. A test like, choosing express makes the total forty-six pounds, passes for the tangled version too. So it proves nothing about the pattern. The first special test checks the structure. It looks at every field of every control, and fails if any field can hold another control. A comment saying, controls must not reference each other, lasts until the first person in a hurry. This test does not. The second test checks a wrong answer, on purpose. It confirms that the naive form still has the bug: the tick stays, and the total is forty-two pounds. The cost of that design is stated out loud, by the build.

## 12. Running It

Let's run the demo. The same page, the same three clicks, and the same change of mind. First, the tangled version. The total is forty-two pounds, with two pounds of phantom gift wrap. And the place order button still works, even though no courier is chosen. Now the mediated version. The tick disappeared when the offer did. The courier was cleared, so the total is back to just the basket. And the button switched itself off. Notice that nobody wrote code saying, when the country changes, disable the button. It just happens, because the mediator re-checks everything after every change.

## 13. What to Remember

So, what should you remember? When everything talks to everything, nobody can see the whole picture. Give them one place to talk to, and the rules have somewhere to live. People often confuse Mediator with Observer. The difference is knowledge. An observer's publisher knows nothing about its subscribers. A mediator knows all of its controls, on purpose. That knowledge is what lets it enforce a rule that spans several of them. A Facade also sits in front of several objects. But a facade faces outward, to make life simpler for an outside caller. A mediator faces inward. Now the honest cost, and this criticism is fair. Everything you take out of the controls goes into the mediator. On a real form, that class can grow huge. The answer is to split it, one mediator per section of the page, before it gets there. And for two controls that will never be three, direct wiring is clearer. This pattern pays off at about four or five interacting parts.

## 14. Thanks for Watching

That's the Mediator pattern. If you remember one sentence, make it this one. Give a group of objects one place to talk to, and their rules have one place to live. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. Here is one exercise to try. Give the country control a field that points at the total. Run the tests, and listen as the structure test names that field. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
