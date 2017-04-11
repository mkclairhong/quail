#!/usr/bin/env python

import pandas as pd
from .analysis import recall_matrix
from .helpers import list2pd
from .helpers import default_dist_funcs

class Egg(object):
    """
    Data object for the quail package

    An Egg data object contains the data you need to analyze free recall experiments.
    This can be a single subject's data, or a group of subjects.  An Egg is comprised of
    a number of fields: the pres field contains the words/stimuli presented to the subject.
    The rec field contains the words/stimuli recalled by the subject. The feature field
    is optional, but may contain a dictionary of features for each stimulus.  This
    field is necessary to run the fingerprint analyses. Related to the features
    is the dist_funcs dictionary (also optional).  This dictionary specifies
    a set of distance functions required for the fingerprint analyses.  Finally,
    the meta field is an optional dictionary that contains any details useful for
    identifying the egg object

    Attributes
    ----------

    pres : pd.DataFrame
        Dataframe containing the presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number

    rec : pd.DataFrame
        Dataframe containing the words recalled.  Each row represents the recalled words for a given list and each column
        represents a list.  Each row represents the recalled words for a given list and each column
        represents a list. The cells should be lowercase words. The index will be a multi-index, where the first level reprensents the subject number
        and the second level represents the list number

    features : pd.DataFrame (optional)
        Dataframe containing the features for presented words.  Each row represents the presented words for a given list and each column
        represents a list. The cells should be a dictionary of features, where the keys are the name of the features, and the values are the feature values.
        The index will be a multi-index, where the first level reprensents the subject number and the second level represents the list number

    dist_funcs : dict (optional)
        A dictionary of custom distance functions for stimulus features.  Each key should be the name of a feature
        and each value should be an inline distance function (e.g. `dist_funcs['feature_n'] = lambda a, b: abs(a-b)`)

    meta : dict (optional)
        Meta data about the study (i.e. version, description, date, etc.) can be saved here.

    """


    def __init__(self, pres=[[[]]], rec=[[[]]], features=None, dist_funcs=dict(), meta={}, list_length=None):

        if not all(isinstance(item, list) for sub in pres for item in sub):
            pres = [pres]

        if not all(isinstance(item, list) for sub in rec for item in sub):
            rec = [rec]

        if features:
            if not all(isinstance(item, list) for sub in features for item in sub):
                features = [features]

        self.pres = list2pd(pres)
        self.rec = list2pd(rec)
        self.meta = meta

        # attach features and dist funcs if they are passed
        if features:
            self.features = list2pd(features)
            self.dist_funcs = default_dist_funcs(dist_funcs, features[0][0][0])
        else:
            self.features = None
            self.dist_funcs = None

        if list_length is None:
            self.list_length = len(pres[0][0])-1
        else:
            self.list_length = list_length
