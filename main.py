"""
====================================================================
LDCW6123 - Fundamentals of Digital Competence for Programmer
Group Project: Part 2 - Interactive Program (Bolt On-Demand Services)

Description:
    An interactive CLI program simulating Bolt's ride-hailing and 
    food delivery services, featuring fare breakdown, peak hour 
    multipliers, promo discounts, and session history tracking.
====================================================================
"""
import os
from datetime import datetime
from decimal import Decimal, InvalidOperation

# Global session storage for bookings and orders
TRIP_HISTORY = []
FOOD_HISTORY = []
PRICING_PLANS = {
    "1": {"name": "Bolt Standard", "base": Decimal("3.00"), "per_km": Decimal("1.25"), "per_min": Decimal("0.25")},
    "2": {"name": "Bolt Green (EV)", "base": Decimal("3.50"), "per_km": Decimal("1.35"), "per_min": Decimal("0.25")},
    "3": {"name": "Bolt Premium", "base": Decimal("6.00"), "per_km": Decimal("2.10"), "per_min": Decimal("0.45")},
    "4": {"name": "Bolt XL", "base": Decimal("5.00"), "per_km": Decimal("1.80"), "per_min": Decimal("0.35")},
}


def clear_screen():
    """Clears the terminal screen for a better user interface experience."""
    os.system("cls" if os.name == "nt" else "clear")


def display_header():
    """Displays the system banner heading."""
    print("=============================================")
    print("           BOLT ON-DEMAND SERVICES           ")
    print("=============================================")


def display_main_menu():
    """Displays available menu options."""
    print("1. Book / Estimate Ride Fare")
    print("2. Order / Estimate Food Delivery")
    print("3. View Past Trip History")
    print("4. View Past Food Orders")
    print("5. Exit System")
    print("---------------------------------------------")


def read_choice(prompt, valid_choices):
    """Validates user menu selections to ensure input matches valid options."""
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid selection. Please enter one of: {', '.join(valid_choices)}.")


def read_positive_decimal(prompt):
    """Ensures input values for distance, duration, or cost are positive numbers."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = Decimal(raw_value)
            if value.is_finite() and value > 0:
                return value
        except InvalidOperation:
            pass
        print("Please enter a finite number greater than zero.")


def read_yes_no(prompt):
    """Safely handles Yes/No user decisions."""
    while True:
        answer = input(prompt).strip().upper()
        if answer in ("Y", "N"):
            return answer == "Y"
        print("Please enter Y or N.")


def read_confirmation(prompt="Confirm ride booking? (1 for Yes, 0 for No): "):
    """Handles final booking or order confirmations."""
    while True:
        answer = input(prompt).strip()
        if answer in ("1", "0"):
            return answer == "1"
        print("Please enter 1 to confirm or 0 to cancel.")


def apply_promo_code(code, fare):
    """Validates promotional discount codes and applies discount if valid."""
    valid_promos = {"BOLTDISRUPT", "BOLT2026"}
    if code.strip().upper() in valid_promos:
        return True, fare * Decimal("0.85")
    return False, fare


def display_trip_history():
    """Displays all confirmed ride bookings stored in current session memory."""
    print("\n------------- PAST TRIP HISTORY -------------")
    if not TRIP_HISTORY:
        print("No confirmed trips found in this session.")
    else:
        for index, record in enumerate(TRIP_HISTORY, start=1):
            print(f"{index}. {record['service']} | {record['distance']} km | "
                  f"{record['duration']} mins | RM {record['fare']}")
            if record.get("date"):
                print(f"   Booked: {record['date']}")
    print("---------------------------------------------")
    input("Press Enter to return to the main menu...")


def display_food_history():
    """Displays all confirmed food delivery orders stored in current session memory."""
    print("\n----------- PAST FOOD ORDER HISTORY -----------")
    if not FOOD_HISTORY:
        print("No confirmed food orders found in this session.")
    else:
        for index, record in enumerate(FOOD_HISTORY, start=1):
            print(f"{index}. Basket RM {record['basket']} | Delivery RM {record['delivery_fee']} | "
                  f"Small order RM {record['small_order_fee']} | Total RM {record['total']}")
            if record.get("date"):
                print(f"   Ordered: {record['date']}")
    print("-----------------------------------------------")
    input("Press Enter to return to the main menu...")


def estimate_ride_fare():
    """
    Calculates estimated ride fare based on distance, duration, service tier,
    peak hour multiplier, and optional promo codes.
    """
    print("\n--- Bolt Ride Booking ---")
    print("Select Ride Option:")
    print("  1. Bolt Standard (Eco/Sedan)")
    print("  2. Bolt Green (Electric Vehicle)")
    print("  3. Bolt Premium (Executive Comfort)")
    print("  4. Bolt XL (6-Seater)")

    ride_type = read_choice("Select option (1-4): ", tuple(PRICING_PLANS))
    distance = read_positive_decimal("Enter estimated trip distance in kilometers: ")
    duration = read_positive_decimal("Enter estimated trip duration in minutes: ")

    selected = PRICING_PLANS[ride_type]
    base_fare = selected["base"]
    distance_fare = distance * selected["per_km"]
    duration_fare = duration * selected["per_min"]
    subtotal = base_fare + distance_fare + duration_fare
    surge_amount = Decimal("0.00")
    discount_amount = Decimal("0.00")
    total_fare = subtotal

    if read_yes_no("Is it peak demand / rush hour? (Y/N): "):
        total_fare = subtotal * Decimal("1.30")
        surge_amount = total_fare - subtotal
        print(">> Peak hour pricing (1.3x) applied.")

    if read_yes_no("Do you have a promo code? (Y/N): "):
        promo_code = input("Enter Promo Code: ").strip()
        is_valid, discounted_total = apply_promo_code(promo_code, total_fare)
        if is_valid:
            discount_amount = total_fare - discounted_total
            total_fare = discounted_total
            print(">> Promo code validated! 15% discount applied.")
        else:
            print(">> Invalid promo code. Standard fare remains.")

    total_fare = total_fare.quantize(Decimal("0.01"))
    print("\n------------- RIDE FARE BREAKDOWN -------------")
    print(f"Service Type       : {selected['name']}")
    print(f"Base fare          : RM {base_fare:.2f}")
    print(f"Distance ({distance:.2f} km) : RM {distance_fare:.2f}")
    print(f"Time ({duration:.2f} min)    : RM {duration_fare:.2f}")
    print(f"Peak surcharge     : RM {surge_amount.quantize(Decimal('0.01')):.2f}")
    print(f"Promo discount     : -RM {discount_amount.quantize(Decimal('0.01')):.2f}")
    print("-----------------------------------------------")
    print(f"Estimated total    : RM {total_fare:.2f}")
    print("-----------------------------------------------")

    if read_confirmation():
        TRIP_HISTORY.append({
            "service": selected["name"],
            "distance": f"{distance:.2f}",
            "duration": f"{duration:.2f}",
            "fare": f"{total_fare:.2f}",
            "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        })
        print("Booking Confirmed! Driver assigned nearby.\n")
    else:
        print("Booking cancelled.\n")


def estimate_food_delivery():
    """Calculates food delivery fare, including distance-based fee and small order surcharge."""
    print("\n--- Bolt Food Delivery ---")
    basket_total = read_positive_decimal("Enter food basket subtotal (RM): ")
    delivery_distance = read_positive_decimal("Enter delivery distance (km): ")

    delivery_fee = Decimal("2.50") + (delivery_distance * Decimal("0.80"))
    small_order_fee = Decimal("2.00") if basket_total < Decimal("15.00") else Decimal("0.00")
    final_payable = (basket_total + delivery_fee + small_order_fee).quantize(Decimal("0.01"))

    print("\n------------ ORDER PRICE BREAKDOWN ------------")
    print(f"Basket subtotal    : RM {basket_total:.2f}")
    print(f"Delivery fee       : RM {delivery_fee:.2f} ({delivery_distance:.2f} km)")
    print(f"Small order fee    : RM {small_order_fee:.2f}")
    print("-----------------------------------------------")
    print(f"Total payable      : RM {final_payable:.2f}")
    print("-----------------------------------------------")

    if read_confirmation("Confirm food order? (1 for Yes, 0 for No): "):
        FOOD_HISTORY.append({
            "basket": f"{basket_total:.2f}",
            "delivery_fee": f"{delivery_fee.quantize(Decimal('0.01')):.2f}",
            "small_order_fee": f"{small_order_fee:.2f}",
            "total": f"{final_payable:.2f}",
            "date": datetime.now().astimezone().isoformat(timespec="seconds"),
        })
        print("Food order confirmed.\n")
    else:
        print("Food order cancelled.\n")
    input("Press Enter to return to the main menu...")


def main():
    """Main execution loop for the interactive CLI system."""
    while True:
        clear_screen()
        display_header()
        display_main_menu()

        choice = read_choice("Enter your selection (1-5): ", ("1", "2", "3", "4", "5"))
        if choice == "1":
            clear_screen()
            estimate_ride_fare()
            input("Press Enter to return to the main menu...")
        elif choice == "2":
            clear_screen()
            estimate_food_delivery()
        elif choice == "3":
            clear_screen()
            display_trip_history()
        elif choice == "4":
            clear_screen()
            display_food_history()
        else:
            clear_screen()
            print("\nThank you for choosing Bolt. Session history will be cleared when the program exits.")
            break


if __name__ == "__main__":
    main()
