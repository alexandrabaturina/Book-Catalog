from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, User, Book, Author

engine = create_engine('sqlite:///books.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


#Create dummy user
dummy_user = User(
    name="John Johnson",
    email="JohnJohnson@gmail.com",
    picture='https://f1.pngfuel.com/png/110/885/214/green-circle-child-avatar-user-profile-smile-boy-cartoon-face-png-clip-art.png')

session.add(dummy_user)
session.commit()


# Books by John Grisham
john_grisham = Author(
    user_id=1,
    name="John Grisham")

session.add(john_grisham)
session.commit()

camino_island = Book(
    title="Camino Island",
    description="Bruce Cable owns a popular bookstore in the sleepy resort town of Santa Rosa on Camino Island in Florida. He makes his real money, though, as a prominent dealer in rare books. Very few people know that he occasionally dabbles in the black market of stolen books and manuscripts. Mercer Mann is a young novelist with a severe case of writer's block who has recently been laid off from her teaching position. She is approached by an elegant, mysterious woman working for an even more mysterious company. A generous offer of money convinces Mercer to go undercover and infiltrate Bruce Cable's circle of literary friends, ideally getting close enough to him to learn his secrets. But eventually Mercer learns far too much.",
    author=john_grisham)

session.add(camino_island)
session.commit()


the_whistler = Book(
    title="The Whistler",
    description="Lacy Stoltz, an investigator for the Florida Board on Judicial Conduct, takes on a case involving a corrupt judge, a Native American casino, and the mafia when a previously disbarred lawyer approaches her on behalf of a client who claims to know the truth.",
    author=john_grisham)

session.add(the_whistler)
session.commit()


theodore_boone = Book(
    title="Theodore Boone",
    description="With two attorneys for parents, thirteen-year-old Theodore Boone knows more about the law than most lawyers do. But when a high profile murder trial comes to his small town and Theo gets pulled into it, it's up to this amateur attorney to save the day.",
    author=john_grisham)

session.add(theodore_boone)
session.commit()


skipping_christmas = Book(
    title="Skipping Christmas",
    description="Imagine a year without Christmas. No crowded malls, no corny office parties, no fruitcakes, no unwanted presents. That's just what Luther and Nora Krank have in mind when they decide that, just this once, they'll skip the holiday together.",
    author=john_grisham)

session.add(skipping_christmas)
session.commit()


# Books by Dale Carnegie
dale_carnegie = Author(
    user_id=1,
    name="Dale Carnegie")

session.add(dale_carnegie)
session.commit()


how_to_win_friends= Book(
    title="How to Win Friends and Influence People",
    description="Carnegie's classic bestseller - an inspirational personal development guide that shows how to achieve lifelong success.",
    author=dale_carnegie)

session.add(how_to_win_friends)
session.commit()


how_to_enjoy_your_life = Book(
    title="How to Enjoy your Life and your Job",
    description="Collecting the most inspirational passages from his landmark mega-bestsellers How to win friends and influence people and How to stop worrying and start living, Dale Carnegie's How to enjoy your life and your job will help you create a new approach to life and get the most out of yourself.",
    author=dale_carnegie)

session.add(how_to_enjoy_your_life)
session.commit()


how_to_stop_worrying = Book(
    title="How to Stop Worrying and Start Living",
    description="In this classic work, How to Stop Worrying and Start Living, Carnegie offers a set of practical formulas that you can put to work today. It is a book packed with lessons that will last a lifetime and make that lifetime happier!",
    author=dale_carnegie)

session.add(how_to_stop_worrying)
session.commit()


# Books by Jamie Oliver
jamie_oliver = Author(
    user_id=1,
    name="Jamie Oliver")

session.add(jamie_oliver)
session.commit()


ultimate_veg = Book(
    title="Ultimate Veg",
    description="Plant-based and veg-forward dishes and meals to encourage eating more plants; based in nutritional, economical, and environmental considerations.",
    author=jamie_oliver)

session.add(ultimate_veg)
session.commit()


everyday_super_food = Book(
    title="Everyday Super Food",
    description="The chef describes his personal journey of weight loss and improved eating habits and offers a collection of recipes for those looking to become healthier, including such offerings as figgy banana bread and crumbed pesto fish.",
    author=jamie_oliver)

session.add(everyday_super_food)
session.commit()


print("Added books from database.")
