from collections import OrderedDict

import factory

from purchases.models import BeerPurchase
from rooms.models import Room

DEFAULT_USER_FACTORY_PASSWORD = 'test'


class RelatedFactoryListDynamicSize(factory.RelatedFactoryList):
    # https://github.com/FactoryBoy/factory_boy/issues/767

    def evaluate(self, instance, step, extra):
        return super().evaluate(instance, step, extra)

    def call(self, instance, step, context):
        size = context.extra.pop('size', self.size)
        assert isinstance(size, int), 'Size passed to RelatedFactoryList must be an integer'
        return [
            super(factory.RelatedFactoryList, self).call(instance, step, context)
            for _ in range(size)
        ]


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'users.User'

    username = factory.Faker('user_name')
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall(
        'set_password',
        DEFAULT_USER_FACTORY_PASSWORD
    )


class BreweryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'beers.Brewery'

    name = factory.Faker('company')
    city = factory.Faker('city')
    country = factory.Faker('country_code')
    year_established = factory.Faker('year')
    website = factory.Faker('url')
    image = None
    description = factory.Faker('text')


class BeerStyleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'beers.BeerStyle'

    name = factory.Faker('word')
    known_as = factory.LazyAttribute(lambda o: o.name)
    country = factory.Faker('country_code')
    description = factory.Faker('text')
    serving_temperature_range = None
    abv_range = None
    color_range = None
    bitterness_range = None
    original_gravity_range = None
    final_gravity_range = None


class HopFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'beers.Hop'

    name = factory.Faker('word')
    description = factory.Faker('text')
    country = factory.Faker('country_code')


class BeerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'beers.Beer'

    name = factory.Faker('name')
    brewery = factory.SubFactory(BreweryFactory)
    style = factory.SubFactory(BeerStyleFactory)
    percentage = factory.Faker('random_int', min=1, max=12)
    volume_ml = 500
    hop_rate = None
    extract = None
    IBU = None
    image = None
    description = factory.Faker('text')

    with_hops = False

    class Params:
        with_hops = factory.Trait(
            hops=RelatedFactoryListDynamicSize(
                HopFactory,
                size=2
            )
        )


class BeerPurchaseFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'purchases.BeerPurchase'

    beer = factory.SubFactory(BeerFactory)
    sold_to = factory.SubFactory(UserFactory)
    packaging = factory.Faker(
        'random_element',
        elements=OrderedDict(
            [
                (BeerPurchase.Packaging.BOTTLE, 0.4),
                (BeerPurchase.Packaging.CAN, 0.3),
                (BeerPurchase.Packaging.DRAUGHT, 0.2),
                (BeerPurchase.Packaging.KEG, 0.1),
            ]
        ),
    )
    price = factory.Faker(
        'pydecimal',
        left_digits=2,
        right_digits=2,
        positive=True,
        min_value=2.0,
        max_value=30.0
    )
    volume_ml = 500
    image = None
    purchased_at = factory.Faker('date_this_year', after_today=False)


class RoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'rooms.Room'

    name = factory.LazyAttributeSequence(lambda o, n: f'room_{n}')
    password = None
    host = factory.SubFactory(UserFactory)
    slots = factory.Faker('random_int', min=1, max=10)
    state = factory.Faker('random_element', elements=Room.State.values)


class UserInRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'rooms.UserInRoom'


class BeerInRoomFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'rooms.BeerInRoom'


class RatingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'ratings.Rating'

    added_by = factory.SubFactory(UserFactory)
    beer = factory.SubFactory(BeerFactory)
    # todo: maybe make beer_purchase and room fks random
    beer_purchase = factory.SubFactory(
        BeerPurchaseFactory,
        beer=factory.SelfAttribute('..beer')
    )
    room = None
    color = factory.Faker('text')
    foam = factory.Faker('text')
    smell = factory.Faker('text')
    taste = factory.Faker('text')
    opinion = factory.Faker('text')
    note = factory.Faker('random_int', min=1, max=10)
