from datetime import date, timedelta

FILE_NAME = "tips.txt"

def get_date():
    user_input = input("Enter a date (YYYY-MM-DD) or press ENTER for today: ")

    if user_input.strip() == "":
        return date.today().isoformat()
    else:
        return user_input

def add_tips():
    while True:
        user_input = input("Enter an amount or 'q' to exit: ")
        if user_input.lower() == "q":
            return None
        
        try:    
            amount = int(user_input)
            if amount < 0:
                print("Tips must be positive!")
                continue
            break
        except ValueError:
            print("Enter a number, please!")
    
    while True:
        date_input = input("Enter a date or 'q' to exit: ")
        if date_input.lower() == "q":
            return None
        try:
            tip_date = date.fromisoformat(date_input)
        except ValueError:
            print("Invalid date format.")
            continue

        if tip_date > date.today():
            print("Date can not be in the future.")
            continue
        break

    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(f"{tip_date} {amount}\n")

        print("Information saved.")
    
    comment = get_fun_comment(amount)
    print(comment)

def add_tips_for_past_day():
    while True:
        user_input = input("Enter an amount or 'q' to exit: ")
        if user_input.lower() == "q":
            return None
        try:
            amount = int(user_input)
            if amount < 0:
                print("Tips must be positive")
                continue
            break
        except ValueError:
            print("Enter a number, please!")

    while True:
        date_input = input("Enter a date (YYYY-MM-DD) or 'q' to exit: ")
        if date_input.lower() == "q":
            return None

        try:
            tip_date = date.fromisoformat(date_input)
        except ValueError:
            print("Invalid date format.")
            continue

        if tip_date >= date.today():
            print("Date must be in the past.")
            continue

        break

    with open(FILE_NAME, "a", encoding="utf-8") as file:
        file.write(f"{tip_date.isoformat()} {amount}\n")

def read_tips():

    tips = []

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split()

                if len(parts) != 2:
                    continue

                date_str, amount = parts

                try:
                    amount = int(amount)
                except ValueError:
                    continue

                tips.append((date_str, int(amount)))
    except FileNotFoundError:
        pass
    return tips


def total_for_day():
    today = date.today().isoformat()
    tips = read_tips()

    total = 0

    for tip_date, amount in tips:
        if tip_date == today:
            total += amount

    print(f"Tips for today: {total} kc.")

def total_for_week():
    tips = read_tips()
    today = date.today()
    week_ago = today - timedelta(days=7)

    total = 0

    for tip_date, amount in tips:
        tip_day = date.fromisoformat(tip_date)

        if week_ago <= tip_day <= today:
            total += amount

    print(f"Tips for last 7 days: {total}")

def best_day_of_week():
    tips = read_tips()
    today = date.today()
    week_ago = today - timedelta(days=7)

    weekly_totals = {}

    for tip_day_str, amount in tips:

        try:
            tip_day = date.fromisoformat(tip_day_str)
        except ValueError:
            continue

        if week_ago <= tip_day <= today:
            day_name = tip_day.strftime("%a")

            if day_name in weekly_totals:
                weekly_totals[day_name] += amount
            else:
                weekly_totals[day_name] = amount

    if not weekly_totals:
        print("No tips for last 7 days")
        return
    
    best_day_name = max(weekly_totals, key=weekly_totals.get)
    best_amount = weekly_totals[best_day_name]

    print(f"Best day of the week: {best_day_name} - {best_amount} kc")



def total_for_month():
    tips = read_tips()
    today = date.today()
    
    total = 0

    for tip_date, amount in  tips:
        tip_day = date.fromisoformat(tip_date)

        if tip_day.year == today.year and tip_day.month == today.month:
            total += amount

    print(f"Total current for month: {total}")

def show_all_tips():
    tips = read_tips()

    if not tips:
        print("No tips yet.")
        return
    
    print("\nAll tips")
    print("-" * 20)

    for tip_date, amount in tips:
        print(f"{tip_date} - {amount} kc.")

def stats_by_weekday():
    tips = read_tips()

    if not tips:
        print("No tips yet.")
        return
    weekday_totals = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0,
    }

    for tip_date_str, amount in tips:
        try:
            tip_day = date.fromisoformat(tip_date_str)
        except ValueError:
            continue

        day_name = tip_day.strftime("%a")
        weekday_totals[day_name] += amount

    print("\nTips by weekdays.")
    print("-" * 20)

    for day, total in weekday_totals.items():
        print(f"{day}: {total} kc")

def sorted_day_by_tips():
    tips = read_tips()

    if not tips:
        print("No tips yet.")
        return
    
    weekday_totals = {
        "Mon": 0,
        "Tue": 0,
        "Wed": 0,
        "Thu": 0,
        "Fri": 0,
        "Sat": 0,
        "Sun": 0,
    }

    for tip_day_str, amount in tips:
        try:
            tip_day = date.fromisoformat(tip_day_str)
        except ValueError:
            continue

        day_name = tip_day.strftime("%a")
        if day_name in weekday_totals:
            weekday_totals[day_name] += amount

    day_and_totals = list(weekday_totals.items())

    sorted_days = []

    while day_and_totals:
        max_day = day_and_totals[0]

        for item in day_and_totals:
            if item[1] > max_day[1]:
                max_day = item

        sorted_days.append(max_day)
        day_and_totals.remove(max_day)

    print("\nDays sorted by tips:")
    print("-" * 25)

    for day, total in sorted_days:
        print(f"{day}: {total} kc")



fun_comments = {
    50: "Dobre ze jsi jedl vcera",
    100: "Dneska jen rohlík 😅",
    300: "Dneska na nakup do zabky!",
    500: "Taxi domu zní reálně 🚕",
    600: "Napiš provoznímu, že zítra do prace nepřijdeš 😎"
}

def get_fun_comment(day_tips):
    for limit, comment in fun_comments.items():
        if day_tips <= limit:
            return comment
    return "Mas otevrit vlastni podnik!"


menu_actions = {
    "1": add_tips,
    "2": add_tips_for_past_day,
    "3": total_for_day,
    "4": total_for_week,
    "5": total_for_month,
    "6": show_all_tips,
    "7": best_day_of_week,
    "8": stats_by_weekday,
    "0": exit
}    

def menu():
    print("---Accounting of tips---\n")
    print("1 - Add tips")
    print("2 - Add tips for past day")
    print("3 - Tips for today")
    print("4 - Tips for a week")
    print("5 - Tips for a month")
    print("6 - Show all tips")
    print("7 - Best day of the week")
    print("8 - State by weekday")
    print("0 - Exit")

while True:
    menu()
    choice = input("Enter an item: ")

    action = menu_actions.get(choice)

    if action:
        action()
        if choice == "0":
            break

    else:
        print("Incorrect input.")
