# Parent base class: GeneralFlight (shared attributes for any flight globally)
class GeneralFlight:
    def __init__(
        self, 
        flight_number: str, 
        aircraft_type: str, 
        dep_airport: str, 
        arr_airport: str, 
        depart_time: str, 
        passenger_count: int
        ):
        # Initialize common flight attributes (all inherited into child class automatically)
        self.flight_number = flight_number
        self.aircraft_type = aircraft_type
        self.dep_airport = dep_airport
        self.arr_airport = arr_airport
        self.depart_time = depart_time
        self.passenger_count = passenger_count
        
    def display_route(self) -> str:
        # A shared method to return the flight path
        return f"{self.dep_airport} to {self.arr_airport}"
    
    def display_flight_info(self):
        print(f"Flight: {self.flight_number} | Route: {self.display_route()}")
        print(f"Aircraft: {self.aircraft_type}")
        print(f"Depart Time: {self.depart_time}")
    
        
    def calculate_base_fare(self, flight_distance_km: float) -> float:
        base_price_per_km = 0.28  # Base NZ dollar per KM fixed rate
        base_total = flight_distance_km * base_price_per_km
        return round(base_total, 2)

class DomesticFlight(GeneralFlight):
    def __init__(
        self, 
        flight_number: str, 
        aircraft_type: str, 
        dep_airport: str, 
        arr_airport: str, 
        depart_time: str, 
        passenger_count: int, 
        domestic_tax_rate: float
        ):
        # super().__init__() calls the constructor of the parent class (GeneralFlight)
        # This inherits and sets the shared attributes.
        super().__init__(flight_number, aircraft_type, dep_airport, arr_airport, depart_time, passenger_count)
        
        # Additional attributes specific ONLY to domestic flights
        self.domestic_tax_rate = domestic_tax_rate
     
    def display_flight_info(self):
        # OVERRIDE: 1. Execute parent class print logic
        super().display_flight_info()
        # OVERRIDE: 2. Add child class specific print logic
        print(f"Domestic Tax Rate: {self.domestic_tax_rate * 100}%")
       
    def calculate_final_fare(self, flight_distance_km:float) -> float:
        base_cost = self.calculate_base_fare(flight_distance_km)
        final_cost = base_cost * (1 + self.domestic_tax_rate)
        return round(final_cost, 2)