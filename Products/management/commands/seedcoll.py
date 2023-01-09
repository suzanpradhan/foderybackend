from django.core.management.base import BaseCommand
import random

from Products.models import Collection, Item

# python manage.py seed --mode=refresh

""" Clear all data and creates collectiones """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    print("Delete collection instances")
    Collection.objects.all().delete()


def create_collection(name):
    """Creates an collection object combining different elements from the list"""
    print("Creating collection")
    description = ["Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque pellentesque faucibus turpis, sit amet egestas odio mollis et. Praesent sollicitudin velit non ante pellentesque, at convallis ante finibus",
                 " Nunc viverra sollicitudin risus, quis vehicula neque placerat quis. Praesent maximus sodales tincidunt. Aliquam eget pulvinar ex, eu finibus erat. Quisque tincidunt nulla mauris, in varius nisi euismod eleifend. Vestibulum interdum, eros eget eleifend laoreet, lorem tellus sodales urna, nec tempor odio lorem quis tellus."
                 , "Quisque interdum pellentesque tellus quis lobortis. In at aliquam nibh. Donec placerat quam sed viverra consectetur. Nullam non vulputate est. Cras non orci varius, pharetra lorem id, fermentum diam. Mauris tristique imperdiet tempor.", 
                 ]
    isFeatured = [True,False]
    status = [True,False]

    for _ in name:
        collection = Collection(
            title=_,
            description=random.choice(description),
            isFeatured=random.choice(isFeatured),
            status=random.choice(status),
            
        )
        collection.save()
        print("{} collection created.".format(collection))
    return collection

def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    # Clear data from tables
    clear_data()
    if mode == MODE_CLEAR:
        return

    create_collection(['Best Seller','Featured','Popular'])