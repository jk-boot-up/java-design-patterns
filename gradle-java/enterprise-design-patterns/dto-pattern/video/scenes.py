"""Scene definitions for the DTO teaching video.

Each scene has: key, title, kind, body, narration.

Narration speaks the counts out loud and never points at a picture.
"""

SCENES = [
    dict(
        key='01-poster', kind='poster', title='DTO',
        body=None,
        narration=(
            'Hello, and welcome. [[slnc 400]] This video explains the D T '
            'O pattern, in Java. [[slnc 300]] D T O stands for Data '
            'Transfer Object. [[slnc 300]] This video is presented by '
            'Jayasekhar Konduru. [[slnc 600]] First, a simple definition. '
            '[[slnc 300]] A data transfer object is a small object built '
            'only for crossing a boundary. [[slnc 300]] It carries just '
            'what the other side needs. [[slnc 300]] So your real '
            'business objects never have to leave. [[slnc 600]] Think of '
            'a postcard, instead of sending your whole diary. [[slnc '
            '300]] You write only what the reader needs to know. [[slnc '
            '700]] In our online store, the question is: what should a '
            'customer web service return? [[slnc 500]] By the end, you '
            'will know what goes wrong when you return the real object. '
            '[[slnc 300]] Why renaming a private field can break a '
            'client. [[slnc 300]] What a D T O costs. [[slnc 300]] And '
            'why D T Os multiply.'
        ),
    ),
    dict(
        key='02-scenario', kind='bullets', title='The Scenario',
        body=['A REST endpoint returns a customer.', '', 'The client wants the name and the city.', '', 'What should the endpoint send?'],
        narration=(
            'Here is the scenario. [[slnc 400]] A web service returns a '
            'customer. [[slnc 300]] The client, a web page, only wants '
            "the customer's name, and city. [[slnc 500]] So here is the "
            'question. [[slnc 300]] What should the web service actually '
            'send?'
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
            'The easy answer: return the customer object itself. [[slnc '
            '400]] A small serialiser writes it out as JSON, by walking '
            'every field, exactly as a real one does. [[slnc 500]] '
            'Everything is in there. [[slnc 300]] The password hash is in '
            'there. [[slnc 300]] The whole order history is in there too. '
            '[[slnc 300]] Walking every field touched the order history, '
            'so it was loaded from the database, just to be written out. '
            '[[slnc 500]] The result is five thousand two hundred and '
            'ninety-seven characters, for a name and a city.'
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
            'There is a quieter problem too. [[slnc 400]] The keys in '
            "that JSON are the names of the class's private fields. "
            '[[slnc 500]] A developer tidies the customer class, and '
            'renames the private field name to full name. [[slnc 300]] It '
            'compiles, and the customer tests pass. [[slnc 500]] But the '
            'JSON now says full name. [[slnc 300]] And the web page, '
            'still reading the key called name, gets nothing. [[slnc '
            '500]] A private field became a public promise, without '
            'anyone deciding it.'
        ),
    ),
    dict(
        key='05-pattern', kind='bullets', title='The Pattern',
        body=['A separate object, built for the boundary.', '', 'A Java record: flat, immutable,', 'exactly the fields the client needs.', '', 'The domain object stays inside.'],
        narration=(
            'Now, the pattern. [[slnc 400]] A separate object, built for '
            'the boundary. [[slnc 300]] In modern Java, it is a record. '
            '[[slnc 300]] Flat, unchangeable, with exactly the fields the '
            'client needs. [[slnc 500]] The real customer object stays '
            'inside. [[slnc 300]] And a small piece of mapping code '
            'copies the fields across.'
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
            'Third demo: the same web service, with a D T O. [[slnc 400]] '
            'The real object came to five thousand two hundred and '
            'ninety-seven characters. [[slnc 300]] The D T O comes to '
            'forty-six. [[slnc 500]] Just an I D, a name, and a city: Ada '
            'Lovelace, London. [[slnc 500]] The password hash cannot '
            'leak, because the record has no field for it. [[slnc 300]] '
            'The order history is never touched. [[slnc 300]] And the '
            'keys are now a promise that someone chose, not an accident '
            'of private field names.'
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
            'A D T O is not a business model, and the project shows one '
            'of each. [[slnc 500]] The customer D T O is a record, with '
            'no behaviour at all. [[slnc 300]] The real customer object '
            'has rules. [[slnc 300]] For example, it refuses an email '
            'address with no at sign. [[slnc 500]] The D T O would carry '
            'a bad email without a word. [[slnc 300]] It is data, not a '
            'model. [[slnc 300]] Mixing the two up is how business logic '
            'ends up scattered everywhere.'
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
            'Now the costs. [[slnc 300]] The first is mapping code, '
            'everywhere. [[slnc 500]] Every D T O needs a method that '
            'copies fields across, by hand. [[slnc 300]] It is tedious. '
            '[[slnc 500]] Here there are four D T Os: plain, summary, '
            'list item, and detail. [[slnc 300]] Together they carry '
            'fifteen fields, copied from a customer that has seven. '
            '[[slnc 500]] And when a new field is added to the customer, '
            'it silently does not reach any D T O nobody remembered to '
            'update.'
        ),
    ),
    dict(
        key='09-multiply', kind='bullets', title='Cost Two: DTOs Multiply',
        body=['CustomerDto, CustomerSummaryDto,', 'CustomerListItemDto, CustomerDetailDto.', '', 'Near-duplicates that drift,', 'until the mapping layer is larger', 'than the domain it protects.'],
        narration=(
            'The second cost: D T Os multiply. [[slnc 400]] First a '
            'customer D T O. [[slnc 300]] Then a summary one. [[slnc '
            '300]] Then a list item one. [[slnc 300]] Then a detail one. '
            '[[slnc 500]] Near-duplicates, each slightly different. '
            '[[slnc 300]] They drift apart over time. [[slnc 300]] And in '
            'a large system, the mapping code can grow bigger than the '
            'business code it was meant to protect.'
        ),
    ),
    dict(
        key='10-loads', kind='bullets', title='Cost Three: The Mapping Decides What Loads',
        body=['The detail DTO asks for the order count.', 'That touches the lazy history,', 'and loads it.', '', 'A DTO can hide the cost,', 'but only if the mapping does.'],
        narration=(
            'The third cost: the mapping decides what gets loaded. [[slnc '
            "400]] The detail D T O includes the customer's number of "
            'orders. [[slnc 300]] To count them, the mapper asks the '
            'customer for its orders. [[slnc 300]] And that loads the '
            'whole order history from the database. [[slnc 500]] A D T O '
            'can hide a cost from the client. [[slnc 300]] But only if '
            'the mapping code stays careful.'
        ),
    ),
    dict(
        key='11-bff', kind='bullets', title='Where This Sits',
        body=['This is Backends for Frontends,', 'at the level of one object,', 'not one deployment.', '', 'Same idea: shape what leaves', 'for who receives it.'],
        narration=(
            'This connects to another pattern in the series: Backends for '
            'Frontends. [[slnc 400]] That pattern shapes a whole service '
            'for each kind of client. [[slnc 300]] A D T O does the same '
            'thing, for a single object. [[slnc 500]] The idea is the '
            'same. [[slnc 300]] Shape what leaves, for whoever receives '
            'it.'
        ),
    ),
    dict(
        key='12-met', kind='bullets', title='Where You Have Met This',
        body=['A Java record returned from a Spring', 'controller is a DTO.', 'Jackson writes its JSON.', '', 'MapStruct writes the mapping code,', 'and is worth taking once you have', 'felt the tedium by hand.'],
        narration=(
            'You have met this pattern before. [[slnc 400]] A Java record '
            'returned from a Spring controller is a D T O. [[slnc 300]] '
            'And the Jackson library turns it into JSON. [[slnc 500]] A '
            'library called MapStruct can write the mapping code for you. '
            '[[slnc 300]] It is worth using, but only after you have felt '
            'the tedium by hand. [[slnc 300]] So you know exactly what it '
            'saves you.'
        ),
    ),
    dict(
        key='13-real', kind='bullets', title='What Is Real Here',
        body=['The serialiser here is small, and', 'not Jackson.', '', 'But it does the same thing: it walks', 'every field. That is why the leak', 'is real.'],
        narration=(
            'A quick, honest note about this demo. [[slnc 400]] The '
            'serialiser here is small, and it is not Jackson. [[slnc '
            '500]] But it does what every serialiser does. [[slnc 300]] '
            'It walks every field it can reach. [[slnc 300]] That is why '
            'the leak, and the rename problem, are real.'
        ),
    ),
    dict(
        key='14-too-much', kind='bullets', title='When This Is Too Much',
        body=['An internal call between two classes', 'in one module: a needless copy.', '', 'It earns its place at a boundary you', 'do not control: an API, a message,', 'a file.'],
        narration=(
            'So, when is this too much? [[slnc 400]] For a call between '
            'two classes inside one module, a D T O is a needless copy. '
            '[[slnc 500]] It earns its place at a boundary you do not '
            'control. [[slnc 300]] A public web interface, a message, or '
            'a file.'
        ),
    ),
    dict(
        key='15-outro', kind='outro', title='Thanks for Watching',
        body=['Full source, notes, diagrams and an animated walkthrough', 'are in the repository. Add a phone field to the customer,', 'and see which classes change.'],
        narration=(
            "That's the D T O pattern. [[slnc 400]] If you remember one "
            'sentence, make it this one. [[slnc 300]] A D T O is a '
            'promise to the outside world, and the mapping code is what '
            'you pay for it. [[slnc 500]] The full source code, written '
            'notes, diagrams, and an animated walkthrough are all in the '
            'repository. [[slnc 500]] Here is one exercise to try. [[slnc '
            '300]] Add a phone number to the customer. [[slnc 300]] Then '
            'see which classes must change to show it, and which to hide '
            'it. [[slnc 500]] If this helped, a like really does help '
            "other people find it. [[slnc 300]] And subscribe, if you'd "
            'like the rest of the series. [[slnc 400]] Thanks for '
            'watching.'
        ),
    ),
]
