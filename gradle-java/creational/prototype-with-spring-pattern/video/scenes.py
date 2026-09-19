"""Scene definitions for the Prototype with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Prototype with Spring',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the Prototype '
            'pattern with Spring Boot, in Java, and it is written and '
            'presented by Jayasekhar Konduru. [[slnc 300]] It is the '
            'framework version of the Prototype video. That one copied a '
            'fully assembled product listing into variants, deciding '
            'field by field what a copy means, and kept a registry of '
            'templates. This one shows the same idea inside Spring Boot. '
            '[[slnc 350]] The plain definition, in short: in Spring, a '
            'prototype is a scope. Every request for the bean builds a '
            'new one from its definition. [[slnc 300]] By the end you '
            'will see the listing as a prototype-scoped bean, then see '
            'the three ways it surprises people: it is not a copy of an '
            'edited draft, it is built only once inside a singleton, and '
            'Spring never destroys it.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Prototype, the hand-built video,', 'copies a finished product listing', 'into variants.', '', 'It decided field by field what a', 'copy means, and kept a registry.', '', 'If you have not seen it, start there.'],
        narration=(
            'This video assumes the Prototype video. If you have not seen '
            'it, start there. It copies a finished product listing into '
            'variants, decides field by field what a copy means, and '
            'keeps a registry of templates. [[slnc 300]] This one uses '
            'the same example. It does not teach the pattern again. It '
            'shows what Spring Boot does with it.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its prototype scope builds a new', 'bean on every request.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'Before the first line of code, what Spring Boot is. Spring '
            'is a framework whose core is a container that creates your '
            'objects. It has a prototype scope, which builds a new bean '
            'for every request. [[slnc 300]] And a promise: skipping this '
            'video loses none of the pattern. The hand-built one teaches '
            'all of it.'
        ),
    ),
    dict(
        key='04-fresh', kind='console', title='A New One Each Time',
        body="""ONE. A new one each time.
  same object: false.
  both are titled Untitled.""",
        narration=(
            'First, the scope. Ask the container for a listing twice, and '
            'you get two different objects. Both are untitled, straight '
            'from the definition.'
        ),
    ),
    dict(
        key='05-independent', kind='console', title='Independent',
        body="""TWO. Independent.
  a: Blue Mug, 2 images.
  b: Untitled, 1 image.""",
        narration=(
            'Second, they are independent. Give one a title and an extra '
            'image. The other still says untitled, with one image. So far '
            'this looks like the pattern.'
        ),
    ),
    dict(
        key='06-definition', kind='console', title='A Definition, Not A Draft',
        body="""THREE. A definition.
  asked the container again:
  Untitled, 1 image.

  asked the draft to copy():
  Blue Mug, 2 images.""",
        narration=(
            'Third, the difference that matters. Edit a draft, then ask '
            'the container for another listing. You get an untitled one. '
            'The container builds from the definition, not from your '
            "draft. [[slnc 300]] Only the draft's own copy method carries "
            'the edits. Spring gives you the scope. The copy is still '
            'your job.'
        ),
    ),
    dict(
        key='07-trap', kind='console', title='A Prototype Inside A Singleton',
        body="""FOUR. In a singleton.
  two calls, same object: true.

  the second caller sees the
  first caller's title:
  Blue Mug.""",
        narration=(
            'Fourth, the classic trap. A singleton takes a prototype in '
            'its constructor. The constructor runs once, so the listing '
            'is built once. Every call returns the same object. [[slnc '
            '300]] One caller sets a title, and the next caller sees it. '
            'The bean is a prototype in name only.'
        ),
    ),
    dict(
        key='08-provider', kind='console', title='Ask Each Time',
        body="""FIVE. Ask each time.
  two calls, same object: false.
  the second caller sees:
  Untitled.""",
        narration=(
            'Fifth, the fix. Inject an object provider, and ask it each '
            'time. Every call builds a new listing. The second caller '
            'sees an untitled one.'
        ),
    ),
    dict(
        key='09-cleanup', kind='console', title='Nobody Cleans Up',
        body="""SIX. Nobody cleans up.
  listings built: 3.
  destroyed on close: 0.

  the singleton's destroy
  method ran 1 time.""",
        narration=(
            'Last, cleanup. Build three listings, and close the '
            "container. None of the three is destroyed. The singleton's "
            'destroy method runs once. [[slnc 300]] Spring builds a '
            'prototype and lets go of it. If yours holds a file or a '
            'connection, closing it is your job.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Prototype scope for fresh objects.', '', 'A provider inside singletons.', '', 'Your own copy for edited drafts.', '', 'Clean up after it yourself.'],
        narration=(
            'My verdict, plainly. Use the prototype scope for a fresh '
            'object. Ask for it through a provider inside a singleton. '
            'Copy an edited draft with a copy method of your own. And '
            'clean up after it yourself.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Scope prototype on a class.', '', 'An ObjectProvider in a constructor.', '', 'getBean in a loop.'],
        narration=(
            'How do you recognise this in code you did not write? A scope '
            'annotation naming prototype. An object provider in a '
            'constructor. Or get bean, called in a loop.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Per-request helpers, stateful', 'builders and command objects.', '', 'Any bean marked prototype.'],
        narration=(
            'You have met this in per request helpers, stateful builders '
            'and command objects. Any bean marked prototype.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record. Spring Boot four point one point one. No web '
            'server, no database, and no web starter.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'container and its scopes.', '', 'Nothing here depends on timing.'],
        narration=(
            'The same honest admission as everywhere in this course. '
            "Everything is real: Spring's container and its scopes. "
            'Nothing here depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the object is cheap and has no', 'state to configure, new is simpler', 'than a scope.'],
        narration=(
            'So when is it too much? If the object is cheap and has no '
            'state to configure, new is simpler than a scope.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Inject a listing into a second', 'singleton and predict what its callers see.'],
        narration=(
            "That's Prototype with Spring. [[slnc 250]] If you take one "
            "sentence away, take this one: Spring's prototype is a new "
            'bean from the definition, not a copy of a draft. [[slnc '
            '350]] The full source, the written notes, the diagrams and '
            'an animated walkthrough are all in the repository. [[slnc '
            '300]] If you try one exercise, inject a listing into a '
            'second singleton, and predict what its callers see. [[slnc '
            '300]] If this helped, a like genuinely does help other '
            'people find it, and subscribe if you would like the rest of '
            'the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
