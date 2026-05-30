from nz_airline_classes import GeneralFlight, DomesticFlight

if __name__ == "__main__":
    # 1. Create an instance of the Parent Class (General Flight)
    # This might represent a general fleet aircraft where domestic/international isn't specified yet.
    generalflight = GeneralFlight("NZ1", "Boeing 787-9", "AKL", "ZQN", "08:30 10-JUN-2026", 150)
    
    print("\n--- General Flight Information (Parent Class) ---\n")
    generalflight.display_flight_info()
    
    # 2. Create an instance of the Subclass (Domestic Flight)
    # This specific flight inherits the general properties but adds domestic-only features.
    domesticflight = DomesticFlight(
       flight_number = "NZ501",
       aircraft_type = "Airbus A320",
       dep_airport = "AKL",
       arr_airport = "CHC",
       depart_time = "08:30 10-SEP-2026",
       passenger_count = 140,
       domestic_tax_rate = 0.15
    )
    
    # 3. Call the overridden method on the subclass
    # This demonstrates inheritance in action: it uses parent attributes + subclass attributes
    print("--- Domestic Flight Information (Child Class) ---\n")
    print(f"The information of the flight:")
    domesticflight.display_flight_info()
    
    distance = 350
    
    print(f"\nFare Breakdown for {distance}km:")
    print(f"Base Fare: ${domesticflight.calculate_base_fare(distance)}")
    print(f"Final Fare (incl. tax): ${domesticflight.calculate_final_fare(distance)}")
    