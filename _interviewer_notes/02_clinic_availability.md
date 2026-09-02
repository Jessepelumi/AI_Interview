# Interviewer notes: Clinic appointment availability

## Intended defects

Both defects are in `scheduling/services.py` and can be fixed in one coherent ORM
query.

1. The `clinic` argument is unused, so same-day slots from every clinic are
   returned. This is a data-isolation failure, not merely a cosmetic result bug.
2. `Count("bookings")` counts every booking status, so pending and cancelled
   bookings incorrectly consume capacity. The annotation needs a filtered count
   for `Booking.Status.CONFIRMED`.

A narrow repair filters slots by `clinic=clinic` and uses `Count(...,
filter=Q(bookings__status=Booking.Status.CONFIRMED))`.

## Useful candidate-added tests

- pending bookings do not consume capacity;
- a capacity-two slot with one confirmed and several cancelled bookings reports
  one remaining place;
- one clinic's full slot does not affect another clinic's slot at the same time.

## Evaluation signals

Strong candidates notice the unused parameter, inspect the generated query or
annotation semantics, recognise tenant leakage as higher severity, and avoid
moving filtering into Python after fetching all rows.

