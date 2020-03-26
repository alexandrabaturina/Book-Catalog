from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Category, Base, CatalogItem

engine = create_engine('sqlite:///catalogitems.db')
Base.metadata.bind = engine

#Books of John Grisham (= Category1)
category1 = Category(name = "John Grisham")

session.add(category1)
session.commit()


catalogItem1 = CatalogItem(
    name = "Camino Island",
    description = '''Bruce Cable owns a popular bookstore in the sleepy resort
    town of Santa Rosa on Camino Island in Florida. He makes his real money,
    though, as a prominent dealer in rare books. Very few people know that he
    occasionally dabbles in the black market of stolen books and manuscripts.
    Mercer Mann is a young novelist with a severe case of writer's block who
    has recently been laid off from her teaching position. She is approached by
    an elegant, mysterious woman working for an even more mysterious company.
    A generous offer of money convinces Mercer to go undercover and infiltrate
    Bruce Cable's circle of literary friends, ideally getting close enough to
    him to learn his secrets. But eventually Mercer learns far too much.''',
    category = category1)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(
    name = "The Whistler",
    description = '''Lacy Stoltz, an investigator for the Florida Board on
    Judicial Conduct, takes on a case involving a corrupt judge, a Native
    American casino, and the mafia when a previously disbarred lawyer
    approaches her on behalf of a client who claims to know the truth ''',
    category = category1)

session.add(catalogItem2)
session.commit()


catalogItem3 = CatalogItem(
    name = "Theodore Boone",
    description = '''With two attorneys for parents, thirteen-year-old Theodore
    Boone knows more about the law than most lawyers do. But when a high
    profile murder trial comes to his small town and Theo gets pulled into it,
    it's up to this amateur attorney to save the day. ''',
    category = category1)

session.add(catalogItem3)
session.commit()


catalogItem4 = CatalogItem(
    name = "Skipping Christmas",
    description = '''Imagine a year without Christmas. No crowded malls, no
    corny office parties, no fruitcakes, no unwanted presents. That's just what
    Luther and Nora Krank have in mind when they decide that, just this once,
    they'll skip the holiday together.''',
    category = category1)

session.add(catalogItem4)
session.commit()

#Books of Dale Carnegie (= Category 2)
category2 = Category(name = "Dale Carnegie")

session.add(category2)
session.commit()


catalogItem1 = CatalogItem(
    name = "How to Win Friends and Influence People",
    description = '''Carnegie's classic bestseller - an inspirational personal
    -development guide that shows how to achieve lifelong success.''',
    category = category2)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(name = "How to Enjoy your Life and your Job",
    description = '''Collecting the most inspirational passages from his
    landmark mega-bestsellers How to win friends and influence people and How
    to stop worrying and start living, Dale Carnegie's How to enjoy your life
    and your job will help you create a new approach to life and get the most
    out of yourself.''',
    category = category2)

session.add(catalogItem2)
session.commit()


catalogItem3 = CatalogItem(name = "How to Stop Worrying and Start Living",
    description = '''In this classic work, How to Stop Worrying and Start
    Living, Carnegie offers a set of practical formulas that you can put to
    work today. It is a book packed with lessons that will last a lifetime and
    make that lifetime happier!''',
    category = category2)

session.add(catalogItem3)
session.commit()

#Books of Jamie Oliver (= Category 3)
category3 = Category(name = "Jamie Oliver")

session.add(category3)
session.commit()


catalogItem1 = CatalogItem(
    name = "Ultimate Veg",
    description = '''Plant-based and veg-forward dishes and meals to encourage
    eating more plants; based in nutritional, economical, and environmental
    considerations.''',
    category = category3)

session.add(catalogItem1)
session.commit()


catalogItem2 = CatalogItem(
    name = "Everyday Super Food",
    description = '''The chef describes his personal journey of weight loss and
    improved eating habits and offers a collection of recipes for those looking
    to become healthier, including such offerings as figgy banana bread and
    crumbed pesto fish.''',
    category = category3)

session.add(catalogItem2)
session.commit()

DBSession = sessionmaker(bind=engine)
session = DBSession()
