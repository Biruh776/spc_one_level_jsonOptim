import pandas as pd


class Spc_quality_control:
    """
    This class defines a spc_quality control object and provides definitions for spc rules that are applied on a single
    level.
    """

    def __init__(self, lev1, mean, std):
        self.lev1 = lev1
        self.mean = mean
        self.std = std
        self.std_bool = self.std.astype(bool)

    def r1_2s(self):
        """
        The 1-2s rule is usually a warning rule violated when a single control observation is outside the ±2SD limit.
        """
        return self._check_diff(2)

    def r1_25s(self):
        """
        The 1-2.5s rule indicates random error and may also point to systematic error.
        Indicates an observation is outside ±2.5SD range
        """
        return self._check_diff(2.5)

    def r1_3s(self):
        """
        The 1-3s rule identifies unacceptable random error or possibly the beginning of a large systematic error.
        Any QC result outside ±3SD violates this rule.
        """
        return self._check_diff(3)

    def r1_35s(self):
        """
        The 1-3.5s rule indicates random error and may also indicate systematic error.
        The run is considered out of control when one control value exceeds the mean ±3.5SD.
        """
        return self._check_diff(3.5)

    def r1_4s(self):
        """
        Violation of the 1-4s rule indicates random error and may also point to systematic error.
        The run is considered out of control when one control value exceeds the mean ±4SD.
        """
        return self._check_diff(4)

    def r1_5s(self):
        """
        Violation of this rule indicates random error and may also point to systematic error.
        The run is considered out of control when one control value exceeds the mean ±5SD.
        """
        return self._check_diff(5)

    def r2_2s(self):
        """
        Checks if two control values in the across runs are >2SD on the same side of the mean.
        Violation of the within run application indicates systematic error is present and potentially affecting
        the entire analytical curve.
        """
        violations = [False]

        for i in range(1, len(self.lev1)):
            curr = self.lev1[i]
            prev = self.lev1[i - 1]

            curr_deviation = curr - self.mean[i]
            prev_deviation = prev - self.mean[i - 1]

            if (
                    curr_deviation > 2 * self.std[i] and
                    prev_deviation > 2 * self.std[i - 1] and
                    self.std_bool[i] and self.std_bool[i - 1]
            ):
                violations.append(True)
            elif (
                    curr_deviation < -2 * self.std[i] and
                    prev_deviation < -2 * self.std[i - 1] and
                    self.std_bool[i] and self.std_bool[i - 1]
            ):
                violations.append(True)
            else:
                violations.append(False)

        return pd.Series(violations)

    # def r2_3_2s(self):
    #     """
    #     This rule is violated when two of three consecutive values are more the 2SD on the same side of the mean.
    #     The rule identifies systematic error.
    #     """
    #     filter_result = pd.Series(False, index=self.lev1.index)
    #     for i in range(len(self.lev1) - 3 + 1):
    #         window = self.lev1[i: i + 3]
    #         window_mean = self.mean[i: i + 3]
    #         window_std = self.std[i: i + 3]
    #         if (sum(window < window_mean - 2 * window_std) == 2 or
    #                 sum(window > window_mean + 2 * window_std) == 2):
    #             filter_result[i + 3 - 1] = True
    #
    #     return filter_result

    def r4_s(self):
        """
        The R-4s rule identifies random error.
        This rule is violated when the difference between the rolling min and the current value is more than 4SD.
        Where SD is the current standard deviation.
        """
        # Calculate the rolling minimum
        rolling_min = self.lev1.expanding().min()
        violations = (self.lev1 - rolling_min) >= 4 * self.std
        violations = violations & self.std_bool
        return violations

    def r3_1s(self):
        """
        Checks if three consecutive results are greater than 1SD and on the same side of the mean.
        """
        violations = [False, False]

        for i in range(2, len(self.lev1)):
            curr = self.lev1[i]
            prev = self.lev1[i - 1]
            prev2 = self.lev1[i - 2]

            curr_deviation = curr - self.mean[i]
            prev_deviation = prev - self.mean[i - 1]
            prev2_deviation = prev2 - self.mean[i - 2]

            if (
                    curr_deviation > self.std[i] and
                    prev_deviation > self.std[i - 1] and
                    prev2_deviation > self.std[i - 2] and
                    self.std_bool[i] and self.std_bool[i - 1] and self.std_bool[i - 2]
            ):
                violations.append(True)
            elif (
                    curr_deviation < -self.std[i] and
                    prev_deviation < -self.std[i - 1] and
                    prev2_deviation < -self.std[i - 2] and
                    self.std_bool[i] and self.std_bool[i - 1] and self.std_bool[i - 2]
            ):
                violations.append(True)
            else:
                violations.append(False)

        return pd.Series(violations)

    def r4_1s(self):
        """
        Checks if four consecutive results are greater than 1SD and on the same side of the mean.
        """
        violations = [False, False, False]

        for i in range(3, len(self.lev1)):
            curr = self.lev1[i]
            prev = self.lev1[i - 1]
            prev2 = self.lev1[i - 2]
            prev3 = self.lev1[i - 3]

            curr_deviation = curr - self.mean[i]
            prev_deviation = prev - self.mean[i - 1]
            prev2_deviation = prev2 - self.mean[i - 2]
            prev3_deviation = prev3 - self.mean[i - 3]

            if (
                    curr_deviation > self.std[i] and
                    prev_deviation > self.std[i - 1] and
                    prev2_deviation > self.std[i - 2] and
                    prev3_deviation > self.std[i - 3] and
                    self.std_bool[i] and self.std_bool[i - 1] and
                    self.std_bool[i - 2] and self.std_bool[i - 3]
            ):
                violations.append(True)
            elif (
                    curr_deviation < -self.std[i] and
                    prev_deviation < -self.std[i - 1] and
                    prev2_deviation < -self.std[i - 2] and
                    prev3_deviation < -self.std[i - 3] and
                    self.std_bool[i] and self.std_bool[i - 1] and
                    self.std_bool[i - 2] and self.std_bool[i - 3]
            ):
                violations.append(True)
            else:
                violations.append(False)

        return pd.Series(violations)

    def r7_T(self):
        """
        The 7-T rule is violated when a group of seven consecutive data points for a single level of control show
        either a "strict" increasing or decreasing pattern. A "strict" increasing pattern is defined as a series of
        points increasing incrementally from the previous point without a break in the pattern.
        """
        increasing_filter = pd.Series(False, index=self.lev1.index)
        decreasing_filter = pd.Series(False, index=self.lev1.index)

        for i in range(len(self.lev1) - 7 + 1):
            window = self.lev1[i: i + 7]
            if window.is_monotonic_increasing and window.is_unique:
                increasing_filter[i + 7 - 1] = True
            elif window.is_monotonic_decreasing and window.is_unique:
                decreasing_filter[i + 7 - 1] = True
        return increasing_filter | decreasing_filter

    def r7_x(self):
        """
        7-x rules are violated when there are seven control results on the same side of the mean.
        """
        return self._rN_x(7)

    def r8_x(self):
        """
        8-x rules are violated when there are eight control results on the same side of the mean.
        """
        return self._rN_x(8)

    def r9_x(self):
        """
        9-x rules are violated when there are nine control results on the same side of the mean.
        """
        return self._rN_x(9)

    def r10_x(self):
        """
        10-x rules are violated when there are 10 control results on the same side of the mean.
        """
        return self._rN_x(10)

    def r12_x(self):
        """
        12-x rules are violated when there are 12 control results on the same side of the mean.
        """
        return self._rN_x(12)

    def _rN_x(self, n):
        """
        Helper method. It checks if n consecutive values are control results on the same side of the mean.
        :param n: Number of consecutive values checked
        :return: a Boolean for each value of the data. True shows violation. False shows no violation
        """
        filter_result = pd.Series(False, index=self.lev1.index)
        for i in range(len(self.lev1) - n + 1):
            window = self.lev1[i: i + n]
            window_mean = self.mean[i: i + n]
            if (window < window_mean).all() or (window > window_mean).all():
                filter_result[i + n - 1] = True

        return filter_result

    def _check_diff(self, n):
        """
        Helper method. It checks if a value is n * STD away from the mean value
        :param n:
        :return: A Boolean. True shows violation. False shows no violation.
        """
        filter_result = pd.Series(False, index=self.lev1.index)
        mean_diff = self.lev1 - self.mean
        filter_result = mean_diff.abs() > n * self.std
        filter_result = filter_result & self.std_bool
        return filter_result
