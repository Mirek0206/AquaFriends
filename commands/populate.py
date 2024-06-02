from django.core.management.base import BaseCommand, CommandParser
from abc import ABC, abstractmethod
from faker import Faker
from faker.providers import BaseProvider
from typing import Iterable
import random
from django.contrib.auth.models import User
from AquaLife.models import Species, Fish
from AquaMaker.models import *

class Command(BaseCommand):
    """
    A Django management command class that populates the database with users.

    :param BaseCommand: Inherits from Django's BaseCommand class.
    :type BaseCommand: class
    """
    help = 'Populates the database with the users'

    def add_arguments(self, parser: CommandParser) -> None:
        """
        Adds custom command arguments.

        :param parser: The command line parser.
        :type parser: CommandParser
        """
        parser.add_argument('amount', type=int, help='The number of users to be created')
        return super().add_arguments(parser)

    def handle(self, *args, **kwargs):
        """
        The function that executes the command logic.

        :param args: Command arguments.
        :type args: tuple
        :param kwargs: Command keyword arguments.
        :type kwargs: dict
        """

        user_generator = ProfileGenerator()
        existing_emails = set(User.objects.values_list('email', flat=True))
        creations: int = 0

        requested = int(kwargs['amount'])
        if requested < 1:
            raise ValueError("Amount must be greater than 0.")
        
        # create fish species
        fish_species = [
            "Akara błękitna",
            "Babka tęczowa",
            "Czerwieniak kongijski - Moanda",
            "Danio tęczowy",
            "Fantom czarny",
            "Garra panda",
            "Kirysek czarny",
            "Kosiarka - Grubowarg syjamski",
            "Molinezja ostrousta",
            "Naskalnik Dickfelda",
            "Neon czerwony",
            "Paletka - Dyskowiec"
        ]

        for single_species in fish_species:
            fish_species_model = Species(name=single_species)
            fish_species_model.save()

        # create filters
        aquarium_filters = [
            "Filtr wewnętrzny do akwarium 10-40l",
            "Filtr wewnętrzny do akwarium 50-80l",
            "Filtr wewnętrzny do akwarium 100-160l"
        ]

        for single_filter in aquarium_filters:
            filter_model = Filter(type=single_filter)
            filter_model.save()

        # create heaters
        aquarium_heaters = [
            "75W",
            "100W",
            "150W",
            "200W",
            "25W"
            "50W"
            "300W"
        ]

        for single_heater in aquarium_heaters:
            heater_model = Heater(power=single_heater)
            heater_model.save()

        # create pumps
        aquarium_pumps = [
            "12W",
            "20W",
            "25W",
            "30W",
            "40W"
        ]

        for single_pump in aquarium_pumps:
            pump_model = Pump(power=single_pump)
            pump_model.save()

        while creations < requested:
            for data in user_generator.generate(requested - creations):
                if data['email'] in existing_emails:
                    print(f'User with email {data["email"]} already exists. Skipping')
                    continue
                else:
                    existing_emails.add(data['email'])

                # create user
                user = User.objects.create_user(
                    first_name=data['name'],
                    email=data['email'],
                    username=data['email'].split('@')[0],
                    password='default'
                )

                # create profile for given user
                profile = user.profile
                profile.city = 'Warsaw'
                profile.age = data['age']
                profile.bio = data['bio']
                profile.gender = data['gender']
                profile.save()
                
                first_aquarium = Aquarium.objects.create(
                    user=user,
                    name=(profile.user.first_name + "'s 1st aquarium"),
                    x=random.randrange(10, 50),
                    y=random.randrange(10, 50),
                    z=random.randrange(10, 50),
                    light=random.choice(Light.objects),
                    pump=random.choice(Pump.objects),
                    heater=random.choice(Heater.objects),
                    filters=random.choice(Filter.objects)
                )

                second_aquarium = Aquarium.objects.create(
                    user=user,
                    name=(profile.user.first_name + "'s 2nd aquarium"),
                    x=random.randrange(10, 50),
                    y=random.randrange(10, 50),
                    z=random.randrange(10, 50),
                    light=random.choice(Light.objects),
                    pump=random.choice(Pump.objects),
                    heater=random.choice(Heater.objects),
                    filters=random.choice(Filter.objects)
                )

                third_aquarium = Aquarium.objects.create(
                    user=user,
                    name=(profile.user.first_name + "'s 3rd aquarium"),
                    x=random.randrange(10, 50),
                    y=random.randrange(10, 50),
                    z=random.randrange(10, 50),
                    light=random.choice(Light.objects),
                    pump=random.choice(Pump.objects),
                    heater=random.choice(Heater.objects),
                    filters=random.choice(Filter.objects)
                )

                # add fish to the 1st aquarium
                for _ in range(random.randint(1, 4)):
                    Fish.objects.create(
                        name=Faker.first_name,
                        age=random.randint(0, 20),
                        species=random.choice(Species.objects),
                        aquarium=first_aquarium
                    )

                # add fish to the 2nd aquarium
                for _ in range(random.randint(1, 4)):
                    Fish.objects.create(
                        name=Faker.first_name,
                        age=random.randint(0, 20),
                        species=random.choice(Species.objects),
                        aquarium=second_aquarium
                    )

                # add fish to the 3rd aquarium
                for _ in range(random.randint(1, 4)):
                    Fish.objects.create(
                        name=Faker.first_name,
                        age=random.randint(0, 20),
                        species=random.choice(Species.objects),
                        aquarium=third_aquarium
                    )

                # save all aquariums
                first_aquarium.save()
                second_aquarium.save()
                third_aquarium.save()

                creations += 1
                print(f'Created User with email {data["email"]}.')

        print(f'Created {creations} mock users.')

class Generator(ABC):
    """
    An abstract class for generating mock users.

    :param ABC: Inherits from Python's ABC (Abstract Base Class) class.
    :type ABC: class
    """

    @abstractmethod
    def generate(self, *args, **kwargs):
        """
        Abstract method for generating mock users.

        :param args: Command arguments.
        :type args: tuple
        :param kwargs: Command keyword arguments.
        :type kwargs: dict
        """
        raise NotImplementedError


class ProfileGenerator(Generator, BaseProvider):
    """
    A class for generating mock profiles.

    :param Generator: Inherits from the Generator abstract base class.
    :type Generator: class
    :param BaseProvider: Inherits from Faker's BaseProvider class.
    :type BaseProvider: class
    """

    def __init__(self):
        """
        Constructor for UserGenerator class.
        """
        self.__faker = Faker()
        Faker.seed(2137)
        random.seed(2137)

    def generate(self, amount: int = 1) -> Iterable[dict]:
        """
        Method for generating mock users.

        :param amount: The number of mock users to generate.
        :type amount: int
        :return: A generator yielding user data.
        :rtype: Iterable[dict]
        """
        if amount < 1:
            raise ValueError("Amount must be greater than 0.")

        for _ in range(amount):
            data = dict()
            data["gender"] = random.choice(["M", "K"])
            data["name"] = self.generate_name(data["gender"])
            data["email"] = self.generate_email(data["name"])
            data["pwd"] = self.generate_password()
            data["age"] = random.randint(18, 69)
            data["bio"] = self.generate_bio()

            yield data

    def generate_name(self, gender: str) -> str:
        """
        Generates a random name based on the provided gender.

        :param gender: The gender of the name ("M" for male, "K" for female).
        :type gender: str
        :return: A random name.
        :rtype: str
        """

        if gender == "M":
            return f'{self.__faker.first_name_male()} {self.__faker.last_name_male()}'.lower()
        else:
            return f'{self.__faker.first_name_female()} {self.__faker.last_name_female()}'.lower()

    def generate_password(self) -> str:
        """
        Generates a random password.

        :return: A random password.
        :rtype: str
        """
        # return self.__faker.password(length=25, special_chars=True, digits=True, upper_case=True, lower_case=True)
        return "haslo123"
    
    def generate_bio(self) -> str:
        """
        Generates a random bio.

        :return: A random bio.
        :rtype: str
        """
        return self.__faker.text(max_nb_chars=150)
    
    def generate_email(self, name: str) -> str:
        """
        Generates a random email address from a given name.

        :param name: The name of the user.
        :type name: str
        :return: A random email address.
        :rtype: str
        """
        return f'{name.replace(" ", ".")}{random.randint(0, 2137)}@{self.__faker.free_email_domain()}'.lower()