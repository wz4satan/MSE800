from classes_nz_airline import DomesticFlight, InternationalFlight

def main():
    print("=====================================================")
    print("      AIR NEW ZEALAND FLIGHT MANAGEMENT SYSTEM       ")
    print("=====================================================\n")
    
    # 1. Test Domestic Flight (Inherits core data + signature domestic cookie service)
    print("--- Test 1: Air NZ Domestic Flight (Auckland -> Christchurch) ---")
    domestic = DomesticFlight(
        flight_number="NZ501",
        aircraft_type="Airbus A320",
        dep_airport="AKL",
        arr_airport="CHC",
        depart_time="08:30 10-SEP-2026",
        passenger_count=145,
        snack_option="Cookie Time Chocolate Chunk Cookie", 
        # Basic amenity attribute
        has_wifi=False,
        domestic_tax_rate=0.15
    )
    
    domestic.show_safety_video() # Inherited from BasicAmenities
    domestic.display_flight_info() # Overridden method
    print(f"Final Fare (incl. tax): ${domestic.calculate_final_fare(740)} NZD")
    domestic.announce_baggage_claim() # Domestic specific method
    
    print("\n" + "="*50 + "\n")
    
    # 2. Test International Flight (Inherits core data + magazines + expands with full meals, duty-free, customs)
    print("--- Test 2: Air NZ International Flight (Auckland -> Sydney) ---")
    international = InternationalFlight(
        flight_number="NZ103",
        aircraft_type="Boeing 787-9",
        dep_airport="AKL",
        arr_airport="SYD",
        depart_time="14:15 12-SEP-2026",
        passenger_count=280,
        snack_option="Cassava Veggie Chips", 
        # Basic amenity attribute
        has_wifi=True,
        international_tax_rate=0.10,
        meal_choice="NZ Roasted Lamb or Creamy Vegetarian Pasta" # International specific attribute
    )
    
    international.display_flight_info() # Overridden method
    print(f"Final Fare (incl. tax & surcharge): ${international.calculate_final_fare(2160)} NZD")
    international.offer_duty_free_service() 
    # International specific service
    international.verify_customs_clearance() 
    # International specific method
    
if __name__ == "__main__":
    main()   
    
    