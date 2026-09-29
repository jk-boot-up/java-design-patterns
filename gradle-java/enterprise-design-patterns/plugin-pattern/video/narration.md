# Plugin Pattern — Video Narration Script

## 1. Plugin

Hello, and welcome. This video explains the Plugin pattern, in Java. This video is presented by Jayasekhar Konduru. First, a simple definition. With plugins, the code only asks for what it needs by interface, such as a payment gateway. A configuration file for each environment says which class plays that part. And one factory creates it. Think of a theatre. The script says Hamlet enters, but never which actor. A cast sheet on the noticeboard says who plays each part tonight. To change the actor, you change the sheet, not the script. In this video, the domain is an online shop. It runs in development, staging, and production. Only production may charge real cards, or send real emails. By the end, you will hear how scattered choices went wrong. How plugins fix it. How to add an environment without code. And what you give up.

## 2. The Scenario

Here is the scenario. The shop runs in three environments. Development on laptops. Staging, for testing. And production, for real customers. Real card payments and real emails must only happen in production. Every place in the code that needed a payment gateway or an emailer chose one itself, with an if statement on the environment's name.

## 3. Act One — Choices scattered in code

First demo: each place picks its own implementation, from the environment name. The shop runs in development, staging, and production. Only production should charge real cards, or send real emails. When staging was added, the payment code was updated. Staging uses the fake gateway. The email code was missed. It only knew about development. So staging fell through to the real emailer, and sent a real customer an email.

## 4. Act Two — Plugins from configuration

Second demo: plugins, chosen by configuration. Each environment has one small file. It says which class plays each part. Payment gateway: the fake one. Emailer: the sandbox one. One factory reads the file and creates the objects. Checkout only ever names the interfaces. In development, the gateway is fake and the emails stay in a sandbox. In production, the card is really charged, and the email is really sent.

## 5. Act Three — A new environment

Third demo: a new environment is a new file, not new code. Staging gets its own file. Two lines. Fake gateway, sandbox emailer. No Java changes at all. And there is no second place to forget. Priya's email stays in the sandbox inbox.

## 6. Act Four — Caught at startup

Fourth demo: a bad entry is caught when the shop starts. Someone misspells a class name in the demo environment's file. When the shop starts, the factory tries to create every plugin, once. It reports: cannot create sandbox emaler, for the emailer. The mistake is found before the first customer, not by the first customer.

## 7. Act Five — The bill

Fifth demo: the bill. The compiler cannot see the wiring. A misspelt class name is a startup error, not a compile error. And if a developer searches the code for who uses the sandbox emailer, they find nothing. It is only named in text files.

## 8. The Pattern

Let's name the pattern. The code only asks for interfaces. Payment gateway. Emailer. Each environment has one configuration file. Each line says: this interface, that class. One factory reads the file, creates the objects, and checks them all when the shop starts.

## 9. Who Does What

Here is who does what. Payment gateway and emailer are the interfaces. Card gateway, fake gateway, SMTP emailer, and sandbox emailer are the classes that can play those parts. The properties files are the cast sheets, one per environment. The plugin factory reads the right sheet and creates the objects. And scattered choices is the old way, kept for comparison.

## 10. Where You Have Seen It

You have probably met this pattern already. Java's service loader finds implementations listed in files. Spring profiles choose different beans for different environments. And J D B C drivers, and logging libraries such as SLF4J, pick their implementation the same way.

## 11. When To Use It

So, when should you use it? When implementations differ between environments or deployments. Keep all the wiring in one factory. Check every plugin when the program starts. And if you already use Spring, use its profiles, rather than writing your own factory.

## 12. Thanks for Watching

That's the Plugin pattern. If you remember one sentence, make it this one. The code names the part, and a file per environment names the actor. The full source code, written notes, diagrams, and an animated walkthrough are all in the repository. It runs offline, with nothing installed except a Java development kit. Here is one exercise to try. Make the factory refuse to start production if any plugin is a fake. If this helped, a like really does help other people find it. And subscribe, if you'd like the rest of the series. Thanks for watching.
