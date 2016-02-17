#!/usr/bin/env python
# -*- coding: UTF-8 -*-#
#
# Copyright (C) 2014 The University of Sydney
# This file is part of the data2u toolkit

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor
# Boston, MA  02110-1301, USA.
#
# Author: Abelardo Pardo (abelardo.pardo@sydney.edu.au)
#
import datetime
import pytz
import json
import itertools

from django.conf import settings
from django.utils import timezone
from django.db.models import F

import accumulate.process
import leco.views
import leco.models
import data2u


class Handler(accumulate.HandlerBasic):
    # Name of the context with which the events are captured
    context_name = 'ELEC1601'

    # Context object in the database
    context_obj = None

    # Define the timezone
    this_timezone = pytz.timezone('Australia/Sydney')

    # Monday midnight of the first day of the semester
    first_timeline = datetime.datetime(2015, 07, 27, tzinfo = this_timezone)

    # Offset for the lecture
    lec_offset = datetime.timedelta(4, 0, 0, 0, 0, 12)

    # Days that separate each week (starting from Week 2
    weekly_steps = [
        0,  # Week 1
        7,  # Week 2
        14,  # Week 3
        21,  # Week 4
        28,  # Week 5
        35,  # Week 6
        42,  # Week 7
        49,  # Week 8
        56,  # Week 9
        70,  # Week 10
        77,  # Week 11
        84,  # Week 12
        91  # Week 13
    ]

    timeline_lec = [first_timeline + lec_offset + datetime.timedelta(x, 0, 0)
                    for x in weekly_steps]

    course_url = '/elec1601/index.html'
    course_url_text = 'Weeks'

    # Format for the Weekly information tuple
    #
    # ( [(activity-label, video_id, number of EQTs),...], # VIDEOS
    #   [(label, number of EQTs),...], # EQTs
    #   ['Problem_sequence',...] # EXCO
    # )
    units_lec = [
        #
        # Week 01
        #
        ([],  # Videos (activity-label, video id in youtube, number of EQTs)
         [],  # EQTs from other activities (no video) (label, number of EQTs)
         [],  # Problem sequence 'sequence_ID'
         ),  # End of Week 01

        #
        # Week 02
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('COD-baseencoding-videoeqt', 'U6d_MsDk2R8', 6),
             ('COD-naturalencoding-videoeqt', '6h0cM-ASXGc', 0),
             ('COD-integerencoding-videoeqt', 'SeoW3YNo3Zs', 5)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('COD-encodereals-section', 4),
             ('COD-realrangeaccuracyprecision-subsection', 2),
             ('COD-overflow-subsection', 2)
         ],
         [  # Problem sequence 'sequence_ID'
             'COD-exco-C',  # Sequence name, num of questions
         ]
         ),  # End of Lecture

        #
        # Week 03
        #
        ([  # Videos
             ('COD-symbolencoding-videoeqt', 'D3A3YMYC094', 5),
             ('DRM-structureoperations-videoeqt', 'F0Ri2TpRBBg', 5),
             ('DRM-tables-videoeqt', 'zOe8r08_F8E', 5),
             ('DRM-indirection-videoeqt', 'ZlXur4yUiBM', 5)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video)
             ('DRM-storagebooleans-subsection', 2),
             ('DRM-storagecharacters-subsection', 2),
             ('DRM-storageintegers-subsection', 2),
             ('DRM-storageinstructions-subsection', 2),
             ('DRM-storageoperationsize-subsection', 2)
         ],
         [  # Problem sequences
             'DRM-exco-C'  # Sequence name
         ]
         ),  # End of Lecture

        #
        # Week 04
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('CDL-soppos-videoeqt', 'Gjsfx-o7nnQ', 4),
             ('CDL-logicgates-videoeqt', 'LBs2ybCYu_E', 4),
             ('CDL-frombooleanexpressiontocircuit-videoeqt', 'cblZ7Rdaxog', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('CDL-designcriteria-section', 2)
         ],
         [  # Problem sequence 'sequence_ID'
             'CDL-exco-C'  # Sequence name
         ]
         ),  # End of Lecture

        #
        # Week 05
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('SDL-fsmsummary-videoeqt', 'hJIST1cEf6A', 4),
             ('SDL-fsmtocircuit-videoeqt', 'Z4Zz7n-Lj0g', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('SDL-levelsensitivecircuits-subsection', 2),
             ('SDL-edgesensitivecircuits-subsection', 2),
             ('SDL-summarysensitivecircuits-subsection', 2)
         ],
         [  # Problem sequence 'sequence_ID'
             'SDL-exco-C'
         ]
         ),  # End of Lecture

        #
        # Week 06
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
         ],
         [  # Problem sequence 'sequence_ID'
         ]
         ),  # End of Lecture

        #
        # Week 07
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('ARC-avr8architecture-videoeqt', 'itYs-vz-E08', 4),
             ('ARC-executioncycle-videoeqt', 'lJAy02h1aLs', 4),
             ('ARC-stack-videoeqt', 'd-2Peb3pCBg', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('ARC-programdatamemories-subsection', 5),
             ('ARC-generalpurposeregisters-subsection', 4)
         ],
         [  # Problem sequence 'sequence_ID'
             'ARC-exco-C'
         ]
         ),  # End of Lecture

        #
        # Week 08
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('ISA-ciscrisc-videoeqt', 'mDrUkjOVtAU', 4),
             ('ISA-encoding-videoeqt', 'Gfkq3p-7lgY', 4),
             ('ISA-subsetsummary-videoeqt', 'NxXrBQcZoSc', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('ISA-assemblylanguage-section', 8)
         ],
         [  # Problem sequence 'sequence_ID'
             'ISA-exco-C'
         ]
         ),  # End of Lecture

        #
        # Week 09
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('ASP-createprogram-videoeqt', 'nlyXUAr4134', 4),
             ('ASP-datalabelstackregister-videoeqt', 'FmvGwVojt8Q', 4),
             ('ASP-asmexample-videoeqt', 'l6WvMiiVANM', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('ASP-guidelines-section', 3)
         ],
         [  # Problem sequence 'sequence_ID'
             'ASP-exco-C'
         ]
         ),  # End of Lecture

        #
        # Week 10
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('ADM-regdirindir-videoeqt', 'GWN_VZM6Tfs', 5),
             ('ADM-indirprepostdisp-videoeqt', 'q19ikSIYFzI', 4)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('ADM-immediate-subsection', 3)
         ],
         [  # Problem sequence 'sequence_ID'
             'ADM-exco-C'
         ]
         ),  # End of Lecture

        #
        # Week 11
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('HLP-ifthenelse-videoeqt', 'xEJtdMQMcrs', 2),
             ('HLP-switch-videoeqt', '_4S3w4CBZcI', 2),
             ('HLP-while-videoeqt', 'HIPnr8V6foY', 2),
             ('HLP-for-videoeqt', 'xEJtdMQMcrs', 2)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('HLP-translateite-subsection', 4),
             ('HLP-translateswitch-subsection', 3),
             ('HLP-translatewhile-subsection', 2),
             ('HLP-translatefor-subsection', 1)
         ],
         [  # Problem sequence 'sequence_ID'
             'HLP-exco-C1'
         ]
         ),  # End of Lecture

        #
        # Week 12
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
             ('HLP-subroutineexecution-videoeqt', 'IGgxSgNxU1c', 4),
             ('HLP-activationblock-videoeqt', '7q-R2mCK_1Y', 3),
             ('HLP-subroutineexample-videoeqt', '5WenymqHm2M', 3)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
             ('HLP-callreturn-subsection', 3),
             ('HLP-registerparameters-subsubsection', 3),
             ('HLP-memoryparameters-subsubsection', 2),
             ('HLP-stackparameters-subsubsection', 1)
         ],
         [  # Problem sequence 'sequence_ID'
             'HLP-exco-C2'
         ]
         ),  # End of Lecture

        #
        # Week 13
        #
        ([  # Videos (activity-label, video id in youtube, number of EQTs)
         ],  # End of Lecture Videos
         [  # EQTs from other activities (no video) (label, number of EQTs)
         ],
         [  # Problem sequence 'sequence_ID'
         ]
         )  # End of Lecture
    ]

    # Pair (low, high) to restrict the versions to consider
    version_range = (1, 14)

    #
    # Given a resource ID, returns the week it is scheduled. The information in
    # this dictionary is derived solely from the previous table.
    #
    resource_id_to_category = {}

    accumulate.HandlerBasic.render_dict['data_capture_context'] = context_name
    accumulate.HandlerBasic.render_dict['url_home'] = course_url
    accumulate.HandlerBasic.render_dict['url_home_text'] = course_url_text
    accumulate.HandlerBasic.render_dict['template'] = \
        'dboard/elec1601_dboard.html'
    accumulate.HandlerBasic.render_dict['title_text'] = \
        'Your lecture preparation'
    accumulate.HandlerBasic.render_dict['time_slot'] = ''
    accumulate.HandlerBasic.render_dict['lecture_data'] = [0, 0, 0, 0, 0, 0,
                                                           0, 0]
    # accumulate.HandlerBasic.render_dict['suggestion_title'] = 'Learning ' \
    #                                                           'Strategy'
    accumulate.HandlerBasic.render_dict['suggestion_data'] = \
        ["""We don't have any recommendations yet!
           <img class="img-middle" src="{0}no_info.png"/></img>""".format(
                settings.STATIC_URL)]


    def __init__(self):

        # Loop over all the units given in the map
        for index in range(0, len(self.units_lec)):
            # Loop over all the ids and assign them to the right week
            for item_id in sum(self.expand_resource_ids(self.units_lec[index]),
                               []):
                self.resource_id_to_category[item_id] = index

    def get_version(self, event = None):
        """
        :param event:

        Uses the list of the session times and returns the index of the first
        session that is larger than the time of the given event.
        """

        # Get the time from the event, if any, or else, the current time
        if event is None:
            event_time = timezone.now()
        else:
            event_time = event.received

        # If the requested time is past the last session, return the last
        # session.
        if event_time > self.timeline_lec[-1]:
            return len(self.timeline_lec) - 1

        # Create the function to detect when the given time is larger.
        def test(c): return c > event_time

        # Return the index of the first element that is larger than EVENT_TIME
        return next(i for i, v in enumerate(self.timeline_lec) if test(v))

    def update_render_dict(self, username):

        # Value of the variable to show dashboard or not
        show_dboard = leco.models.Submission.objects.filter(
                user__email = username, action_id = 'form-submit',
                payload__contains = '"show-dboard"'
            ).order_by('-received').first()
        if show_dboard == None:
            accumulate.HandlerBasic.render_dict['show_dboard'] = 'Yes'
            return

        # There is a result from the query
        payload = json.loads(show_dboard.payload)
        accumulate.HandlerBasic.render_dict['show_dboard'] = payload['answer']

        # Value of the variable to show the suggestions or not
        show_suggestions = leco.models.Submission.objects.filter(
                user__email = username, action_id = 'form-submit',
                payload__contains = '"show-suggestions"'
            ).order_by('-received').first()
        if show_suggestions == None:
            accumulate.HandlerBasic.render_dict['show_suggestions'] = 'Yes'
            return

        # There is a result from the query
        payload = json.loads(show_suggestions.payload)
        accumulate.HandlerBasic.render_dict['show_suggestions'] = \
            payload['answer']

        return

    @staticmethod
    def expand_resource_ids(resources):
        """
        :param resources: A tuple of the form

        ([ youtube_id, ... ] # Video Ids
         [question_id, ... ] # Questions Embedded in Videos
         [question_id, ... ] # Questions Embedded in text
         ['sequence_id', ... ] # Problem sequences
        )

        Returns three lists with the resource ids that should be present in the
        events stored for each student.
        """
        video_ids = []
        video_eqts = []
        for (act_id, video_id, n) in resources[0]:
            video_ids.append(video_id)
            video_eqts.extend(["{0}-eqt_{1}".format(act_id, x)
                               for x in range(1, n + 1)])

        # Process the EQTs
        eqt_ids = []
        for (act_id, n) in resources[1]:
            eqt_ids.extend(["{0}-eqt_{1}".format(act_id, x)
                            for x in range(1, n + 1)])

        return video_ids, video_eqts, eqt_ids, resources[2]

    def get_week_resource_ids(self, category):
        """
        :param category: Given a category index, obtain a resource tuple of the
        form:

        ([ youtube_id, ... ] # Videos
         [ question_id, ... ] # Embedded q. in Videos
         [ question_id, ... ] # EQTs
         exco_answer: [ 'sequence_id', ... ] # Problem sequences
        )

        :return: a list of lists of labels with:
        - embedded video labels
        - embedded video question labels
        - embedded question labels
        - exco sequences
        """

        if category >= len(self.units_lec):
            return []

        return self.expand_resource_ids(self.units_lec[category])

    def calculate_week_scores(self, ctx_object, last_execution, options):
        """
        :param ctx_object: Context object (of the context_name)
        :param last_execution: Date time when it was last executed
        :param options: Options for the filter
        :return:
        """

        # Store the pointer to the context object in the database
        self.context_obj = ctx_object

        # Obtain the week to be considered
        week = options.get('week', None)
        if week is None:
            week = self.get_version()

        # Get the lecture activities for the week (separated in categories)
        lecture_activities = self.get_week_resource_ids(int(week))

        # Get a single list of activity ids
        all_activities = list(itertools.chain.from_iterable(lecture_activities))

        # Pre-load the new datetime stamp
        new_stamp = timezone.now()

        # Get all the users for which there is an indicator that has changed
        indicators = accumulate.models.Indicator.objects.filter(
                context = ctx_object,
                version = week,
                resource_id__in = all_activities)

        # If there are no indicators, terminate
        if len(indicators) == 0:
            # Update the time stamp on the filter
            last_execution.datetime_last_processed = new_stamp
            last_execution.save()
            return

        # Use the QuerySet to calculate the scores: video, vmcq, mcq, exco

        # VIDEO SCORES
        self.calculate_week_video_scores(indicators, lecture_activities[0],
                                         week, new_stamp)
        self.calculate_average_score('VIDEO', week, new_stamp)

        # VIDEO MCQ SCORES
        self.calculate_week_mcq_scores(indicators, lecture_activities[1],
                                       week, new_stamp, 'VMCQ')
        self.calculate_average_score('VMCQ', week, new_stamp)

        # MCQ SCORES
        self.calculate_week_mcq_scores(indicators, lecture_activities[2],
                                       week, new_stamp, 'MCQ')
        self.calculate_average_score('MCQ', week, new_stamp)

        # EXCO SCORES
        self.calculate_week_exco_scores(indicators, lecture_activities[3],
                                        week, new_stamp)
        self.calculate_average_score('EXCO', week, new_stamp)

        # Update the time stamp on the filter
        last_execution.datetime_last_processed = new_stamp
        last_execution.save()

    def calculate_week_video_scores(self, indicators, activities, week,
                                    new_stamp):

        # Filter the indicators
        video_indicators = indicators.distinct('user').filter(
                type = 'EVC_VIDEO', resource_id__in = activities)

        # Loop over every user
        for ind in video_indicators:

            user_payloads = indicators.filter(
                    type = 'EVC_VIDEO',
                    user = ind.user,
                    resource_id__in = activities).values_list(
                    'payload', flat = True)

            # The number of items selected must be below or equal to # of
            # activities
            assert (len(user_payloads) <= len(activities))

            score = 0
            # Loop over the video counts
            for video_payload in user_payloads:

                counters = json.loads(video_payload)
                # If the seconds viewed is more than 500 count it
                if counters[4] > 500:
                    score += 1
                    continue

                # If more plays than pauses, give it as "viewed"
                if counters[0] >= counters[1]:
                    score += 1
                    continue

            score = 1.0 * score / len(activities)

            # Create/update the indicator
            score_indicator = accumulate.iepf.get_indicator(ind.user,
                                                            'SCORE',
                                                            self.context_obj,
                                                            'VIDEO',
                                                            week)
            score_indicator.payload = json.dumps(score)
            score_indicator.updated = new_stamp
            score_indicator.save()

            if data2u.settings.DEBUG:
                print 'SCORE(Video): ', score, ind.user.email, week

    def calculate_week_mcq_scores(self, indicators, activities, week,
                                  new_stamp, score_type):

        # Filter the indicators
        mcq_indicators = indicators.distinct('user').filter(
                type = 'EVC_MCQ', resource_id__in = activities)

        # Loop over every user
        for ind in mcq_indicators:

            user_payloads = indicators.filter(
                    type = 'EVC_MCQ',
                    user = ind.user,
                    resource_id__in = activities).values_list(
                    'payload', flat = True)

            # The number of items selected must be below or equal to # of
            # activities
            assert (len(user_payloads) <= len(activities))

            # Formula:
            #
            # If #correct = 0 & #show_answers = 0 --> 0
            # If #correct = 0 & #show_answers != 0 --> 0.5
            # If #correct > #show_answers --> 1
            # Otherwise: 0.5

            score = 0
            for q_counters in user_payloads:

                counters = json.loads(q_counters)

                # If #correct = 0 & #show_answers = 0:  --> Value is 0
                if counters[0] == 0 and counters[2] == 0:
                    continue

                # If #correct = 0 & #show_answers != 0 --> Value is 0.5
                if counters[0] == 0 and counters[2] != 0:
                    score += 0.5
                    continue

                # If #correct > #show_answers --> 1
                if counters[0] > counters[2]:
                    score += 1
                    continue

                # Otherwise: 0.5
                score += 0.5

            score = 1.0 * score / len(activities)

            # Create/update the indicator
            score_indicator = accumulate.iepf.get_indicator(ind.user,
                                                            'SCORE',
                                                            self.context_obj,
                                                            score_type,
                                                            week)
            score_indicator.payload = json.dumps(score)
            score_indicator.updated = new_stamp
            score_indicator.save()

            if data2u.settings.DEBUG:
                print 'SCORE({0}): '.format(score_type), score, ind.user.email,
                print week

    def calculate_week_exco_scores(self, indicators, activities, week,
                                   new_stamp):
        # Filter the indicators
        exco_indicators = indicators.distinct('user').filter(
                type = 'EVC_EXCO', resource_id__in = activities)

        # Loop over every user
        for ind in exco_indicators:

            user_payloads = indicators.filter(
                    type = 'EVC_EXCO',
                    user = ind.user,
                    resource_id__in = activities).values_list(
                    'payload', flat = True)

            # The number of items selected must be below or equal to # of
            # activities
            assert (len(user_payloads) <= len(activities))

            score = 0
            for exco_payload in user_payloads:
                # Load the payload (list with score as first element)
                counters = json.loads(exco_payload)

                # Get the first element and accumulate it
                score += counters[0]

            score = 0.01 * score / len(activities)

            # Create/update the indicator
            score_indicator = accumulate.iepf.get_indicator(ind.user,
                                                            'SCORE',
                                                            self.context_obj,
                                                            'EXCO',
                                                            week)
            score_indicator.payload = json.dumps(score)
            score_indicator.updated = new_stamp
            score_indicator.save()

            if data2u.settings.DEBUG:
                print 'SCORE(EXCO): ', score, ind.user.email, week

    def calculate_average_score(self, ind_type, week, new_stamp):
        """
        Use the context name, type of indicator and a week to select the
        indicators and compute their average value.

        Create a new indicator with empty user to store this average

        :param ind_type: Type of indicators to consider
        :param week: Week to select indicators for the average
        :param new_stamp: Date time stamp to use for the new indicator
        :return:
        """

        # Obtain the relevant indicators from the database
        to_average = accumulate.models.Indicator.objects.filter(
                        user__isnull = False,
                        context__members = F('user'),
                        context__name = self.context_name,
                        type = 'SCORE',
                        resource_id = ind_type,
                        version = week).values_list(
                        'payload', flat = True)

        # Calculate the average score
        if not to_average:
            result = 0
        else:
            result = sum([float(x) for x in to_average])/len(to_average)

        # Create or update the new indicator
        # Create/update the indicator
        avg_indicator = accumulate.iepf.get_indicator(None,
                                                      'SCORE',
                                                      self.context_obj,
                                                      ind_type,
                                                      week)
        avg_indicator.payload = json.dumps(result)
        avg_indicator.updated = new_stamp
        avg_indicator.save()

################################################################################
#
# Execution as script
#
if __name__ == "__main__":
    # print units
    # for x in timelines_lecs['1']:
    #     print str(x)
    # for x in timelines_tuts['MON1']:
    #     print str(x)
    # for x in timelines_tuts['MON2']:
    #     print str(x)

    # Lecture activities
    # print units_lec[get_week_index(timelines_lecs['1'])][1]
    # Tutorial activities
    # print units_tut[get_week_index(timelines_tuts['THU1'])][0]

    # data = student_initial_scores(units_lec[2])
    # print data
    # print 'Summary'
    # print len(data[0]), 'videos'
    # print len(data[1]), 'eqts'
    # print len(data[2]), 'sequences'

    # data = student_initial_course_scores(units_lec)
    # print data
    # print len(data)
    # data2 = student_initial_course_scores(units_lec, data)
    # print data2
    # print len(data2)

    # print expand_resource_ids(units_lec[1])
    # print resource_id_to_category

    print data2u.settings.student_list

    pass
