# events/management/commands/import_participants.py
import csv
from django.core.management.base import BaseCommand
from events.models import Participant, Event
from django.db import IntegrityError


class Command(BaseCommand):
    help = "Import participants from a CSV file by email and update their points and streaks."

    def add_arguments(self, parser):
        # Argument for the CSV file path
        parser.add_argument("csv_file", type=str, help="The path to the CSV file")

    def handle(self, *args, **kwargs):
        # Get the CSV file path from arguments
        csv_file = kwargs["csv_file"]

        try:
            with open(csv_file, mode="r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    # Check if required columns are present
                    if "event_id" not in row or "email" not in row:
                        self.stdout.write(
                            self.style.ERROR("Missing required columns in CSV")
                        )
                        continue

                    # Get event by event_id
                    event_id = row["event_id"]
                    try:
                        event = Event.objects.get(event_id=event_id)
                    except Event.DoesNotExist:
                        self.stdout.write(
                            self.style.ERROR(f"Event with ID {event_id} does not exist")
                        )
                        continue

                    # Check if participant exists by email
                    try:
                        participant, created = Participant.objects.get_or_create(
                            event=event, email=row["email"]
                        )

                        if created:
                            # Set default name if new participant
                            participant.name = row["email"].split("@")[0]
                            participant.save()

                        # Update points and streak for the participant
                        participant.participate_in_event()

                    except IntegrityError as e:
                        self.stdout.write(self.style.ERROR(f"Integrity error: {e}"))

                self.stdout.write(
                    self.style.SUCCESS(
                        "Successfully added/updated participants and their points/streaks"
                    )
                )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File not found: {csv_file}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"An unexpected error occurred: {e}"))
