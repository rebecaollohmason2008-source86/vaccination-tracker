# Community Vaccination Tracker

A small, open-source Python program that tracks vaccine doses for anonymous
recipients. Built for **PROG211 Object-Oriented Programming 1** (Limkokwing University of Creative Technology, Sierra Leone) under the assignment
*Real-World Solutions under DPG Standards*.

- **Domain:** Health
- **Problem:** Health workers need a simple way to record which vaccine doses a
  person has received, check that doses follow the correct schedule, and see
  how many people are fully vaccinated, without storing sensitive personal data.

## Project structure

| File | Purpose |
|------|---------|
| `vaccination_tracker.py` | The whole program in one file: Part 1 `Vaccine` and `Recipient` classes, Part 2 dictionary registry functions, Part 3 demonstration |
| `output.txt` | Sample output of a run |
| `LICENSE` | MIT open-source licence |

## How to run

Requires **Python 3.6 or newer**. No external packages are needed.

```bash
python vaccination_tracker.py
```

In PyCharm: open the folder, right-click `vaccination_tracker.py`, then choose **Run 'vaccination_tracker'**.

## How the solution aligns with Digital Public Goods (DPG) standards

| DPG principle | How this project meets it |
|---------------|---------------------------|
| **Open-source** | Published on GitHub under the MIT licence, so anyone can use, study, modify and share it. |
| **Inclusive and accessible** | Plain-language messages, no special hardware, standard library only, works on any computer with Python and is easy to translate. |
| **Privacy-respecting** | No names, phone numbers, addresses or dates of birth are stored. A person is only an anonymous ID (`R-0001`), a broad age group and a district. Dose records are immutable tuples. |
| **Modular and reusable** | Data classes (Part 1), storage functions (Part 2) and the demo (Part 3) are separate sections, so the classes can be reused in a web, mobile or database-backed system. |

## OOP concepts used

- **Classes and objects:** `Vaccine` and `Recipient`, with attributes and methods.
- **Interaction between objects:** `Recipient.receive_dose(vaccine)` uses a `Vaccine` object to check the schedule.
- **Data structures:** a **dictionary** stores all recipients by ID; **tuples** hold the immutable vaccine schedules and dose records.
- **Instance methods:** `receive_dose()`, `update_record()`, `display_info()`, `doses_of()`, `is_fully_vaccinated()`.
- **Class methods (`@classmethod`):** `Vaccine.from_standard()`, `Vaccine.count_created()`, `Recipient.register()`, `Recipient.total_registered()`.
- **Static methods (`@staticmethod`):** `Vaccine.is_valid_code()`, `Recipient.is_valid_age_group()`.
- **Encapsulation:** dose records are kept in a private `_doses` attribute exposed through a read-only `@property`.

## Example usage

```python
# Place this in a new file next to vaccination_tracker.py
from datetime import date
from vaccination_tracker import Recipient, Vaccine, add_record, display_records

registry = {}
penta = Vaccine.from_standard("PENTA")
person = Recipient.register("infant", "Bo")      # gets ID R-0001
add_record(registry, person)

print(person.receive_dose(penta, date(2026, 1, 5)))
display_records(registry)
```

### Sample output (`python vaccination_tracker.py`, shortened)

```
Vaccine PENTA: Pentavalent
  Doses required : 3
  Schedule (days after dose 1): (0, 28, 56)

[OK]     R-0001: PENTA dose 1 of 3 recorded on 2026-01-05.
[REJECT] R-0001: dose 2 of PENTA is too early (earliest 2026-02-02).
[OK]     R-0001: PENTA dose 2 of 3 recorded on 2026-02-02.
[OK]     R-0001: PENTA dose 3 of 3 recorded on 2026-03-02.
[REJECT] R-0001: already completed PENTA.

PENTA coverage: 1/4 fully vaccinated (25.0%)
```

The full output is in `output.txt`.

## Author

Replace with your name and student ID.

## Licence

Released under the MIT Licence. See `LICENSE`.
