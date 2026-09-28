"""Scene definitions for the Prototype with Spring teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='Prototype with Spring',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the '
            'Prototype pattern, in Java, using Spring Boot. [[slnc 300]] '
            'This video is presented by Jayasekhar Konduru. [[slnc 600]] '
            'First, a simple definition. [[slnc 300]] The Prototype '
            'pattern makes new objects by copying an existing example. '
            '[[slnc 500]] In Spring, prototype is also the name of a '
            'scope. [[slnc 300]] Every time you ask for a '
            'prototype-scoped bean, Spring builds a new one from its '
            'definition. [[slnc 600]] Think of a cookie cutter. [[slnc '
            '300]] Every press makes a fresh cookie of the same shape. '
            '[[slnc 300]] But icing one cookie does not ice the next. '
            '[[slnc 700]] This is the framework version of the Prototype '
            'video, with the same product listings. [[slnc 400]] We will '
            'make the listing a prototype-scoped bean. [[slnc 300]] Then '
            'we will hear three surprises. [[slnc 300]] It is not a copy '
            'of your edited draft, it is built only once inside a '
            'singleton, and Spring never cleans it up.'
        ),
    ),
    dict(
        key='02-partner', kind='bullets', title='The Partner Project',
        body=['Prototype, the hand-built video,', 'copies a finished product listing', 'into variants.', '', 'It decided field by field what a', 'copy means, and kept a registry.', '', 'If you have not seen it, start there.'],
        narration=(
            'Before we start, a quick note. [[slnc 300]] This video has a '
            'partner: the hand-built Prototype video. [[slnc 400]] That '
            'one copies a finished product listing into variants. [[slnc '
            '300]] It decides field by field what a copy means, and keeps '
            'a registry of templates. [[slnc 500]] If you are new to the '
            'pattern, watch that one first. [[slnc 400]] Here, we ask '
            'what Spring Boot does with the same idea.'
        ),
    ),
    dict(
        key='03-dependencies', kind='bullets', title='Before The First Line',
        body=['One thing is new: Spring Boot.', '', 'Its prototype scope builds a new', 'bean on every request.', '', 'Skipping this video loses none', 'of the pattern.'],
        narration=(
            'One thing is new in this project: Spring Boot. [[slnc 400]] '
            'At its heart, Spring is a container that creates your '
            'objects. [[slnc 400]] It has a prototype scope, which builds '
            'a new bean for every request. [[slnc 500]] And one promise. '
            '[[slnc 300]] If you skip this video, you lose none of the '
            'pattern. [[slnc 300]] This one is about the tool.'
        ),
    ),
    dict(
        key='04-fresh', kind='console', title='A New One Each Time',
        body="""ONE. A new one each time.
  same object: false.
  both are titled Untitled.""",
        narration=(
            'First demo: a new one each time. [[slnc 400]] Ask the '
            'container for a listing, twice. [[slnc 300]] You get two '
            'different objects. [[slnc 300]] Both are titled untitled, '
            'straight from the definition.'
        ),
    ),
    dict(
        key='05-independent', kind='console', title='Independent',
        body="""TWO. Independent.
  a: Blue Mug, 2 images.
  b: Untitled, 1 image.""",
        narration=(
            'Second demo: they are independent. [[slnc 400]] Give the '
            'first listing a title, blue mug, and an extra picture. '
            '[[slnc 300]] The second listing still says untitled, with '
            'one picture. [[slnc 500]] So far, this looks exactly like '
            'the pattern.'
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
            'Third demo: the difference that matters. [[slnc 400]] Edit a '
            'draft listing, then ask the container for another. [[slnc '
            '300]] You get an untitled one. [[slnc 500]] The container '
            'builds from the definition, not from your draft. [[slnc '
            "300]] Only the draft's own copy method carries your edits "
            'across. [[slnc 500]] Spring gives you the scope. [[slnc '
            '300]] Copying is still your job.'
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
            'Fourth demo: the classic trap. [[slnc 400]] A singleton '
            'receives a prototype listing in its constructor. [[slnc '
            '300]] But the constructor only runs once. [[slnc 300]] So '
            'the listing is built only once. [[slnc 500]] Every call '
            'returns the same listing. [[slnc 300]] One caller sets the '
            'title to blue mug. [[slnc 300]] And the next caller sees '
            'blue mug too. [[slnc 500]] The bean is a prototype in name '
            'only.'
        ),
    ),
    dict(
        key='08-provider', kind='console', title='Ask Each Time',
        body="""FIVE. Ask each time.
  two calls, same object: false.
  the second caller sees:
  Untitled.""",
        narration=(
            'Fifth demo: the fix. [[slnc 400]] Instead of the listing '
            'itself, the singleton receives an Object Provider. [[slnc '
            '300]] And it asks the provider for a listing each time it '
            'needs one. [[slnc 500]] Now every call builds a new listing. '
            '[[slnc 300]] And the second caller sees an untitled one.'
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
            'Last demo: nobody cleans up. [[slnc 400]] Three listings are '
            'built. [[slnc 300]] Then the container is closed. [[slnc '
            '500]] None of the three listings is cleaned up. [[slnc 300]] '
            "But the singleton's clean-up method does run, once. [[slnc "
            '500]] Spring builds a prototype, and then lets go of it. '
            '[[slnc 300]] If yours holds a file, or a connection, closing '
            'it is your job.'
        ),
    ),
    dict(
        key='10-verdict', kind='bullets', title='The Verdict',
        body=['Prototype scope for fresh objects.', '', 'A provider inside singletons.', '', 'Your own copy for edited drafts.', '', 'Clean up after it yourself.'],
        narration=(
            'So, here is the verdict. [[slnc 400]] Use the prototype '
            'scope when you want a fresh object. [[slnc 300]] Inside a '
            'singleton, ask for it through a provider. [[slnc 300]] Copy '
            'an edited draft with a copy method of your own. [[slnc 300]] '
            'And clean up after it yourself.'
        ),
    ),
    dict(
        key='11-recognise', kind='bullets', title='How To Recognise It',
        body=['@Scope prototype on a class.', '', 'An ObjectProvider in a constructor.', '', 'getBean in a loop.'],
        narration=(
            'How can you spot this in code someone else wrote? [[slnc '
            '400]] Look for a scope annotation that says prototype. '
            '[[slnc 300]] An Object Provider passed into a constructor. '
            '[[slnc 300]] Or get bean, called inside a loop.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['Per-request helpers, stateful', 'builders and command objects.', '', 'Any bean marked prototype.'],
        narration=(
            'Where have you met this before? [[slnc 300]] In helpers '
            'created fresh for each request, builders that hold state, '
            'and command objects. [[slnc 300]] Any bean marked prototype.'
        ),
    ),
    dict(
        key='13-versions', kind='bullets', title='What Was Used',
        body=['Spring Boot 4.1.1.', '', 'No web server, no database,', 'no web starter.'],
        narration=(
            'For the record, here are the versions. [[slnc 300]] Spring '
            'Boot four point one point one. [[slnc 300]] No web server, '
            'no database, and no web library.'
        ),
    ),
    dict(
        key='14-real', kind='bullets', title='What Is Real Here',
        body=["Everything is real: Spring's", 'container and its scopes.', '', 'Nothing here depends on timing.'],
        narration=(
            "A quick, honest note about this demo. [[slnc 300]] Spring's "
            'container, and its scopes, are real. [[slnc 300]] And '
            'nothing here depends on timing.'
        ),
    ),
    dict(
        key='15-too-much', kind='bullets', title='When This Is Too Much',
        body=['If the object is cheap and has no', 'state to configure, new is simpler', 'than a scope.'],
        narration=(
            'So, when is this too much? [[slnc 400]] If the object is '
            'cheap, and has nothing to configure, simply creating it with '
            'new is easier than a scope.'
        ),
    ),
    dict(
        key='16-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Inject a listing into a second', 'singleton and predict what its callers see.'],
        narration=(
            "That's Prototype with Spring. [[slnc 400]] If you remember "
            "one sentence, make it this one. [[slnc 300]] Spring's "
            'prototype is a new bean built from its definition, not a '
            'copy of your draft. [[slnc 500]] The full source code, '
            'written notes, diagrams, and an animated walkthrough are all '
            'in the repository. [[slnc 500]] Here is one exercise to try. '
            '[[slnc 300]] Inject a listing into a second singleton. '
            '[[slnc 300]] And predict what its callers will see, before '
            'you run it. [[slnc 500]] If this helped, a like really does '
            'help other people find it. [[slnc 300]] And subscribe, if '
            "you'd like the rest of the series. [[slnc 400]] Thanks for "
            'watching.'
        ),
    ),
]
