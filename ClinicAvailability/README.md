# Exercise 2: Clinic appointment availability

Contributed by Jesse.

Suggested time: 40–50 minutes.

## Client report

A clinic administrator says the availability API sometimes shows appointment
times belonging to another clinic. They also report that cancelling a booking
does not reliably make the slot available again.

The affected endpoint is
`GET /api/clinics/<clinic-slug>/availability/?date=YYYY-MM-DD`.

## Contract

- Results contain slots for the clinic in the URL and no other clinic.
- Only `confirmed` bookings consume slot capacity.
- `pending` and `cancelled` bookings do not consume capacity.
- A slot is available while its confirmed booking count is strictly less than
  its capacity.
- Results are ordered by start time and the existing JSON shape is public API.

## Task

Use the report and tests to locate every defect responsible for the behaviour.
Make the smallest coherent fix in production code and add at least one test that
strengthens the capacity or isolation contract.

Run the suite with:

```bash
python manage.py test
```

Solutions are intentionally not stored on `main`. Create a separate branch in
your fork before making changes.
