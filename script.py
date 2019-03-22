import json
import csv
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta

DATE_PARSE = '%Y-%m-%dT%H:%M:%SZ'

TIMEDELTA = relativedelta(months=1)

GATHER = ['commits'] # ['pullRequests', 'commitComments', 'issues', 'issueComments']
CUMULATIVE = True

with open('orbit-db-contribs.json') as json_data:
    d = json.load(json_data)
    with open('contribs.csv', 'w', newline='') as csvfile:

      objects = []

      # get all objects (prs, issues, comments) sorted by date
      for repository in d['organization']['repositories']:
        for obj_type in GATHER:
          if obj_type != 'commits':
            for obj in repository[obj_type]:
              objects.append((repository['name'], obj_type, obj['author']['name'] if obj['author'] else 'None', obj['createdAt']))

        if 'commits' in GATHER:
          for obj in repository['ref']['target']['history']:
            objects.append((repository['name'], 'commits', obj['author']['user']['name'] if obj['author'] and obj['author']['user'] else 'None', obj['committedDate']))

      sorted_objects = sorted(objects, key=lambda object: object[3])

      # get first & last date
      first = datetime.strptime(sorted_objects[0][3], DATE_PARSE)
      last = datetime.strptime(sorted_objects[-1][3], DATE_PARSE)

      # get first day of week
      current_date = first - timedelta(days=first.weekday())

      # go through weeks from first date and push all objects to it
      start_index = 0

      by_weeks = []

      while current_date <= last:
        next_week = current_date + TIMEDELTA

        objects_this_week = []
        if CUMULATIVE and len(by_weeks) > 0:
          objects_this_week = by_weeks[-1]['objects'][:]

        for obj in sorted_objects[start_index:]:
          obj_date = datetime.strptime(obj[3], DATE_PARSE)
          if obj_date < next_week and obj_date >= current_date:
            objects_this_week.append(obj)

          if obj_date >= next_week:
            break
          start_index += 1

        by_weeks.append({
          'week': current_date,
          'objects': objects_this_week
        })
        current_date = next_week

      contribswriter = csv.writer(csvfile, quotechar='|', quoting=csv.QUOTE_MINIMAL)
      contribswriter.writerow(['week', 'contributions'])
      for week in by_weeks:
        contribswriter.writerow([week['week'], len(week['objects'])])

print('done')