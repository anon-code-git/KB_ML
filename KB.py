#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
.. module:: KB.py
    :synopsis: Code for the diagramatic representations of suicide risk, both Moderate and High, and inference of final data.
"""

import pandas as pd
import sys
import csv


def bakoitza_altu(lerro):
    """
    Indicates that a person is at high risk.
    The algorithm is based on the diagram from the High suicidal risk.

    Args:
        row: An array containing data for each person. The contents are as follows
        (with the number indicating the position):

            [0=identifier, 1=age, 2=gender, 3=suicidal_ideation, 4=suicidal_desire,
             5=suicide_plan, 6=suicide_attempt, 7=attempt_count, 8=self_harm,
             9=exposure_to_suicide, 10=relation_label_of_suicide,
             11=identification_with_suicide, 12=depression_score,
             13=mental_pain, 14=pain_tolerance, 15=hopelessness, 16=SCS,
             17=perceived_burden, 18=social_connectedness]


    Returns:
        label: An index that can be 0, or 2; corresponding to:
            {0: "no risk",
            1: "moderate risk",
            2: "high risk",
    """


    etiketa = 0
    if int(lerro[16]) >= 40:  # SCS-R
        etiketa = 2     
        return etiketa
    if (int(lerro[6]) == 1) or (int(lerro[8]) == 1) or (
            int(lerro[3]) == 1) or (int(lerro[12]) >= 10) or int(
                lerro[9] == 1):
        # prev. attempts, self-harm, ideation or depression, or suicides of people near
        if int(lerro[13]) >= 46 or int(lerro[14]) <= 25:
            # mental pain or low tolerance
            if int(lerro[15]) >= 2:
                # hopelessness
                if int(lerro[18]) <= 12:
                    # belongingness
                    etiketa = 2
            else:
                # no hopelessness
                if int(lerro[18]) <= 12:
                    # belongingness
                    if int(lerro[5]) == 1:
                        etiketa = 2  
    return etiketa


def bakoitza_moderatu(lerro):
    """
    Indicates that a person is at moderate risk.
    The algorithm is based on the diagram from the Moderate suicidal risk.

    Args:
        row: An array containing data for each person. The contents are as follows
        (with the number indicating the position):

            [0=identifier, 1=age, 2=gender, 3=suicidal_ideation, 4=suicidal_desire,
             5=suicide_plan, 6=suicide_attempt, 7=attempt_count, 8=self_harm,
             9=exposure_to_suicide, 10=relation_label_of_suicide,
             11=identification_with_suicide, 12=depression_score,
             13=mental_pain, 14=pain_tolerance, 15=hopelessness, 16=SCS,
             17=perceived_burden, 18=social_connectedness]


    Returns:
        label: An index that can be 0, or 1; corresponding to:
            {0: "no risk",
            1: "moderate risk",
            2: "high risk",
    """

    etiketa = 0
    if (int(lerro[6]) == 1) or (int(lerro[8]) == 1) or (
            int(lerro[3]) == 1) or (int(lerro[12]) >= 10) or int(
                lerro[9] == 1):
        # prev. attempts, self-harm, ideation or depression, or suicides of people near
        if int(lerro[13]) >= 36 and int(lerro[13]) <= 45 or int(
                lerro[14]) <= 25:
            # moderate mental pain or low tolerance
            if int(lerro[15]) >= 2:
                # hopelessness
                etiketa = 1
            else:
                # no hopelessness
                if int(lerro[18]) <= 12:
                    # belongingness
                    etiketa = 1
    return etiketa


if __name__ == "__main__":
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "data.csv"
    data = pd.read_csv(filename)
    data.replace(to_replace=" ", value=0, inplace=True)
    with open("KB.csv", "w", newline='') as f:
        w = csv.writer(f)
        w.writerow([
            "identifier", "age", "gender", "suicidal_ideation", "suicidal_desire", 
            "suicide_plan", "suicide_attempt", "attempt_count", "self_harm",
            "exposure_to_suicide", "relation_label_of_suicide",
            "identification_with_suicide",
            "depression_score", "mental_pain", "pain_tolerance",
            "hopelessness", "SCS", "perceived_burden",
            "social_connectedness", "target_label"
        ])

        for line in data.values:
            em1 = bakoitza_altu(line)
            em2 = bakoitza_moderatu(line)
            em = max(em1, em2)
            inp = list(line)
            inp.append(em)
            w.writerow(inp)
    f.close()
