"""
vaccination_tracker.py - Community Vaccination Tracker (single-file version)

PROG211 Object-Oriented Programming 1 - Individual Assignment
Domain: Health (Vaccination Tracker) - follows Digital Public Goods (DPG) standards:
  open-source, inclusive/accessible, privacy-respecting (anonymous IDs only),
  modular and reusable.

HOW TO RUN IN PYCHARM:
  Right-click this file -> Run 'vaccination_tracker'.   (Python 3.6 or newer,
  standard library only - nothing to install, no other files needed.)

Sections:
  PART 1  Classes (Vaccine, Recipient)         - Task 1 and Task 3
  PART 2  Dictionary registry functions        - Task 2
  PART 3  Demonstration program                - runs when this file is executed
"""

from datetime import date, datetime, timedelta


# =============================================================================
# PART 1 - CLASSES
# =============================================================================


class Vaccine:
    """A type of vaccine together with its (immutable) dose schedule."""

    # Class variable shared by every Vaccine object.
    total_vaccines_created = 0

    # Standard catalogue stored as a TUPLE of TUPLES (immutable data).
    # Each entry: (code, name, days-after-first-dose for dose 1, 2, 3 ...)
    STANDARD_CATALOGUE = (
        ("BCG", "BCG (Tuberculosis)", (0,)),
        ("PENTA", "Pentavalent", (0, 28, 56)),
        ("MEASLES", "Measles", (0, 180)),
        ("COVID", "COVID-19", (0, 28)),
    )

    def __init__(self, code, name, dose_schedule_days):
        if not Vaccine.is_valid_code(code):
            raise ValueError("Vaccine code must be 2-10 letters or digits.")
        if not name or not name.strip():
            raise ValueError("Vaccine name cannot be empty.")
        schedule = tuple(dose_schedule_days)  # tuples cannot be changed later
        if len(schedule) == 0 or schedule[0] != 0:
            raise ValueError("Schedule must start with 0 (day of first dose).")
        if any(b <= a for a, b in zip(schedule, schedule[1:])):
            raise ValueError("Schedule days must be strictly increasing.")

        self.code = code.strip().upper()
        self.name = name.strip()
        self.dose_schedule_days = schedule
        Vaccine.total_vaccines_created += 1

    # ---------------- instance methods ----------------
    def doses_required(self):
        """Return how many doses make a person fully vaccinated."""
        return len(self.dose_schedule_days)

    def display_info(self):
        """Print a readable summary of this vaccine."""
        print(f"Vaccine {self.code}: {self.name}")
        print(f"  Doses required : {self.doses_required()}")
        print(f"  Schedule (days after dose 1): {self.dose_schedule_days}")

    # ---------------- class methods ----------------
    @classmethod
    def from_standard(cls, code):
        """Create a Vaccine from the built-in standard catalogue."""
        wanted = code.strip().upper()
        for std_code, name, schedule in cls.STANDARD_CATALOGUE:
            if std_code == wanted:
                return cls(std_code, name, schedule)
        raise ValueError(f"'{code}' is not in the standard catalogue.")

    @classmethod
    def count_created(cls):
        """Return how many Vaccine objects have been created so far."""
        return cls.total_vaccines_created

    # ---------------- static methods ----------------
    @staticmethod
    def is_valid_code(code):
        """A valid code is 2-10 letters/digits (no spaces). Needs no object."""
        return isinstance(code, str) and code.strip().isalnum() and 2 <= len(code.strip()) <= 10


class Recipient:
    """An ANONYMOUS person receiving vaccines (privacy by design)."""

    AGE_GROUPS = ("infant", "child", "adolescent", "adult")  # immutable tuple
    _next_number = 1  # used to generate anonymous IDs

    def __init__(self, recipient_id, age_group, district):
        if not Recipient.is_valid_age_group(age_group):
            raise ValueError(f"Age group must be one of {Recipient.AGE_GROUPS}.")
        if not district or not district.strip():
            raise ValueError("District cannot be empty.")

        self.recipient_id = recipient_id
        self.age_group = age_group.strip().lower()
        self.district = district.strip().title()
        # Private (encapsulated): a tuple of dose records. Each record is the
        # tuple (vaccine_code, dose_number, "YYYY-MM-DD"). Tuples are immutable,
        # so a record cannot be altered after it has been written.
        self._doses = ()

    # ---------------- read-only access (encapsulation) ----------------
    @property
    def doses(self):
        """All dose records for this recipient (read-only tuple)."""
        return self._doses

    # ---------------- instance methods ----------------
    def doses_of(self, vaccine_code):
        """Count doses already received of one vaccine."""
        return sum(1 for record in self._doses if record[0] == vaccine_code)

    def is_fully_vaccinated(self, vaccine):
        """True when all required doses of `vaccine` have been received."""
        return self.doses_of(vaccine.code) >= vaccine.doses_required()

    def _first_dose_date(self, vaccine_code):
        for code, dose_number, iso_date in self._doses:
            if code == vaccine_code and dose_number == 1:
                return datetime.strptime(iso_date, "%Y-%m-%d").date()
        return None

    def receive_dose(self, vaccine, date_given=None):
        """
        Record a dose of `vaccine` (interaction between two objects).

        Returns a tuple (success, message). Nothing is recorded when the dose
        is not allowed (already complete, or given too early).
        """
        if date_given is None:
            date_given = date.today()

        taken = self.doses_of(vaccine.code)
        if taken >= vaccine.doses_required():
            return False, f"{self.recipient_id}: already completed {vaccine.code}."

        if taken > 0:
            first = self._first_dose_date(vaccine.code)
            earliest = first + timedelta(days=vaccine.dose_schedule_days[taken])
            if date_given < earliest:
                return False, (f"{self.recipient_id}: dose {taken + 1} of {vaccine.code} "
                               f"is too early (earliest {earliest.isoformat()}).")

        self._doses = self._doses + ((vaccine.code, taken + 1, date_given.isoformat()),)
        return True, (f"{self.recipient_id}: {vaccine.code} dose {taken + 1} of "
                      f"{vaccine.doses_required()} recorded on {date_given.isoformat()}.")

    def update_record(self, age_group=None, district=None):
        """Update the age group and/or district of this recipient."""
        if age_group is not None:
            if not Recipient.is_valid_age_group(age_group):
                raise ValueError(f"Age group must be one of {Recipient.AGE_GROUPS}.")
            self.age_group = age_group.strip().lower()
        if district is not None:
            if not district.strip():
                raise ValueError("District cannot be empty.")
            self.district = district.strip().title()

    def display_info(self):
        """Print a readable summary of this recipient."""
        print(f"Recipient {self.recipient_id} | {self.age_group.title()} | {self.district}")
        if not self._doses:
            print("  No doses recorded yet.")
        for code, dose_number, iso_date in self._doses:
            print(f"  - {code} dose {dose_number} on {iso_date}")

    # ---------------- class methods ----------------
    @classmethod
    def register(cls, age_group, district):
        """Create a Recipient with an auto-generated anonymous ID (R-0001...)."""
        new_id = f"R-{cls._next_number:04d}"
        recipient = cls(new_id, age_group, district)  # raises before the counter moves
        cls._next_number += 1
        return recipient

    @classmethod
    def total_registered(cls):
        """How many anonymous recipients have been registered so far."""
        return cls._next_number - 1

    # ---------------- static methods ----------------
    @staticmethod
    def is_valid_age_group(age_group):
        """Check an age group string without needing an object."""
        return isinstance(age_group, str) and age_group.strip().lower() in Recipient.AGE_GROUPS


# =============================================================================
# PART 2 - REGISTRY (ONE DATA STRUCTURE: A DICTIONARY, KEY = RECIPIENT ID)
# =============================================================================
def add_record(registry, recipient):
    """Add a Recipient to the registry. Returns False if the ID already exists."""
    if recipient.recipient_id in registry:
        print(f"Cannot add: ID {recipient.recipient_id} already exists.")
        return False
    registry[recipient.recipient_id] = recipient
    return True


def display_records(registry):
    """Loop through the registry and display every recipient."""
    if not registry:
        print("The registry is empty.")
        return
    for recipient_id, recipient in registry.items():
        recipient.display_info()


def find_record(registry, recipient_id):
    """Return the Recipient with this ID, or None if not found."""
    return registry.get(recipient_id)


def coverage_report(registry, vaccine):
    """Print how many recipients are fully vaccinated against `vaccine`."""
    total = len(registry)
    done = sum(1 for r in registry.values() if r.is_fully_vaccinated(vaccine))
    percent = (done / total * 100) if total else 0.0
    print(f"{vaccine.code} coverage: {done}/{total} fully vaccinated ({percent:.1f}%)")


# =============================================================================
# PART 3 - DEMONSTRATION PROGRAM
# =============================================================================



def heading(text):
    print()
    print("=" * 60)
    print(text)
    print("=" * 60)


def main():
    # ------------------------------------------------------------------
    # Task 1: object creation
    # ------------------------------------------------------------------
    heading("1. Creating Vaccine objects (class method + constructor)")
    penta = Vaccine.from_standard("penta")          # class method
    measles = Vaccine.from_standard("MEASLES")      # class method
    custom = Vaccine("YF", "Yellow Fever", (0,))    # normal constructor
    for vaccine in (penta, measles, custom):
        vaccine.display_info()
    print(f"Vaccine objects created so far: {Vaccine.count_created()}")
    print(f"Is 'A B' a valid code? {Vaccine.is_valid_code('A B')}")  # static method

    # ------------------------------------------------------------------
    # Task 2: one data structure (dictionary) + add / display functions
    # ------------------------------------------------------------------
    heading("2. Registering anonymous recipients in the dictionary")
    registry = {}
    profiles = (
        ("infant", "Western Area Urban"),
        ("child", "Bo"),
        ("adult", "Kenema"),
        ("infant", "Port Loko"),
    )
    for age_group, district in profiles:
        recipient = Recipient.register(age_group, district)  # class method
        add_record(registry, recipient)
    print(f"Total registered: {Recipient.total_registered()}")

    duplicate = Recipient("R-0001", "adult", "Bombali")
    add_record(registry, duplicate)  # rejected: duplicate ID

    # ------------------------------------------------------------------
    # Task 1 + 3: interaction between objects (instance methods)
    # ------------------------------------------------------------------
    heading("3. Recording doses (Recipient interacts with Vaccine)")
    infant_1 = find_record(registry, "R-0001")
    infant_2 = find_record(registry, "R-0004")
    child = find_record(registry, "R-0002")

    messages = [
        infant_1.receive_dose(penta, date(2026, 1, 5)),
        infant_1.receive_dose(penta, date(2026, 1, 10)),   # too early
        infant_1.receive_dose(penta, date(2026, 2, 2)),    # dose 2 (day 28)
        infant_1.receive_dose(penta, date(2026, 3, 2)),    # dose 3 (day 56)
        infant_1.receive_dose(penta, date(2026, 6, 1)),    # already complete
        infant_2.receive_dose(penta, date(2026, 1, 15)),
        child.receive_dose(measles, date(2026, 2, 1)),
        child.receive_dose(custom, date(2026, 2, 1)),
    ]
    for success, message in messages:
        print(("[OK]     " if success else "[REJECT] ") + message)

    # ------------------------------------------------------------------
    # Task 3: update_record() instance method
    # ------------------------------------------------------------------
    heading("4. Updating a record")
    infant_2.update_record(district="Kambia")
    print(f"R-0004 district is now: {infant_2.district}")
    try:
        infant_2.update_record(age_group="teenager")  # invalid on purpose
    except ValueError as error:
        print(f"Validation works -> {error}")

    # ------------------------------------------------------------------
    # Display all records and a summary
    # ------------------------------------------------------------------
    heading("5. All records in the registry")
    display_records(registry)

    heading("6. Coverage summary")
    coverage_report(registry, penta)
    coverage_report(registry, measles)
    coverage_report(registry, custom)

    heading("7. Looking up a missing ID")
    missing = find_record(registry, "R-9999")
    print("Result:", missing if missing is not None else "No record found for R-9999.")


if __name__ == "__main__":
    main()
