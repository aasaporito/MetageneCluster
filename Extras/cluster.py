"""Summary

"""
from dataclasses import dataclass

#  todo 5 (general) +0: Is this file unused?
@dataclass
class cluster:

    """Summary

    """

    def __init__(self, data):
        """Summary
            Constructor for Cluster object

        Args:
            data (list): Description
        """
        # initialize random centers

        self._centers = []
        self._idxs = []
        self._data = []
        self._plus = 0
        self._minus = 0

    # gettrs
    def getCenters(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return self._centers

    def getIdxs(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return self._idxs

    def getData(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return self._data

    def strandRatio(self):
        """Summary

        Returns:
            TYPE: Description
        """
        return self._plus / (self._plus / self._minus)

    def incStrand(self, strand):
        """Summary

        Args:
            strand (TYPE): Description
        """
        if strand == '+':
            self._plus += 1
        elif strand == '-':
            self._minus += 1

   # def _randCenters(self):
