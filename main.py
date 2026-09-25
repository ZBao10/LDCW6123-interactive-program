import os

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

def display_header():
    print("=============================================")
    print("           BOLT ON-DEMAND SERVICES           ")
    print("=============================================")


def display_main_menu():
    print("1. Book / Estimate Ride Fare")
    print("2. Order / Estimate Food Delivery")
    print("3. Exit System")
    print("---------------------------------------------")


def apply_promo_code(code: str, fare: float) -> tuple[bool, float]:
    valid_promos = ["BOLTDISRUPT", "BOLT2026"]
    if code.upper() in valid_promos:
        return True, fare * 0.85  # 15% discount
    return False, fare


def estimate_ride_fare():
    print("\n--- Bolt Ride Booking ---")
    print("Select Ride Option:")
    print("  1. Bolt Standard (Eco/Sedan)")
    print("  2. Bolt Green (Electric Vehicle)")
    print("  3. Bolt Premium (Executive Comfort)")
    print("  4. Bolt XL (6-Seater)")

    try:
        ride_type = int(input("Select option (1-4): ").strip())
        if ride_type not in (1, 2, 3, 4):
            print("Invalid ride option selected. Returning to main menu.\n")
            return

        distance = float(input("Enter estimated trip distance in kilometers: ").strip())
        duration = float(input("Enter estimated trip duration in minutes: ").strip())

        if distance <= 0 or duration <= 0:
            print("Distance and duration must be positive numbers.\n")
            return

    except ValueError:
        print("Invalid numerical input. Returning to main menu.\n")
        return

    # Base pricing configurations
    pricing_plans = {
        1: {"name": "Bolt Standard", "base": 3.00, "per_km": 1.25, "per_min": 0.25},
        2: {"name": "Bolt Green (EV)", "base": 3.50, "per_km": 1.35, "per_min": 0.25},
        3: {"name": "Bolt Premium", "base": 6.00, "per_km": 2.10, "per_min": 0.45},
        4: {"name": "Bolt XL", "base": 5.00, "per_km": 1.80, "per_min": 0.35},
    }

    selected = pricing_plans[ride_type]
    total_fare = selected["base"] + (distance * selected["per_km"]) + (duration * selected["per_min"])

    # Peak hour surge
    is_peak = input("Is it peak demand / rush hour? (Y/N): ").strip().upper()
    if is_peak == 'Y':
        total_fare *= 1.30  # 30% surge multiplier
        print(">> Peak hour pricing (1.3x) applied.")

    # Promo code
    has_promo = input("Do you have a promo code? (Y/N): ").strip().upper()
    if has_promo == 'Y':
        promo_code = input("Enter Promo Code: ").strip()
        is_valid, total_fare = apply_promo_code(promo_code, total_fare)
        if is_valid:
            print(">> Promo code validated! 15% discount applied.")
        else:
            print(">> Invalid promo code. Standard fare remains.")

    # Receipt display
    print("\n------------- RIDE RECEIPT -------------")
    print(f"Service Type     : {selected['name']}")
    print(f"Total Distance   : {distance:.2f} km")
    print(f"Est. Duration    : {duration:.2f} mins")
    print(f"Final Total Fare : RM {total_fare:.2f}")
    print("----------------------------------------")
    
    confirm = input("Confirm ride booking? (1 for Yes, 0 for No): ").strip()
    if confirm == "1":
        print("Booking Confirmed! Driver assigned nearby.\n")
    else:
        print("Booking cancelled.\n")


def estimate_food_delivery():
    print("\n--- Bolt Food Delivery ---")
    try:
        basket_total = float(input("Enter food basket subtotal (RM): ").strip())
        delivery_distance = float(input("Enter delivery distance (km): ").strip())

        if basket_total <= 0 or delivery_distance <= 0:
            print("Values must be greater than zero.\n")
            input("Press Enter to return to the main menu...")
            return

    except ValueError:
        print("Invalid numerical input. Returning to main menu.\n")
        input("Press Enter to return to the main menu...")
        return

    delivery_fee = 2.50 + (delivery_distance * 0.80)
    small_order_fee = 2.00 if basket_total < 15.00 else 0.00
    final_payable = basket_total + delivery_fee + small_order_fee

    print("\n------------ ORDER SUMMARY ------------")
    print(f"Basket Subtotal  : RM {basket_total:.2f}")
    print(f"Delivery Fee     : RM {delivery_fee:.2f}")

    if small_order_fee > 0:
        print(f"Small Order Fee  : RM {small_order_fee:.2f}")

    print(f"Total Payable    : RM {final_payable:.2f}")
    print("----------------------------------------")

    input("\nPress Enter to return to the main menu...")


def main():
    while True:
        clear_screen()
        display_header()
        display_main_menu()

        choice = input("Enter your selection (1-3): ").strip()

        if choice == "1":
            clear_screen()
            estimate_ride_fare()

        elif choice == "2":
            clear_screen()
            estimate_food_delivery()

        elif choice == "3":
            clear_screen()
            print("\nThank you for choosing Bolt. Moving forward together!")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")
            input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()