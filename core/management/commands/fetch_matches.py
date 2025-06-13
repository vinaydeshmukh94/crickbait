from django.core.management.base import BaseCommand
import requests, logging
from matches.models import Match
from decouple import config
from datetime import datetime
from bets.models import Bet


x_rapid_api_key = config("x_RapidAPI_KEY")
x_rapid_api_host = config("x_RapidAPI_HOST")


def get_current_ipl_series_id():
    url = "https://cricbuzz-cricket.p.rapidapi.com/series/v1/league"
    headers = {"x-rapidapi-key": x_rapid_api_key, "x-rapidapi-host": x_rapid_api_host}
    response = requests.get(url, headers=headers)
    for item in response.json().get("seriesMapProto", []):
        for series in item.get("series", []):
            if "Indian Premier League" in series["name"]:
                print(series["id"])
                return series["id"]
    return None


class Command(BaseCommand):
    help = "Fetch and store current IPL matches"

    def update_bets_table(self, match_info, match, match_date):
        # Check if match has completed
        winning_point = 1
        losing_point = 0
        if (
            match_info["state"].lower() == "complete"
        ):  # Or however 'completed' is represented
            # Adjust key to actual structure
            winning_team_id = ""
            if match_info["team1"]["teamName"] in match_info["status"]:
                winning_team_id = "team1"
                losing_team_id = "team2"
            if match_info["team2"]["teamName"] in match_info["status"]:
                winning_team_id = "team2"
                losing_team_id = "team1"
            if winning_team_id and losing_team_id:
                winning_update_count = Bet.objects.filter(
                    match=match, chosen_team=winning_team_id, created_at__lt=match_date
                ).update(is_correct=True, points_awarded=winning_point)
                losing_update_count = Bet.objects.filter(
                    match=match, chosen_team=losing_team_id, created_at__lt=match_date
                ).update(is_correct=False, points_awarded=losing_point)
                logging.info(
                    f" -{match.id}, winning-update-{winning_update_count}, losing-update-{losing_update_count}"
                )

    def handle(self, *args, **kwargs):
        series_id = get_current_ipl_series_id()
        if not series_id:
            self.stdout.write(self.style.ERROR("IPL Series ID not found"))
            return

        url = f"https://cricbuzz-cricket.p.rapidapi.com/series/v1/{series_id}"
        headers = {
            "x-rapidapi-key": x_rapid_api_key,
            "x-rapidapi-host": x_rapid_api_host,
        }
        response = requests.get(url, headers=headers)
        print("==" * 20)
        print(response)
        data = response.json()
        count = 0

        for match_data in data.get("matchDetails", []):
            date_string = match_data.get("matchDetailsMap", {}).get("key", "")
            for match_info in match_data.get("matchDetailsMap", {}).get("match", []):
                date_obj = datetime.strptime(date_string, "%a, %d %b %Y").date()
                m = match_info["matchInfo"]
                match, _ = Match.objects.update_or_create(
                    match_id=m["matchId"],
                    series_id=m["seriesId"],
                    date=date_obj,
                    defaults={
                        "team1sname": m["team1"]["teamSName"],
                        "team2sname": m["team2"]["teamSName"],
                        "state": m["state"],
                        "status": m["status"],
                        "team1name": m["team1"]["teamName"],
                        "team2name": m["team2"]["teamName"],
                    },
                )
                self.update_bets_table(match_info=m, match=match, match_date=date_obj)
                count += 1

        self.stdout.write(self.style.SUCCESS(f"Fetched and updated {count} matches"))
