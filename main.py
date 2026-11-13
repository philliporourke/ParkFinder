
from dataclasses import dataclass
from math import radians, sin, cos, sqrt, atan2
from drafter import *

set_website_title("ParkFinder")
set_site_information(
    "Phillip O'Rourke",
    "Find amusement parks based on location, budget, and attractions.",
    "Drafter documentation and ChatGPT",
    "CISC106 planning and design worksheets",
    []
)

# These are fixed reference locations, not live GPS locations.
STATE_LOCATIONS = {
    "Delaware": (39.16, -75.52),
    "Pennsylvania": (40.27, -76.88),
    "New Jersey": (40.22, -74.76),
    "Maryland": (38.98, -76.49),
    "New York": (42.65, -73.76),
    "Virginia": (37.54, -77.44),
    "North Carolina": (35.78, -78.64),
    "South Carolina": (34.00, -81.03),
    "Ohio": (39.96, -83.00),
    "Florida": (28.54, -81.38),
    "California": (34.05, -118.24),
    "Texas": (30.27, -97.74),
    "Georgia": (33.75, -84.39),
    "Tennessee": (36.16, -86.78),
    "Michigan": (42.73, -84.55)
}


@dataclass
class Park:
    name: str
    state: str
    price: int
    latitude: float
    longitude: float
    ride_type: str
    attractions: str
    description: str


@dataclass
class State:
    location: str
    budget: int
    max_distance: int
    ride_preference: str
    favorites: list[Park]


# Estimated prices are examples, not live ticket prices.
PARKS = [
    Park(
        "Hersheypark", "Pennsylvania", 75,
        40.29, -76.65, "Thrill rides",
        "Candymonium, Skyrush, Great Bear",
        "A chocolate-themed park with exciting rides."
    ),
    Park(
        "Six Flags Great Adventure", "New Jersey", 65,
        40.14, -74.44, "Thrill rides",
        "El Toro, Nitro, Jersey Devil Coaster",
        "A popular park with major roller coasters."
    ),
    Park(
        "Dorney Park", "Pennsylvania", 55,
        40.58, -75.53, "Water rides",
        "Steel Force, Hydra, Wildwater Kingdom",
        "A park with roller coasters and water attractions."
    ),
    Park(
        "Kings Dominion", "Virginia", 60,
        37.84, -77.45, "Thrill rides",
        "Project 305, Twisted Timbers, Dominator",
        "A Virginia park with exciting roller coasters."
    ),
    Park(
        "Busch Gardens Williamsburg", "Virginia", 95,
        37.23, -76.65, "Family rides",
        "Pantheon, Griffon, Verbolten",
        "A European-themed amusement park."
    ),
    Park(
        "Cedar Point", "Ohio", 85,
        41.48, -82.68, "Thrill rides",
        "Millennium Force, Maverick, Steel Vengeance",
        "A famous park known for its roller coasters."
    ),
    Park(
        "Kings Island", "Ohio", 70,
        39.34, -84.27, "Family rides",
        "Orion, Diamondback, The Beast",
        "A large park with thrill rides and family attractions."
    ),
    Park(
        "Carowinds", "North Carolina", 65,
        35.10, -80.94, "Thrill rides",
        "Fury 325, Copperhead Strike, Afterburn",
        "An amusement park on the Carolinas state line."
    ),
    Park(
        "Universal Studios Florida", "Florida", 125,
        28.48, -81.47, "Family rides",
        "Revenge of the Mummy, Gringotts, Transformers",
        "A movie-themed park with rides and entertainment."
    ),
    Park(
        "Disney Magic Kingdom", "Florida", 160,
        28.42, -81.58, "Family rides",
        "TRON Lightcycle Run, Space Mountain, Haunted Mansion",
        "A Disney park with classic attractions."
    ),
    Park(
        "Disneyland Park", "California", 150,
        33.81, -117.92, "Family rides",
        "Space Mountain, Indiana Jones Adventure, Pirates",
        "A classic Disney theme park in California."
    ),
    Park(
        "Six Flags Magic Mountain", "California", 75,
        34.43, -118.60, "Thrill rides",
        "Twisted Colossus, X2, Tatsu",
        "A California park famous for roller coasters."
    ),
    Park(
        "Six Flags Over Texas", "Texas", 60,
        32.76, -97.07, "Thrill rides",
        "New Texas Giant, Titan, Mr. Freeze",
        "A Texas park with coasters and family rides."
    ),
    Park(
        "Six Flags Over Georgia", "Georgia", 60,
        33.77, -84.55, "Thrill rides",
        "Goliath, Twisted Cyclone, Batman The Ride",
        "A Georgia park with thrilling attractions."
    ),
    Park(
        "Dollywood", "Tennessee", 90,
        35.80, -83.53, "Family rides",
        "Lightning Rod, Wild Eagle, Big Bear Mountain",
        "A mountain-themed park with rides and entertainment."
    ),
    Park(
        "Michigan's Adventure", "Michigan", 50,
        43.35, -86.28, "Water rides",
        "Shivering Timbers, Thunderhawk, WildWater Adventure",
        "A Michigan park with roller coasters and water rides."
    )
]


def distance_miles(lat1: float, lon1: float,
                   lat2: float, lon2: float) -> int:
    """Calculate approximate straight-line distance in miles."""
    radius = 3959

    lat_difference = radians(lat2 - lat1)
    lon_difference = radians(lon2 - lon1)

    a = sin(lat_difference / 2) ** 2
    a += (cos(radians(lat1)) * cos(radians(lat2))
          * sin(lon_difference / 2) ** 2)

    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return round(radius * c)


def get_distance(location: str, park: Park) -> int:
    """Calculate distance from a state reference point to a park."""
    latitude, longitude = STATE_LOCATIONS[location]

    return distance_miles(
        latitude, longitude,
        park.latitude, park.longitude
    )


def matches_search(state: State, park: Park) -> bool:
    """Check whether a park matches the search settings."""
    if park.price > state.budget:
        return False

    if get_distance(state.location, park) > state.max_distance:
        return False

    if state.ride_preference != "Any":
        if park.ride_type != state.ride_preference:
            return False

    return True


def find_matches(state: State) -> list[Park]:
    """Find parks matching the user's preferences."""
    matches = []

    for park in PARKS:
        if matches_search(state, park):
            matches.append(park)

    matches.sort(key=lambda park: get_distance(state.location, park))

    return matches


def is_favorite(state: State, park: Park) -> bool:
    """Check whether a park is already saved."""
    for favorite in state.favorites:
        if favorite.name == park.name:
            return True

    return False


def navigation() -> list:
    """Create navigation links."""
    return [
        Link("Home", "index"),
        " | ",
        Link("Find Parks", "search"),
        " | ",
        Link("Results", "results"),
        " | ",
        Link("Favorites", "favorites"),
        " | ",
        Link("About", "about")
    ]


@route
def index(state: State) -> Page:
    """Display the homepage."""
    return Page(state, [
        Header("PARKFINDER"),
        Header("Find Your Next Adventure", 2),
        "Discover amusement parks based on your preferences!",
        Header("How It Works", 2),
        "1. Select your state.",
        "2. Choose your ticket budget.",
        "3. Choose how far you want to travel.",
        "4. Select your favorite attractions.",
        "5. Explore parks and save your favorites.",
        Button("Start Exploring", "search"),
        Header("Your Favorites", 3),
        "Saved parks: " + str(len(state.favorites)),
        *navigation()
    ])


@route
def search(state: State) -> Page:
    """Display the amusement park search form."""
    return Page(state, [
        Header("Find Amusement Parks"),
        "Enter your preferences below.",
        Header("Your State", 3),
        SelectBox(
            "new_location",
            list(STATE_LOCATIONS.keys()),
            state.location
        ),
        Header("Maximum Ticket Budget ($)", 3),
        TextBox("new_budget", str(state.budget), "number"),
        Header("Maximum Distance (miles)", 3),
        TextBox("new_distance", str(state.max_distance), "number"),
        Header("Favorite Attraction Type", 3),
        SelectBox(
            "new_preference",
            ["Any", "Thrill rides", "Family rides", "Water rides"],
            state.ride_preference
        ),
        Button("Find My Parks", "update_search"),
        "Distances and ticket prices are estimates.",
        *navigation()
    ])


@route
def update_search(state: State, new_location: str,
                  new_budget: int, new_distance: int,
                  new_preference: str) -> Page:
    """Update the user's search preferences."""
    if new_budget < 0 or new_distance < 0:
        return Page(state, [
            Header("Invalid Search"),
            "Budget and distance cannot be negative.",
            Link("Try Again", "search")
        ])

    if new_location not in STATE_LOCATIONS:
        return search(state)

    state.location = new_location
    state.budget = new_budget
    state.max_distance = new_distance
    state.ride_preference = new_preference

    return results(state)


@route
def results(state: State) -> Page:
    """Display amusement parks matching the search."""
    matches = find_matches(state)

    content = [
        Header("Your Park Recommendations"),
        "Starting state: " + state.location,
        "Maximum budget: $" + str(state.budget),
        "Maximum distance: " + str(state.max_distance) + " miles",
        "Attraction preference: " + state.ride_preference,
        Header(str(len(matches)) + " Parks Found", 2),
        Button("Change Search", "search"),
        Button("Cheapest Matching Park", "cheapest_park")
    ]

    if len(matches) == 0:
        content.append("No parks match your search.")
        content.append("Try increasing your budget or distance.")
    else:
        for park in matches:
            park_index = PARKS.index(park)
            miles = get_distance(state.location, park)

            content.append(Header(park.name, 3))
            content.append("State: " + park.state)
            content.append("Estimated ticket: $" + str(park.price))
            content.append("Approximate distance: " + str(miles) + " miles")
            content.append("Best for: " + park.ride_type)
            content.append(
                Button(
                    "View Details",
                    "park_details",
                    [Argument("park_index", park_index)]
                )
            )

    content.extend(navigation())
    return Page(state, content)


@route
def park_details(state: State, park_index: int) -> Page:
    """Display information about a selected park."""
    if park_index < 0 or park_index >= len(PARKS):
        return results(state)

    park = PARKS[park_index]
    miles = get_distance(state.location, park)

    content = [
        Header(park.name),
        park.description,
        Header("Park Information", 2),
        "State: " + park.state,
        "Estimated ticket price: $" + str(park.price),
        "Approximate distance: " + str(miles) + " miles",
        "Attraction type: " + park.ride_type,
        Header("Top Attractions", 2),
        park.attractions
    ]

    if is_favorite(state, park):
        content.append("This park is already in your favorites.")
    else:
        content.append(
            Button(
                "Add to Favorites",
                "add_favorite",
                [Argument("park_index", park_index)]
            )
        )

    content.append(Link("Back to Results", "results"))
    content.extend(navigation())

    return Page(state, content)


@route
def add_favorite(state: State, park_index: int) -> Page:
    """Save a park to the favorites list."""
    if 0 <= park_index < len(PARKS):
        park = PARKS[park_index]

        if not is_favorite(state, park):
            state.favorites.append(park)

        return park_details(state, park_index)

    return results(state)


@route
def favorites(state: State) -> Page:
    """Display saved amusement parks."""
    content = [
        Header("My Favorite Parks"),
        "Here are the parks you saved."
    ]

    if len(state.favorites) == 0:
        content.append("You have not saved any parks yet.")
        content.append(Link("Find Parks", "search"))
    else:
        for park in state.favorites:
            park_index = PARKS.index(park)

            content.append(Header(park.name, 3))
            content.append("State: " + park.state)
            content.append("Estimated price: $" + str(park.price))
            content.append(
                Button(
                    "View Details",
                    "park_details",
                    [Argument("park_index", park_index)]
                )
            )
            content.append(
                Button(
                    "Remove Favorite",
                    "remove_favorite",
                    [Argument("park_index", park_index)]
                )
            )

    content.extend(navigation())
    return Page(state, content)


@route
def remove_favorite(state: State, park_index: int) -> Page:
    """Remove a park from favorites."""
    if 0 <= park_index < len(PARKS):
        park = PARKS[park_index]

        if is_favorite(state, park):
            state.favorites.remove(park)

    return favorites(state)


@route
def cheapest_park(state: State) -> Page:
    """Show the cheapest park matching the current search."""
    matches = find_matches(state)

    if len(matches) == 0:
        return Page(state, [
            Header("No Parks Found"),
            "Try changing your search preferences.",
            Link("Change Search", "search")
        ])

    cheapest = matches[0]

    for park in matches:
        if park.price < cheapest.price:
            cheapest = park

    return Page(state, [
        Header("Best Budget Option"),
        Header(cheapest.name, 2),
        "Estimated ticket price: $" + str(cheapest.price),
        "Location: " + cheapest.state,
        "Top attractions: " + cheapest.attractions,
        Button(
            "View Park Details",
            "park_details",
            [Argument("park_index", PARKS.index(cheapest))]
        ),
        *navigation()
    ])


@route
def about(state: State) -> Page:
    """Explain ParkFinder and its limitations."""
    return Page(state, [
        Header("About ParkFinder"),
        "ParkFinder helps people discover amusement parks.",
        "Search by state, ticket budget, distance, and attractions.",
        Header("How Recommendations Work", 2),
        "The website checks a built-in list of amusement parks.",
        "It filters parks using your selected preferences.",
        "Matching parks are sorted by approximate distance.",
        Header("Important Information", 2),
        "Ticket prices are example estimates, not live prices.",
        "Distances are straight-line miles from state reference points.",
        "Actual driving distances may be longer.",
        "Check official park websites before visiting.",
        Header("Created For", 2),
        "CISC106 Final Project",
        "University of Delaware",
        *navigation()
    ])


def run_tests() -> None:
    """Test the main calculations and website routes."""
    test_park = Park(
        "Test Park", "Delaware", 40,
        39.16, -75.52, "Thrill rides",
        "Test Coaster", "A test amusement park."
    )

    test_state = State("Delaware", 100, 500, "Any", [])

    assert distance_miles(39.16, -75.52, 39.16, -75.52) == 0
    assert matches_search(test_state, test_park)
    assert not is_favorite(test_state, test_park)

    test_state.favorites.append(test_park)
    assert is_favorite(test_state, test_park)

    empty_state = State("Delaware", 0, 0, "Any", [])
    assert len(find_matches(empty_state)) == 0

    updated = State("Delaware", 100, 500, "Any", [])
    page = update_search(updated, "Ohio", 90, 200, "Thrill rides")

    assert isinstance(page, Page)
    assert updated.location == "Ohio"
    assert updated.budget == 90
    assert updated.max_distance == 200
    assert updated.ride_preference == "Thrill rides"

    saved = State("Delaware", 100, 500, "Any", [])
    assert isinstance(add_favorite(saved, 0), Page)
    assert len(saved.favorites) == 1

    assert isinstance(remove_favorite(saved, 0), Page)
    assert len(saved.favorites) == 0

    assert isinstance(index(saved), Page)
    assert isinstance(search(saved), Page)
    assert isinstance(results(saved), Page)
    assert isinstance(park_details(saved, 0), Page)
    assert isinstance(favorites(saved), Page)
    assert isinstance(cheapest_park(saved), Page)
    assert isinstance(about(saved), Page)


if __name__ == "__main__":
    run_tests()
    print("Tests passed!")
    start_server(State("Delaware", 100, 250, "Any", []))
