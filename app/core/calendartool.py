import datetime
import cherrypy
from calendar import monthrange
from faker import Faker
from app.core.tools import get_date_number
from collections import namedtuple

from app.models.event import Event
from app.models.members import Members
from app.models.participant import Participant
from app.models.usergroup import UserGroup

MONTH = [
    "",
    "Jan",
    "Fev",
    "Mar",
    "Avr",
    "Mai",
    "Jun",
    "Jul",
    "Aou",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]

Day = namedtuple("Day", ["number", "month", "events", "is_today", "year"])


def getCalender(**post):
    events = Event().get_all(id_user=cherrypy.session.get("id_user"))
    participations = Participant().get_all(id_user=cherrypy.session.get("id_user"))
    participations_id = {}
    for participation in participations:
        participations_id[participation["id_event"]] = participation
    groups_id = Members().get_all(id_user=cherrypy.session.get("id_user"))
    userGroups = []
    for group in groups_id:
        userGroups.append(UserGroup().get(id=group["id_group"]))
    for group in userGroups:
        events += Event().get_all(id_group=group.id)
    # Clear doublon
    events_cleared = []
    present_id = []
    print(participations_id)
    for event in events:
        if event.id not in present_id and (
            event.id in participations_id
            or event["id_user"] == cherrypy.session.get("id_user")
        ):
            if event["id_user"] == cherrypy.session.get("id_user"):
                event.is_participating = True
                present_id.append(event.id)
                events_cleared.append(event)
                continue
            if participations_id[event.id]["is_participating"] == 2:
                continue
            if participations_id[event.id]["is_participating"] == 1:
                event.is_participating = True
            else:
                event.is_participating = False
            present_id.append(event.id)
            events_cleared.append(event)

    events = events_cleared
    val = {}
    date = None
    current_month = False
    if not "year" in post and not "month" in post:
        date = datetime.datetime.now()
    else:
        if int(post["year"]) > datetime.datetime.now().year + 1:
            date = datetime.datetime.now()
        else:
            date = datetime.datetime(int(post["year"]), int(post["month"]), 1)
    if (
        date.month == datetime.datetime.now().month
        and date.year == datetime.datetime.now().year
    ):
        current_month = True
    # Mise en place des variables
    val["year"] = date.year
    val["n_year"] = date.year
    val["p_year"] = date.year
    val["month"] = MONTH[date.month]
    val["month_nb"] = date.month
    val["month_p"] = date.month - 1
    val["month_n"] = date.month + 1
    # Check fin ou debut années
    if val["month_p"] == 0:
        val["month_p"] = 12
    if val["month_nb"] == 1:
        val["p_year"] = date.year - 1
    if val["month_nb"] == 12:
        val["n_year"] = date.year + 1
    if val["month_n"] == 13:
        val["month_n"] = 1
    # Construction du calendrier
    first_month_day = datetime.datetime(date.year, date.month, 1)
    old_month_showed_day = first_month_day.weekday()
    old_month_nb_day = monthrange(date.year, val["month_p"])[1]
    lines = []
    c_line = []
    # Premiere ligne ( mois précédent + mois actuel )
    for i in range(-old_month_showed_day + 1, 1):
        c_line.append(
            Day(
                get_date_number(date.year, date.month - 1, old_month_nb_day + i),
                MONTH[val["month_p"]],
                get_event(
                    events,
                    get_date_number(date.year, date.month - 1, old_month_nb_day + i),
                    MONTH[val["month_p"]],
                    val["year"],
                ),  # Load event here
                False,
                val["year"],
            )
        )
    for i in range(0, 7 - old_month_showed_day):
        c_line.append(
            Day(
                i + 1,
                MONTH[date.month],
                get_event(events, i + 1, MONTH[date.month], val["year"]),
                i + 1 == datetime.datetime.now().day and current_month,
                val["year"],
            )
        )  # Load event here
    lines.append(c_line)
    # Lignes suivantes
    c_line = []
    i = 8 - old_month_showed_day
    while i <= monthrange(date.year, date.month)[1]:
        c_line.append(
            Day(
                i,
                MONTH[date.month],
                get_event(events, i, MONTH[date.month], val["year"]),
                i == datetime.datetime.now().day and current_month,
                val["year"],
            )
        )  # Load event here
        if len(c_line) == 7:
            lines.append(c_line)
            c_line = []
        i += 1
    # Fin du calendrier ( mois suivant )
    nb_month_next = 7 - len(c_line)
    for i in range(1, nb_month_next + 1):
        c_line.append(
            Day(
                i,
                MONTH[val["month_n"]],
                get_event(events, i + 1, MONTH[val["month_n"]], val["year"]),
                False,
                val["year"],
            )
        )  # Load event here
    lines.append(c_line)
    val["lines"] = lines
    return val


def get_event(events, day, month, year):
    month = MONTH.index(month)
    event = []
    for e in events:
        if (
            e["date_meeting"].day == day
            and e["date_meeting"].month == month
            and e["date_meeting"].year == year
        ):
            e.has_passed = e["date_meeting"] < datetime.datetime.now()
            event.append(e)
    return event
