"""Scene definitions for the DTO teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='DTO',
        body=None,
        narration=(
            'Hello, and welcome. This video explains the D T O pattern in '
            'Java, and it is written and presented by Jayasekhar Konduru. '
            '[[slnc 300]] The plain definition: a D T O, a data transfer '
            'object, is a small object built just for crossing a '
            'boundary, carrying only what the other side needs, so your '
            'real objects never have to leave. [[slnc 350]] This is the '
            'last hand-built project in the enterprise category. In our '
            'online store, it is what a customer endpoint should return. '
            '[[slnc 300]] By the end you will know what goes wrong when '
            'you return the domain object, why renaming a private field '
            'can break a client, what a D T O costs, and why D T Os '
            'multiply.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A REST endpoint returns a customer.', '', 'The client wants the name and the city.', '', 'What should the endpoint send?'],
        narration=(
            'Here is the scenario. A rest endpoint returns a customer. '
            "[[slnc 300]] The client, a web page, wants the customer's "
            'name and city. [[slnc 300]] The question this video answers: '
            'what should the endpoint actually send?'
        ),
    ),
    dict(
        key='03-leak', kind='console', title='Return The Domain Object',
        body="""ONE. The domain object.
  contains the password hash:
  true

  order history in it: true,
  loaded just to serialise

  size: 5297 characters,
  for a name and a city.""",
        narration=(
            'The easy answer is to return the customer object itself. '
            'Here it is, written out by a small serialiser that walks '
            'every field, exactly as a real one does. [[slnc 300]] '
            'Everything is in it. The password hash is in it. The whole '
            'order history is in it, because walking every field touched '
            'the lazy collection, and loaded it. [[slnc 300]] Five '
            'thousand two hundred and ninety-seven characters, for a name '
            'and a city.'
        ),
    ),
    dict(
        key='04-rename', kind='console', title='The Keys Are Private Names',
        body="""TWO. The keys.
  the client reads: name

  a developer renames the
  private field name to
  fullName.

  the client reads the key
  name: null""",
        narration=(
            'There is a quieter problem. The keys in that JSON are the '
            'names of the private fields. [[slnc 300]] A developer tidies '
            'the customer class, and renames the private field name to '
            'full name. It compiles. The customer tests pass. [[slnc '
            '300]] The JSON now has full name, and the client, still '
            'reading the key name, gets nothing. A private field became a '
            'public contract without anyone deciding it.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['A separate object, built for the boundary.', '', 'A Java record: flat, immutable,', 'exactly the fields the client needs.', '', 'The domain object stays inside.'],
        narration=(
            'The pattern is a separate object, built for the boundary. In '
            'modern Java it is a record: flat, immutable, with exactly '
            'the fields the client needs. [[slnc 300]] The domain object '
            'stays inside. A small piece of mapping code copies the '
            'fields across.'
        ),
    ),
    dict(
        key='06-dto-payload', kind='console', title='A DTO Payload',
        body="""THREE. The pattern.
  domain object: 5297 chars
  DTO:             46 chars

  {"id":7,
   "name":"Ada Lovelace",
   "city":"London"}

  history loaded: 0 times.""",
        narration=(
            'Now the same endpoint with a D T O. The domain object was '
            'five thousand two hundred and ninety-seven characters. The D '
            'T O is forty-six. [[slnc 300]] Just an id, a name and a '
            'city. The password hash cannot leak, because the record has '
            'no field for it. The history is never touched. And the keys '
            'are now a contract that someone chose, not the accident of a '
            "private field's name."
        ),
    ),
    dict(
        key='07-not-model', kind='console', title='A DTO Is Not A Domain Model',
        body="""FOUR. One of each.
  CustomerDto: a record,
  methods of its own: none

  Customer has rules:
  changeEmail, earnPoints

  the domain refuses a bad
  email. the DTO would not.""",
        narration=(
            'A D T O is not a domain model, and the project shows one of '
            'each. [[slnc 300]] The customer D T O is a record with no '
            'behaviour. The customer domain object has rules. It refuses '
            'an email with no at sign. [[slnc 300]] The D T O would carry '
            'a bad email without a word. It is data, not a model. '
            'Confusing the two is how anemic domains start.'
        ),
    ),
    dict(
        key='08-mapping', kind='console', title='Cost One: Mapping Code',
        body="""FIVE. Mapping.
  CustomerDto: 3 fields
  CustomerSummaryDto: 2
  CustomerListItemDto: 4
  CustomerDetailDto: 6

  Customer has 7 fields.
  four DTOs carry 15.""",
        narration=(
            'Now the bill. First, mapping code, everywhere. Every D T O '
            'needs a method that copies fields across by hand. It is '
            'tedious. [[slnc 300]] And a new field on the domain object '
            'silently does not reach a D T O that nobody remembered to '
            'update. Nothing warns you.'
        ),
    ),
    dict(
        key='09-multiply', kind='bullets', title='Cost Two: DTOs Multiply',
        body=['CustomerDto, CustomerSummaryDto,', 'CustomerListItemDto, CustomerDetailDto.', '', 'Near-duplicates that drift,', 'until the mapping layer is larger', 'than the domain it protects.'],
        narration=(
            'Second cost. D T Os multiply. There is a customer D T O, '
            'then a summary one, then a list item one, then a detail one. '
            'Near-duplicates, each a little different. [[slnc 300]] They '
            'drift apart. And in a big system the mapping layer can '
            'become larger than the domain it was meant to protect.'
        ),
    ),
    dict(
        key='10-loads', kind='bullets', title='Cost Three: The Mapping Decides What Loads',
        body=['The detail DTO asks for the order count.', 'That touches the lazy history,', 'and loads it.', '', 'A DTO can hide the cost,', 'but only if the mapping does.'],
        narration=(
            'Third cost. The mapping decides what gets loaded. The detail '
            'D T O includes an order count. To get it, the mapper asks '
            'the customer for its orders, and that loads the whole '
            'history. [[slnc 300]] A D T O can hide a cost from the '
            'client, but only if the mapping code stays careful.'
        ),
    ),
    dict(
        key='11-bff', kind='bullets', title='Where This Sits',
        body=['This is Backends for Frontends,', 'at the level of one object,', 'not one deployment.', '', 'Same idea: shape what leaves', 'for who receives it.'],
        narration=(
            'There is a link to another pattern in this course. This is '
            'Backends for Frontends, at the level of one object instead '
            'of one deployment. Same idea: shape what leaves for whoever '
            'is receiving it.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A Java record returned from a Spring', 'controller is a DTO.', 'Jackson writes its JSON.', '', 'MapStruct writes the mapping code,', 'and is worth taking once you have', 'felt the tedium by hand.'],
        narration=(
            'You have met this. A Java record returned from a Spring '
            'controller is a D T O, and Jackson writes its JSON. [[slnc '
            '300]] There is a library called MapStruct that writes the '
            'mapping code for you. It is worth taking, but only after you '
            'have felt the tedium by hand, so you know what it is saving '
            'you.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The serialiser here is small, and', 'not Jackson.', '', 'But it does the same thing: it walks', 'every field. That is why the leak', 'is real.'],
        narration=(
            'The same honest admission as everywhere in this course. The '
            'serialiser here is small, and it is not Jackson. [[slnc '
            '300]] But it does what any serialiser does: it walks every '
            'field it can reach. That is why the leak, and the rename '
            'problem, are real.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['An internal call between two classes', 'in one module: a needless copy.', '', 'It earns its place at a boundary you', 'do not control: an API, a message,', 'a file.'],
        narration=(
            'So when is it too much? For an internal call between two '
            'classes in one module, a D T O is a needless copy. [[slnc '
            '300]] It earns its place at a boundary you do not control: a '
            'public A P I, a message, a file.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a phone field to the customer,', 'and see which classes change.'],
        narration=(
            "That's the D T O. [[slnc 250]] If you take one sentence "
            'away, take this one: a D T O is a contract, and the mapping '
            'code is what you pay for one. [[slnc 350]] The full source, '
            'the written notes, the diagrams and an animated walkthrough '
            'are all in the repository, running offline with nothing '
            'installed but a Java development kit. [[slnc 300]] If you '
            'try one exercise, add a phone field to the customer, and see '
            'which classes must change to show it, and which to hide it. '
            '[[slnc 300]] If this helped, a like genuinely does help '
            'other people find it, and subscribe if you would like the '
            'rest of the series. [[slnc 250]] Thanks for watching.'
        ),
    ),
]
