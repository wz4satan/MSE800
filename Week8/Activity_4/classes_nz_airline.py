# ------------------------------------------------------
# PARENT CLASS 1: Core Flight Data
# ------------------------------------------------------
class GeneralFlight:
    def __init__(
        self,
        flight_number: str,
        aircraft_type: str,
        dep_airport: str,
        arr_airport: str,
        depart_time: str,
        passenger_count: int,
    ):
        self.flight_number = flight_number
        self.aircraft_type = aircraft_type
        self.dep_airport = dep_airport
        self.arr_airport = arr_airport
        self.depart_time = depart_time
        self.passenger_count = passenger_count

    def display_route(self) -> str:
        # Method 1: Return the flight route
        return f"{self.dep_airport} to {self.arr_airport}"

    def display_flight_info(self):
        # Method 2: Print core flight information
        print(f"Flight: {self.flight_number} | Route: {self.display_route()}")
        print(f"Aircraft: {self.aircraft_type} | Passengers: {self.passenger_count}")
        print(f"Depart Time: {self.depart_time}")

    def calculate_base_fare(self, flight_distance_km: float) -> float:
        # Method 3: Calculate base fare (Air NZ standard per-km rate)
        base_price_per_km = 0.28
        return round(flight_distance_km * base_price_per_km, 2)


# -------------------------------------------------------
# PARENT CLASS 2: Basic In-flight Amenities
# Shared by both domestic and international)
# -------------------------------------------------------
class BasicAmenities:
    def __init__(self, snack_option: str, has_wifi: bool):
        # e.g., "Cookie Time" or "Cassava Chips"
        self.snack_option = snack_option
        self.has_wifi = has_wifi

    def serve_basic_refreshments(self):
        # Method 1: Serve signature basic refreshments
        print(
            f"In-flight Service: Complimentary coffee, tea, and {self.snack_option} will now be served."
        )

    def distribute_reading_material(self):
        # Method 2: Distribute the Kia Ora magazine
        print(
            "In-flight Service: The latest Kia Ora magazine is available in your seat pocket."
        )

    def show_safety_video(self):
        # Method 3: Show the signature Air NZ safety video
        print(
            "Cabin Announcement: Please direct your attention to the screens for the Air New Zealand safety video."
        )


# -------------------------------------------------------
# CHILD CLASS 1: Domestic Flight
# (Multiple inheritance from GeneralFlight & BasicAmenities)
# -------------------------------------------------------
class DomesticFlight(GeneralFlight, BasicAmenities):
    def __init__(
        self,
        flight_number: str,
        aircraft_type: str,
        dep_airport: str,
        arr_airport: str,
        depart_time: str,
        passenger_count: int,
        snack_option: str,
        has_wifi: bool,
        domestic_tax_rate: float,
    ):
        # Explicitly initialize both parent classes to clearly show attribute inheritance
        GeneralFlight.__init__(
            self,
            flight_number,
            aircraft_type,
            dep_airport,
            arr_airport,
            depart_time,
            passenger_count,
        )
        BasicAmenities.__init__(self, snack_option, has_wifi)
        self.domestic_tax_rate = domestic_tax_rate

    def display_flight_info(self):
        # OVERRIDE Method 1: Call base info, add domestic tax rate and amenities
        # Use super() to call the method overrided in child class from parent class
        super().display_flight_info()
        print(
            f"Flight Type: Domestic | In-flight Wi-Fi: {'Available' if self.has_wifi else 'Not Available'}"
        )
        print(f"Domestic Tax Rate: {self.domestic_tax_rate * 100}%")

        # Call the method inherited from BasicAmenities
        # Use self to call the method inherited from parent class
        self.serve_basic_refreshments()

    def calculate_final_fare(self, flight_distance_km: float) -> float:
        # Method 2: Calculate the final fare including domestic tax
        base_cost = self.calculate_base_fare(flight_distance_km)
        final_cost = base_cost * (1 + self.domestic_tax_rate)
        return round(final_cost, 2)

    def announce_baggage_claim(self):
        # Method 3: Announce baggage claim (specific to domestic)
        print(
            f"Cabin Announcement: Welcome to {self.arr_airport}. Please proceed to the domestic baggage claim area."
        )


# -------------------------------------------------------
# CHILD CLASS 2: International Flight
# (Multiple inheritance from GeneralFlight & BasicAmenities)
# -------------------------------------------------------


class InternationalFlight(GeneralFlight, BasicAmenities):
    def __init__(
        self,
        flight_number: str,
        aircraft_type: str,
        dep_airport: str,
        arr_airport: str,
        depart_time: str,
        passenger_count: int,
        snack_option: str,
        has_wifi: bool,
        international_tax_rate: float,
        meal_choice: str,
    ):
        # Explicitly initialize both parent classes
        GeneralFlight.__init__(
            self,
            flight_number,
            aircraft_type,
            dep_airport,
            arr_airport,
            depart_time,
            passenger_count,
        )
        BasicAmenities.__init__(self, snack_option, has_wifi)

        # As international tax is not a single tax like domestic tax, it can not be abstracted with domestic tax to a parent class
        self.international_tax_rate = international_tax_rate
        # International flights are upgraded to full meals
        self.meal_choice = meal_choice
        # Passports are mandatory for international flights
        self.passport_req = True

    def display_flight_info(self):
        # OVERRIDE Method 1: Combine base info, basic amenities, and add international services
        super().display_flight_info()
        print(
            f"Flight Type: International | Passport Required: {'Yes' if self.passport_req else 'No'}"
        )
        print(f"International Meal Choice: {self.meal_choice}")

    def calculate_final_fare(self, flight_distance_km: float) -> float:
        # Method 2: Calculate final fare including international tax and surcharges (e.g., meal costs)
        base_cost = self.calculate_base_fare(flight_distance_km)
        international_surcharge = 65.00
        # International catering and service surcharge
        final_cost = (base_cost + international_surcharge) * (
            1 + self.international_tax_rate
        )
        return round(final_cost, 2)

    def offer_duty_free_service(self):
        # Method 3: Offer duty-free shopping (specific to international)
        print(
            "In-flight Service: Duty-free shopping is now available. Please check the catalogue in your seat pocket."
        )

    def verify_customs_clearance(self) -> bool:
        # Method 4 (Bonus): Verify customs clearance (specific to international)
        print(
            f"System Alert: Customs clearance data for {self.passenger_count} passengers has been sent to {self.arr_airport} Border Control."
        )
        return True
