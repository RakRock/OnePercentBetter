"""
Movie Buff — kid-appropriate movie trivia quiz for Arjun.

Covers popular animated, family-friendly, and adventure movies.
Difficulty: Easy (designed to build interest, will scale to medium/hard later).
"""

import random

CATEGORIES = {
    "animated": {
        "name": "Animated Classics",
        "emoji": "🎬",
        "color": "#f59e0b",
        "description": "Disney, Pixar & animated favourites",
    },
    "adventure": {
        "name": "Adventure & Sci-Fi",
        "emoji": "🚀",
        "color": "#3b82f6",
        "description": "Epic adventures and sci-fi worlds",
    },
    "superhero": {
        "name": "Superheroes",
        "emoji": "🦸",
        "color": "#ef4444",
        "description": "Marvel, DC & superhero movies",
    },
    "comedy_family": {
        "name": "Comedy & Family",
        "emoji": "😂",
        "color": "#10b981",
        "description": "Funny and heartwarming family films",
    },
    "fantasy": {
        "name": "Fantasy & Magic",
        "emoji": "🧙",
        "color": "#8b5cf6",
        "description": "Wizards, dragons & magical worlds",
    },
}

QUESTION_BANK = [
    # ========== ANIMATED CLASSICS ==========
    {
        "id": 1, "category": "animated",
        "question": "In 'Finding Nemo', what type of fish is Nemo?",
        "options": ["Goldfish", "Clownfish", "Angelfish", "Betta fish"],
        "answer": 1,
        "explanation": "Nemo is a clownfish (also called an anemonefish) who lives in the Great Barrier Reef!",
    },
    {
        "id": 2, "category": "animated",
        "question": "What is the name of the snowman in 'Frozen'?",
        "options": ["Marshmallow", "Olaf", "Sven", "Kristoff"],
        "answer": 1,
        "explanation": "Olaf is the friendly snowman created by Elsa's magic who loves warm hugs!",
    },
    {
        "id": 3, "category": "animated",
        "question": "In 'Toy Story', what is the name of the cowboy doll?",
        "options": ["Buzz", "Rex", "Woody", "Hamm"],
        "answer": 2,
        "explanation": "Woody is Andy's favourite toy — a pull-string cowboy who leads all the toys!",
    },
    {
        "id": 4, "category": "animated",
        "question": "What does the old man's house fly with in 'Up'?",
        "options": ["Rockets", "Balloons", "A giant fan", "Propellers"],
        "answer": 1,
        "explanation": "Carl Fredricksen tied thousands of colourful balloons to his house to fly to South America!",
    },
    {
        "id": 5, "category": "animated",
        "question": "In 'The Lion King', who is Simba's father?",
        "options": ["Scar", "Timon", "Mufasa", "Rafiki"],
        "answer": 2,
        "explanation": "Mufasa is the wise and powerful king of Pride Rock and Simba's dad.",
    },
    {
        "id": 6, "category": "animated",
        "question": "Which Pixar movie features a rat who dreams of being a chef?",
        "options": ["Cars", "Ratatouille", "Coco", "Wall-E"],
        "answer": 1,
        "explanation": "In Ratatouille, a rat named Remy becomes a chef in a fancy Paris restaurant!",
    },
    {
        "id": 7, "category": "animated",
        "question": "In 'Moana', what does Moana need to return to Te Fiti?",
        "options": ["A magic ring", "The heart of Te Fiti", "A golden shell", "A pearl necklace"],
        "answer": 1,
        "explanation": "Moana must return the heart (a small greenstone) to the goddess Te Fiti to save her island.",
    },
    {
        "id": 8, "category": "animated",
        "question": "What is the name of the blue fish with memory problems in 'Finding Dory'?",
        "options": ["Nemo", "Gill", "Dory", "Marlin"],
        "answer": 2,
        "explanation": "Dory is a blue tang fish who suffers from short-term memory loss but has a big heart!",
    },
    {
        "id": 9, "category": "animated",
        "question": "In 'Inside Out', which emotion is yellow and always cheerful?",
        "options": ["Sadness", "Anger", "Joy", "Disgust"],
        "answer": 2,
        "explanation": "Joy is the bright yellow emotion who tries to keep Riley happy all the time.",
    },
    {
        "id": 10, "category": "animated",
        "question": "Which Disney movie features a princess with very long magical hair?",
        "options": ["Brave", "Tangled", "Cinderella", "Moana"],
        "answer": 1,
        "explanation": "In Tangled, Rapunzel has about 70 feet of magical golden hair!",
    },
    {
        "id": 11, "category": "animated",
        "question": "In 'Coco', what is the name of the Land where the dead live?",
        "options": ["The Underworld", "The Land of the Dead", "Ghost Town", "Spirit Valley"],
        "answer": 1,
        "explanation": "Miguel accidentally enters the Land of the Dead during Día de los Muertos!",
    },
    {
        "id": 12, "category": "animated",
        "question": "What does WALL-E collect on Earth?",
        "options": ["Rocks", "Trash and interesting objects", "Animals", "Plants"],
        "answer": 1,
        "explanation": "WALL-E is a robot who compacts trash on an abandoned Earth and collects interesting trinkets.",
    },
    {
        "id": 13, "category": "animated",
        "question": "In 'Monsters, Inc.', what powers the monster world?",
        "options": ["Electricity", "Children's screams", "Sunlight", "Wind"],
        "answer": 1,
        "explanation": "Monsters scare children to collect screams that power their city — later they switch to laughter!",
    },
    {
        "id": 14, "category": "animated",
        "question": "Who is the villain in 'The Incredibles'?",
        "options": ["Frozone", "Syndrome", "Edna Mode", "Dash"],
        "answer": 1,
        "explanation": "Syndrome (Buddy Pine) was once a fan of Mr. Incredible who turned into a villain!",
    },
    {
        "id": 15, "category": "animated",
        "question": "In 'Kung Fu Panda', what animal is Po?",
        "options": ["Tiger", "Crane", "Panda", "Snake"],
        "answer": 2,
        "explanation": "Po is a giant panda who becomes the Dragon Warrior and masters kung fu!",
    },
    {
        "id": 16, "category": "animated",
        "question": "Which movie features a young girl named Riley whose emotions come to life?",
        "options": ["Encanto", "Soul", "Inside Out", "Elemental"],
        "answer": 2,
        "explanation": "Inside Out takes us inside Riley's mind where Joy, Sadness, Anger, Fear and Disgust guide her.",
    },
    {
        "id": 17, "category": "animated",
        "question": "In 'Shrek', what kind of creature is Shrek?",
        "options": ["Troll", "Giant", "Ogre", "Goblin"],
        "answer": 2,
        "explanation": "Shrek is a green ogre who lives in a swamp and just wants to be left alone!",
    },
    {
        "id": 18, "category": "animated",
        "question": "What is the name of the little robot in 'Big Hero 6'?",
        "options": ["Baymax", "Wasabi", "GoGo", "Hiro"],
        "answer": 0,
        "explanation": "Baymax is a puffy white healthcare robot who becomes a superhero with Hiro!",
    },
    {
        "id": 19, "category": "animated",
        "question": "In 'Zootopia', what does Judy Hopps want to become?",
        "options": ["A teacher", "A police officer", "A doctor", "A pilot"],
        "answer": 1,
        "explanation": "Judy Hopps is the first bunny to become a police officer in the city of Zootopia!",
    },
    {
        "id": 20, "category": "animated",
        "question": "Which Pixar film is set in the Mexican holiday Día de los Muertos?",
        "options": ["Luca", "Coco", "Encanto", "Turning Red"],
        "answer": 1,
        "explanation": "Coco is about 12-year-old Miguel who visits the Land of the Dead on Day of the Dead.",
    },
    {
        "id": 21, "category": "animated",
        "question": "In 'The Incredibles', what is the superpower of Violet?",
        "options": ["Super speed", "Invisibility and force fields", "Super strength", "Fire control"],
        "answer": 1,
        "explanation": "Violet can turn invisible and create protective force-field bubbles!",
    },
    {
        "id": 22, "category": "animated",
        "question": "In 'Luca', where does the story take place?",
        "options": ["France", "Spain", "Italy", "Greece"],
        "answer": 2,
        "explanation": "Luca is set in a beautiful seaside town on the Italian Riviera!",
    },
    {
        "id": 23, "category": "animated",
        "question": "What is the name of the family in 'Encanto'?",
        "options": ["The Garcias", "The Madrigals", "The Riveras", "The Santos"],
        "answer": 1,
        "explanation": "The Madrigal family lives in a magical house in Colombia, and each member has a special gift!",
    },
    {
        "id": 24, "category": "animated",
        "question": "In 'How to Train Your Dragon', what is the name of Hiccup's dragon?",
        "options": ["Stormfly", "Toothless", "Hookfang", "Meatlug"],
        "answer": 1,
        "explanation": "Toothless is a rare Night Fury dragon who becomes Hiccup's best friend!",
    },
    {
        "id": 25, "category": "animated",
        "question": "Which movie features a superhero family with a baby named Jack-Jack?",
        "options": ["Megamind", "The Incredibles", "Big Hero 6", "Bolt"],
        "answer": 1,
        "explanation": "Jack-Jack is the baby of the Parr family and turns out to have the most powers of all!",
    },

    # ========== ADVENTURE & SCI-FI ==========
    {
        "id": 26, "category": "adventure",
        "question": "In 'Jurassic World', what island do the dinosaurs live on?",
        "options": ["Skull Island", "Isla Nublar", "Treasure Island", "Fantasy Island"],
        "answer": 1,
        "explanation": "Isla Nublar is the fictional island off Costa Rica where the dinosaur theme park is built.",
    },
    {
        "id": 27, "category": "adventure",
        "question": "In 'Star Wars', what colour is Luke Skywalker's first lightsaber?",
        "options": ["Red", "Green", "Blue", "Purple"],
        "answer": 2,
        "explanation": "Luke's first lightsaber (his father's) glows blue!",
    },
    {
        "id": 28, "category": "adventure",
        "question": "What is the name of the ship in 'Pirates of the Caribbean'?",
        "options": ["The Jolly Roger", "The Black Pearl", "The Flying Dutchman", "The Titanic"],
        "answer": 1,
        "explanation": "Captain Jack Sparrow's beloved ship is the Black Pearl!",
    },
    {
        "id": 29, "category": "adventure",
        "question": "In 'E.T.', what does the alien want to do?",
        "options": ["Take over Earth", "Phone home", "Eat candy", "Go to school"],
        "answer": 1,
        "explanation": "E.T. just wants to contact his spaceship and go home — 'E.T. phone home!'",
    },
    {
        "id": 30, "category": "adventure",
        "question": "What is the name of Indiana Jones' weapon of choice?",
        "options": ["A sword", "A whip", "A bow", "A staff"],
        "answer": 1,
        "explanation": "Indiana Jones is famous for his brown fedora hat and his trusty whip!",
    },
    {
        "id": 31, "category": "adventure",
        "question": "In 'Jumanji', what happens when you play the board game?",
        "options": ["You win money", "The game comes to life", "Nothing", "You travel in time"],
        "answer": 1,
        "explanation": "In Jumanji, the jungle adventures from the board game become real!",
    },
    {
        "id": 32, "category": "adventure",
        "question": "Which planet is Luke Skywalker from in 'Star Wars'?",
        "options": ["Hoth", "Naboo", "Tatooine", "Endor"],
        "answer": 2,
        "explanation": "Luke grew up on the desert planet Tatooine with his uncle and aunt.",
    },
    {
        "id": 33, "category": "adventure",
        "question": "In 'Back to the Future', what type of car is the time machine?",
        "options": ["Ferrari", "DeLorean", "Mustang", "Corvette"],
        "answer": 1,
        "explanation": "Doc Brown converts a DeLorean into a time machine that needs to hit 88 mph!",
    },
    {
        "id": 34, "category": "adventure",
        "question": "What do the Na'vi people ride in 'Avatar'?",
        "options": ["Cars", "Horses", "Flying creatures called Banshees", "Motorcycles"],
        "answer": 2,
        "explanation": "The Na'vi bond with and ride Mountain Banshees (Ikran) to fly on Pandora.",
    },
    {
        "id": 35, "category": "adventure",
        "question": "In 'The Maze Runner', what are the kids trapped inside?",
        "options": ["A castle", "A giant maze", "A spaceship", "An island"],
        "answer": 1,
        "explanation": "The Gladers are trapped in a giant, shifting maze and must find a way out!",
    },
    {
        "id": 36, "category": "adventure",
        "question": "What is Baby Yoda's real name in 'The Mandalorian'?",
        "options": ["Yoda Jr.", "Grogu", "Mando", "Din"],
        "answer": 1,
        "explanation": "The adorable little green character is named Grogu!",
    },
    {
        "id": 37, "category": "adventure",
        "question": "In 'Godzilla', what is Godzilla?",
        "options": ["A robot", "A giant dinosaur-like monster", "An alien", "A whale"],
        "answer": 1,
        "explanation": "Godzilla is a massive prehistoric sea monster awakened by nuclear radiation.",
    },
    {
        "id": 38, "category": "adventure",
        "question": "Which planet do humans try to live on in 'The Martian'?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": 2,
        "explanation": "Astronaut Mark Watney gets stranded on Mars and must survive using science!",
    },

    # ========== SUPERHEROES ==========
    {
        "id": 39, "category": "superhero",
        "question": "What is Spider-Man's real name?",
        "options": ["Tony Stark", "Bruce Wayne", "Peter Parker", "Clark Kent"],
        "answer": 2,
        "explanation": "Peter Parker is a regular teenager who gets bitten by a radioactive spider!",
    },
    {
        "id": 40, "category": "superhero",
        "question": "What metal is Captain America's shield made of?",
        "options": ["Iron", "Steel", "Vibranium", "Titanium"],
        "answer": 2,
        "explanation": "Cap's iconic shield is made of Vibranium, the rare metal from Wakanda!",
    },
    {
        "id": 41, "category": "superhero",
        "question": "What is the name of Batman's city?",
        "options": ["Metropolis", "Star City", "Gotham City", "Central City"],
        "answer": 2,
        "explanation": "Batman protects Gotham City from villains like the Joker and the Riddler!",
    },
    {
        "id": 42, "category": "superhero",
        "question": "Which Avenger can shrink to the size of an ant?",
        "options": ["Hawkeye", "Black Widow", "Ant-Man", "Vision"],
        "answer": 2,
        "explanation": "Ant-Man (Scott Lang) uses Pym Particles to shrink down or grow giant!",
    },
    {
        "id": 43, "category": "superhero",
        "question": "What colour does the Hulk turn when he gets angry?",
        "options": ["Blue", "Red", "Green", "Purple"],
        "answer": 2,
        "explanation": "Bruce Banner transforms into the big green Hulk when he gets angry!",
    },
    {
        "id": 44, "category": "superhero",
        "question": "In 'Black Panther', what is the name of T'Challa's country?",
        "options": ["Wakanda", "Asgard", "Sokovia", "Latveria"],
        "answer": 0,
        "explanation": "Wakanda is a hidden, technologically advanced African nation powered by Vibranium!",
    },
    {
        "id": 45, "category": "superhero",
        "question": "What is Iron Man's real name?",
        "options": ["Steve Rogers", "Tony Stark", "Bruce Banner", "Thor Odinson"],
        "answer": 1,
        "explanation": "Tony Stark is a genius inventor and billionaire who builds the Iron Man suit!",
    },
    {
        "id": 46, "category": "superhero",
        "question": "Which superhero is from the planet Krypton?",
        "options": ["Batman", "Wonder Woman", "Superman", "The Flash"],
        "answer": 2,
        "explanation": "Superman (Kal-El) was sent to Earth as a baby when Krypton was destroyed.",
    },
    {
        "id": 47, "category": "superhero",
        "question": "What is Thor's powerful weapon called?",
        "options": ["Excalibur", "Mjolnir", "Sting", "Anduril"],
        "answer": 1,
        "explanation": "Mjolnir is Thor's enchanted hammer — only those who are worthy can lift it!",
    },
    {
        "id": 48, "category": "superhero",
        "question": "In the MCU, who collected all six Infinity Stones?",
        "options": ["Loki", "Ultron", "Thanos", "Red Skull"],
        "answer": 2,
        "explanation": "Thanos collected all six Infinity Stones to snap away half of all life in the universe!",
    },
    {
        "id": 49, "category": "superhero",
        "question": "Which superhero team includes Iron Man, Captain America, and Thor?",
        "options": ["X-Men", "Justice League", "The Avengers", "Fantastic Four"],
        "answer": 2,
        "explanation": "The Avengers are Earth's Mightiest Heroes who assemble to fight big threats!",
    },
    {
        "id": 50, "category": "superhero",
        "question": "What gives Spider-Man his powers?",
        "options": ["A magic ring", "A radioactive spider bite", "A science experiment", "An alien suit"],
        "answer": 1,
        "explanation": "Peter Parker was bitten by a radioactive spider that gave him spider-like abilities!",
    },
    {
        "id": 51, "category": "superhero",
        "question": "What is the name of Wonder Woman's home island?",
        "options": ["Atlantis", "Themyscira", "Asgard", "Krypton"],
        "answer": 1,
        "explanation": "Themyscira is a hidden island of Amazon warriors where Diana (Wonder Woman) grew up.",
    },
    {
        "id": 52, "category": "superhero",
        "question": "Who is Miles Morales in the Spider-Verse movies?",
        "options": ["A villain", "A new Spider-Man", "A scientist", "A reporter"],
        "answer": 1,
        "explanation": "Miles Morales is a teenager from Brooklyn who becomes his universe's Spider-Man!",
    },
    {
        "id": 53, "category": "superhero",
        "question": "What is Doctor Strange's superpower?",
        "options": ["Super strength", "Magic and sorcery", "Super speed", "Mind reading"],
        "answer": 1,
        "explanation": "Doctor Strange is the Sorcerer Supreme who uses mystic arts to protect reality!",
    },

    # ========== COMEDY & FAMILY ==========
    {
        "id": 54, "category": "comedy_family",
        "question": "In 'Home Alone', what does Kevin do when burglars try to rob his house?",
        "options": ["Calls the police immediately", "Sets up booby traps", "Hides in the attic", "Runs away"],
        "answer": 1,
        "explanation": "Kevin McCallister sets up hilarious and painful booby traps all over the house!",
    },
    {
        "id": 55, "category": "comedy_family",
        "question": "In 'The Karate Kid', what does Mr. Miyagi teach Daniel first?",
        "options": ["Punching", "Wax on, wax off", "Running", "Push-ups"],
        "answer": 1,
        "explanation": "Mr. Miyagi secretly teaches karate through chores like waxing cars and painting fences!",
    },
    {
        "id": 56, "category": "comedy_family",
        "question": "In 'Night at the Museum', what happens at night?",
        "options": ["The lights go out", "The museum exhibits come to life", "Ghosts appear", "The building disappears"],
        "answer": 1,
        "explanation": "An ancient Egyptian tablet makes all the museum exhibits come alive at night!",
    },
    {
        "id": 57, "category": "comedy_family",
        "question": "What sport does the team play in 'Space Jam'?",
        "options": ["Football", "Baseball", "Basketball", "Soccer"],
        "answer": 2,
        "explanation": "The Looney Tunes team up with Michael Jordan to play basketball against the Monstars!",
    },
    {
        "id": 58, "category": "comedy_family",
        "question": "In 'Paddington', where does the bear come from?",
        "options": ["Africa", "Australia", "Peru", "India"],
        "answer": 2,
        "explanation": "Paddington Bear comes all the way from Darkest Peru to London!",
    },
    {
        "id": 59, "category": "comedy_family",
        "question": "What is the dog's name in 'Marley & Me'?",
        "options": ["Buddy", "Max", "Marley", "Rex"],
        "answer": 2,
        "explanation": "Marley is a lovable but very mischievous Labrador Retriever!",
    },
    {
        "id": 60, "category": "comedy_family",
        "question": "In 'Stuart Little', what kind of animal is Stuart?",
        "options": ["A hamster", "A rat", "A mouse", "A guinea pig"],
        "answer": 2,
        "explanation": "Stuart Little is a tiny white mouse who is adopted by a human family in New York City!",
    },
    {
        "id": 61, "category": "comedy_family",
        "question": "In 'Despicable Me', what are the small yellow characters called?",
        "options": ["Henchmen", "Minions", "Goblins", "Helpers"],
        "answer": 1,
        "explanation": "Minions are Gru's small, yellow, pill-shaped helpers who love bananas!",
    },
    {
        "id": 62, "category": "comedy_family",
        "question": "What kind of animal is Babe in the movie 'Babe'?",
        "options": ["A dog", "A sheep", "A pig", "A horse"],
        "answer": 2,
        "explanation": "Babe is an adorable little pig who learns to herd sheep!",
    },
    {
        "id": 63, "category": "comedy_family",
        "question": "In 'Wonka', what does Willy Wonka make?",
        "options": ["Toys", "Chocolate", "Cars", "Clothes"],
        "answer": 1,
        "explanation": "Willy Wonka is a brilliant and eccentric chocolate maker with a magical factory!",
    },
    {
        "id": 64, "category": "comedy_family",
        "question": "In 'The Lego Movie', what is Emmet told he is?",
        "options": ["A villain", "The Special", "A king", "An alien"],
        "answer": 1,
        "explanation": "Emmet, an ordinary Lego minifigure, is told he is 'The Special' who can save the world!",
    },
    {
        "id": 65, "category": "comedy_family",
        "question": "What do the Minions always search for?",
        "options": ["Food", "The most despicable villain to serve", "Gold", "A home"],
        "answer": 1,
        "explanation": "Minions are genetically programmed to seek out and serve the most evil villain!",
    },

    # ========== FANTASY & MAGIC ==========
    {
        "id": 66, "category": "fantasy",
        "question": "In 'Harry Potter', what school does Harry attend?",
        "options": ["Beauxbatons", "Durmstrang", "Hogwarts", "Ilvermorny"],
        "answer": 2,
        "explanation": "Hogwarts School of Witchcraft and Wizardry is located in a Scottish castle!",
    },
    {
        "id": 67, "category": "fantasy",
        "question": "What sport do wizards play on broomsticks in Harry Potter?",
        "options": ["Broomball", "Quidditch", "Skyball", "Wizard Racing"],
        "answer": 1,
        "explanation": "Quidditch is played on flying broomsticks with four balls and seven players per team!",
    },
    {
        "id": 68, "category": "fantasy",
        "question": "In 'The Lord of the Rings', what is the Ring supposed to do?",
        "options": ["Grant wishes", "Make you fly", "Control all other rings and rule Middle-earth", "Turn things to gold"],
        "answer": 2,
        "explanation": "The One Ring was created by Sauron to dominate all other Rings of Power!",
    },
    {
        "id": 69, "category": "fantasy",
        "question": "In 'The Chronicles of Narnia', how do the children enter Narnia?",
        "options": ["A magic door", "A wardrobe", "A painting", "A mirror"],
        "answer": 1,
        "explanation": "Lucy first discovers Narnia by walking through an old wardrobe in the Professor's house!",
    },
    {
        "id": 70, "category": "fantasy",
        "question": "What is the name of the lion in 'The Chronicles of Narnia'?",
        "options": ["Mufasa", "Aslan", "Simba", "Scar"],
        "answer": 1,
        "explanation": "Aslan is the great and noble lion who is the true ruler of Narnia!",
    },
    {
        "id": 71, "category": "fantasy",
        "question": "In 'Harry Potter', what are the four Hogwarts houses?",
        "options": [
            "Gryffindor, Slytherin, Ravenclaw, Hufflepuff",
            "Lions, Snakes, Eagles, Badgers",
            "Red, Green, Blue, Yellow",
            "Brave, Cunning, Smart, Loyal",
        ],
        "answer": 0,
        "explanation": "The four houses are Gryffindor, Slytherin, Ravenclaw, and Hufflepuff!",
    },
    {
        "id": 72, "category": "fantasy",
        "question": "What kind of creature is Dobby in Harry Potter?",
        "options": ["A wizard", "A goblin", "A house-elf", "A troll"],
        "answer": 2,
        "explanation": "Dobby is a free house-elf who becomes one of Harry's most loyal friends.",
    },
    {
        "id": 73, "category": "fantasy",
        "question": "In 'Percy Jackson', who is Percy's godly parent?",
        "options": ["Zeus", "Hades", "Poseidon", "Apollo"],
        "answer": 2,
        "explanation": "Percy Jackson is the son of Poseidon, the Greek god of the sea!",
    },
    {
        "id": 74, "category": "fantasy",
        "question": "What is the name of Frodo's best friend in 'Lord of the Rings'?",
        "options": ["Gandalf", "Aragorn", "Legolas", "Samwise Gamgee"],
        "answer": 3,
        "explanation": "Sam is Frodo's loyal gardener and best friend who sticks with him all the way to Mordor!",
    },
    {
        "id": 75, "category": "fantasy",
        "question": "In 'Harry Potter', what does a Patronus charm protect you from?",
        "options": ["Dragons", "Dementors", "Voldemort", "Dark wizards"],
        "answer": 1,
        "explanation": "A Patronus is a positive-energy guardian that drives away soul-sucking Dementors!",
    },
    {
        "id": 76, "category": "fantasy",
        "question": "What is the name of Gandalf's famous line when facing the Balrog?",
        "options": [
            "Run away!",
            "You shall not pass!",
            "Follow me!",
            "Fight me!",
        ],
        "answer": 1,
        "explanation": "Gandalf dramatically blocks the Balrog on the Bridge of Khazad-dûm!",
    },
    {
        "id": 77, "category": "fantasy",
        "question": "In the 'Wizarding World', what is a Muggle?",
        "options": ["A magical creature", "A non-magical person", "A type of spell", "A wizard's pet"],
        "answer": 1,
        "explanation": "A Muggle is a person with no magical ability — like Harry's aunt and uncle, the Dursleys.",
    },
    {
        "id": 78, "category": "fantasy",
        "question": "What does Harry Potter use to play Quidditch?",
        "options": ["A carpet", "A broomstick", "A skateboard", "A dragon"],
        "answer": 1,
        "explanation": "Harry plays Seeker on a broomstick — first a Nimbus 2000, then a Firebolt!",
    },
    {
        "id": 79, "category": "fantasy",
        "question": "In 'The Hobbit', what is Bilbo hired to be?",
        "options": ["A warrior", "A burglar", "A cook", "A guide"],
        "answer": 1,
        "explanation": "Gandalf recommends Bilbo as the dwarves' burglar for their quest to the Lonely Mountain!",
    },
    {
        "id": 80, "category": "fantasy",
        "question": "What type of creature is Smaug in 'The Hobbit'?",
        "options": ["A giant", "A troll", "A dragon", "An orc"],
        "answer": 2,
        "explanation": "Smaug is a massive, fire-breathing dragon who sleeps on a mountain of gold!",
    },
    {
        "id": 81, "category": "fantasy",
        "question": "In 'Harry Potter', what platform does the Hogwarts Express leave from?",
        "options": ["Platform 8", "Platform 9¾", "Platform 10", "Platform 7½"],
        "answer": 1,
        "explanation": "Students run through the barrier between platforms 9 and 10 to reach Platform 9¾!",
    },

    # ========== MORE ANIMATED ==========
    {
        "id": 82, "category": "animated",
        "question": "In 'Turning Red', what does Mei turn into?",
        "options": ["A wolf", "A giant red panda", "A dragon", "A bear"],
        "answer": 1,
        "explanation": "Mei Lee transforms into a giant fluffy red panda whenever she feels strong emotions!",
    },
    {
        "id": 83, "category": "animated",
        "question": "In 'Soul', what does Joe Gardner want to be?",
        "options": ["A teacher", "A jazz musician", "A painter", "A chef"],
        "answer": 1,
        "explanation": "Joe Gardner is a middle school music teacher whose true passion is playing jazz piano!",
    },
    {
        "id": 84, "category": "animated",
        "question": "What is the name of the kingdom in 'Frozen'?",
        "options": ["Corona", "Arendelle", "Agrabah", "Atlantis"],
        "answer": 1,
        "explanation": "Queen Elsa and Princess Anna are from the kingdom of Arendelle!",
    },
    {
        "id": 85, "category": "animated",
        "question": "In 'Elemental', what are the main characters made of?",
        "options": ["Metal and wood", "Fire and water", "Earth and air", "Light and dark"],
        "answer": 1,
        "explanation": "Ember is a fire person and Wade is a water person who become unlikely friends!",
    },

    # ========== MORE SUPERHEROES ==========
    {
        "id": 86, "category": "superhero",
        "question": "What is the name of Batman's butler?",
        "options": ["Jarvis", "Alfred", "Watson", "Jeeves"],
        "answer": 1,
        "explanation": "Alfred Pennyworth has served the Wayne family for years and helps Batman in his missions!",
    },
    {
        "id": 87, "category": "superhero",
        "question": "In 'Guardians of the Galaxy', who is the talking raccoon?",
        "options": ["Groot", "Drax", "Rocket", "Gamora"],
        "answer": 2,
        "explanation": "Rocket is a genetically modified raccoon who's an expert marksman and pilot!",
    },
    {
        "id": 88, "category": "superhero",
        "question": "What can Groot only say?",
        "options": ["Help me", "I am Groot", "Hello there", "Let's go"],
        "answer": 1,
        "explanation": "Groot can only say 'I am Groot' but means different things depending on how he says it!",
    },
    {
        "id": 89, "category": "superhero",
        "question": "Who is the fastest superhero in the DC universe?",
        "options": ["Superman", "Batman", "The Flash", "Aquaman"],
        "answer": 2,
        "explanation": "The Flash (Barry Allen) can run faster than the speed of light using the Speed Force!",
    },
    {
        "id": 90, "category": "superhero",
        "question": "In 'Shang-Chi', what are the Ten Rings?",
        "options": ["Jewelry", "Ancient powerful weapons", "Doorways", "Musical instruments"],
        "answer": 1,
        "explanation": "The Ten Rings are ancient, powerful arm bands that grant superhuman abilities!",
    },

    # ========== MORE ADVENTURE ==========
    {
        "id": 91, "category": "adventure",
        "question": "What kind of dinosaur is the T-Rex in 'Jurassic Park'?",
        "options": ["Herbivore", "Carnivore", "Omnivore", "Insectivore"],
        "answer": 1,
        "explanation": "Tyrannosaurus Rex was one of the largest meat-eating dinosaurs that ever lived!",
    },
    {
        "id": 92, "category": "adventure",
        "question": "In 'Dune', what is the valuable resource found on the desert planet?",
        "options": ["Gold", "Diamonds", "Spice", "Water"],
        "answer": 2,
        "explanation": "Spice (melange) is the most valuable substance in the Dune universe — it extends life and enables space travel!",
    },
    {
        "id": 93, "category": "adventure",
        "question": "What does Marty McFly use to travel through time in 'Back to the Future'?",
        "options": ["A phone booth", "A DeLorean car", "A train", "A spaceship"],
        "answer": 1,
        "explanation": "The time-travelling DeLorean needs to reach 88 mph and uses a flux capacitor!",
    },

    # ========== MORE COMEDY & FAMILY ==========
    {
        "id": 94, "category": "comedy_family",
        "question": "In 'Diary of a Wimpy Kid', what is the main character's name?",
        "options": ["Rodrick", "Greg Heffley", "Rowley", "Manny"],
        "answer": 1,
        "explanation": "Greg Heffley is a middle schooler who writes about his daily life in a journal!",
    },
    {
        "id": 95, "category": "comedy_family",
        "question": "What kind of animal is Scooby-Doo?",
        "options": ["A beagle", "A bulldog", "A Great Dane", "A poodle"],
        "answer": 2,
        "explanation": "Scooby-Doo is a Great Dane who helps the Mystery Inc. gang solve mysteries!",
    },
    {
        "id": 96, "category": "comedy_family",
        "question": "In 'The Secret Life of Pets', what do pets do when owners leave?",
        "options": ["Sleep all day", "Have their own adventures", "Watch TV", "Clean the house"],
        "answer": 1,
        "explanation": "When their owners leave, the pets go on wild adventures around New York City!",
    },
    {
        "id": 97, "category": "comedy_family",
        "question": "In 'Cloudy with a Chance of Meatballs', what falls from the sky?",
        "options": ["Rain", "Snow", "Food", "Toys"],
        "answer": 2,
        "explanation": "Flint Lockwood invents a machine that turns water into food — causing food weather!",
    },
    {
        "id": 98, "category": "comedy_family",
        "question": "What is the name of the boy in 'Puss in Boots: The Last Wish' who is a villain?",
        "options": ["Jack Horner", "Pinocchio", "Humpty Dumpty", "Goldilocks"],
        "answer": 0,
        "explanation": "Big Jack Horner is a wealthy, selfish villain who wants all the magic for himself!",
    },

    # ========== MORE FANTASY ==========
    {
        "id": 99, "category": "fantasy",
        "question": "In 'Doctor Strange', what is the magical building called?",
        "options": ["The Tower", "The Sanctum Sanctorum", "The Temple", "The Academy"],
        "answer": 1,
        "explanation": "The Sanctum Sanctorum is Doctor Strange's magical headquarters in New York!",
    },
    {
        "id": 100, "category": "fantasy",
        "question": "In 'Fantastic Beasts', who is the main wizard character?",
        "options": ["Dumbledore", "Grindelwald", "Newt Scamander", "Credence"],
        "answer": 2,
        "explanation": "Newt Scamander is a magical zoologist who travels the world studying fantastic beasts!",
    },
]

DIFFICULTY_LEVELS = {
    "easy": "Easy — great for getting started!",
    "medium": "Medium — a bit more challenging!",
    "hard": "Hard — for true movie buffs!",
}


def generate_quiz(num_questions: int = 10, category: str | None = None) -> list:
    """Generate a movie trivia quiz with shuffled options."""
    if category and category in CATEGORIES:
        pool = [q for q in QUESTION_BANK if q["category"] == category]
    else:
        pool = list(QUESTION_BANK)

    if len(pool) < num_questions:
        num_questions = len(pool)

    selected = random.sample(pool, num_questions)

    for q in selected:
        correct_text = q["options"][q["answer"]]
        indices = list(range(len(q["options"])))
        random.shuffle(indices)
        q["options"] = [q["options"][j] for j in indices]
        q["answer"] = q["options"].index(correct_text)

    random.shuffle(selected)
    return selected


def get_category_counts() -> dict:
    """Return {category_id: count} for questions in each category."""
    counts = {cat_id: 0 for cat_id in CATEGORIES}
    for q in QUESTION_BANK:
        counts[q["category"]] += 1
    return counts
