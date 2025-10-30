
import csv
import os

def toon_gebruikersinterface():
    """Display the user interface menu."""
    print("\nPersonen Beheer Systeem")
    print("=" * 20)
    print("1. Namen naar hoofdletters")
    print("2. Nieuwe persoon toevoegen")
    print("3. Personen verwijderen")
    print("4. Overzicht van alle personen")
    print("0. Programma stoppen")
    print("=" * 20)

def convert_names_to_uppercase():
    """Convert names to uppercase following the flowchart."""
    try:
        # Open CSV bestand
        with open('lijst.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # Zet regel om naar hoofdletters
        for person in data:
            # Convert first three fields (names) to uppercase
            for i in range(min(3, len(person))):
                person[i] = person[i].upper()
        
        # Schrijf csv bestand
        with open('lijst.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        
        print("Alle namen zijn naar hoofdletters omgezet.")
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def validate_postcode(postcode):
    """Validate Dutch postal code format (1234 AB)."""
    # Remove any extra spaces and convert to uppercase
    postcode = postcode.strip().upper()
    
    # Check basic format (4 digits followed by 2 letters)
    if len(postcode) < 6:
        return False, "Postcode moet 4 cijfers en 2 letters bevatten"
    
    # Split numeric and alphabetic parts
    numeric = postcode[:4]
    alpha = postcode[-2:] if len(postcode) >= 6 else ""
    
    # Check if first part is 4 digits between 1000 and 9999
    if not (numeric.isdigit() and 1000 <= int(numeric) <= 9999):
        return False, "Postcode moet beginnen met 4 cijfers tussen 1000 en 9999"
    
    # Check if last part is 2 letters
    if not (len(alpha) == 2 and alpha.isalpha()):
        return False, "Postcode moet eindigen met 2 letters"
    
    return True, postcode

def validate_address(address):
    """Validate street address format."""
    # Remove extra spaces
    address = address.strip()
    
    # Check minimum length
    if len(address) < 3:
        return False, "Adres is te kort"
    
    # Check if address contains a street name and house number
    parts = address.split()
    if len(parts) < 2:
        return False, "Adres moet een straatnaam en huisnummer bevatten"
    
    # Check if at least one part is a number (house number)
    has_number = any(part.replace('/', '').isdigit() for part in parts)
    if not has_number:
        return False, "Adres moet een huisnummer bevatten"
    
    return True, address

def add_new_person():
    """Add a new person following the flowchart."""
    try:
        # Open CSV bestand
        with open('lijst.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        while True:
            # Vraag gebruiker om nieuwe gegevens in te voeren
            print("\nVoer de gegevens van de nieuwe persoon in:")
            voornaam = input("Voornaam: ").strip()
            tussenvoegsel = input("Tussenvoegsel (laat leeg indien niet van toepassing): ").strip()
            achternaam = input("Achternaam: ").strip()
            
            # Adres validatie
            while True:
                adres = input("Adres (straatnaam + huisnummer): ").strip()
                is_valid, message = validate_address(adres)
                if is_valid:
                    break
                print(f"Ongeldig adres: {message}")
            
            # Postcode validatie
            while True:
                postcode = input("Postcode (1234 AB): ").strip()
                is_valid, message = validate_postcode(postcode)
                if is_valid:
                    postcode = message  # Use formatted postcode
                    break
                print(f"Ongeldige postcode: {message}")
            
            woonplaats = input("Woonplaats: ").strip()
            
            # Check gegevens juist ingevoerd
            if not all([voornaam, achternaam, woonplaats]):
                print("Niet alle verplichte velden zijn ingevuld! Probeer het opnieuw.")
                continue
            
            # Schrijf gegevens weg in csv bestand
            new_person = [voornaam, tussenvoegsel, achternaam, adres, postcode, woonplaats]
            data.append(new_person)
            
            with open('lijst.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(data)
            
            print("\nNieuwe persoon is toegevoegd.")
            return True
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def remove_person():
    """Remove a person following the flowchart."""
    try:
        # Open CSV bestand
        with open('lijst.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        if not data:
            print("Er zijn geen personen om te verwijderen.")
            return False
        
        while True:
            # Toon overzicht van alle regels uit het bestand
            print("\nKies een persoon om te verwijderen:")
            for i, person in enumerate(data, 1):
                print(f"{i}. {person[0]} {person[1]} {person[2]}")
            
            # Vraag gebruiker welke regel hij wil verwijderen
            try:
                choice = int(input("\nVoer het nummer in van de persoon die u wilt verwijderen (0 om te annuleren): "))
                
                # Check invoer correct
                if choice == 0:
                    print("Verwijderen geannuleerd.")
                    return False
                
                if not (1 <= choice <= len(data)):
                    print("Ongeldige keuze! Probeer het opnieuw.")
                    continue
                
                # Verwijder regel
                removed_person = data.pop(choice - 1)
                
                # Schrijf gegevens weg in csv bestand
                with open('lijst.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(data)
                
                print(f"Persoon '{removed_person[0]} {removed_person[1]} {removed_person[2]}' is verwijderd.")
                return True
            except ValueError:
                print("Ongeldige invoer! Voer een nummer in.")
                continue
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def show_all_persons():
    """Show all persons following the flowchart."""
    try:
        # Open CSV bestand
        with open('lijst.csv', 'r') as file:
            reader = csv.reader(file)
            data = list(reader)
        
        # Toon overzicht van alle regels uit het bestand
        if not data:
            print("Er zijn geen personen in de lijst.")
            return False
            
        print("\nOverzicht van alle personen:")
        print("-" * 80)
        for person in data:
            name = f"{person[0]} {person[1]} {person[2]}".strip()
            address = f"{person[3]}, {person[4]}, {person[5]}"
            print(f"Naam: {name:<40} Adres: {address}")
        print("-" * 80)
        return True
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def main():
    """Main program loop following the flowchart."""
    while True:
        try:
            # Clear screen for better readability
            os.system('cls' if os.name == 'nt' else 'clear')
            
            # Toon gebruikersinterface
            toon_gebruikersinterface()
            
            choice = input("\nMaak uw keuze (0-4): ")
            
            if choice == "1":
                convert_names_to_uppercase()
            elif choice == "2":
                add_new_person()
            elif choice == "3":
                remove_person()
            elif choice == "4":
                show_all_persons()
            elif choice == "0":
                print("\nBedankt voor het gebruiken van het programma. Tot ziens!")
                break
            else:
                print("\nOngeldige keuze! Kies een nummer tussen 0 en 4.")
            
            input("\nDruk op Enter om door te gaan...")
        except Exception as e:
            print(f"\nEr is een fout opgetreden: {str(e)}")
            input("\nDruk op Enter om door te gaan...")

if __name__ == "__main__":
    main()