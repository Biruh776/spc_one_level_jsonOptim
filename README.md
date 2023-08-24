## Overview

This is an implementation of Statistical Process Control(SPC) rules for evaluating analytical run quality for medical laboratories. The program checks for violations against 16 unique rules. The program utilizes pandas, which in turn uses NumPy for computations, making it more efficient.

## Contents

1. [SPC Rules](#1-spc-rules)
1. [Input](#2-input)
   1. [Quality Control (QC) Data](#21-quality-control-qc-data)
   1. [Rules List](#22-rules-list)
   1. [Level List](#23-level-list)
   1. [Examples of Complete Requests](#23-examples-of-complete-requests)
1. [Output](#3-output)

## 1 SPC Rules

SPC rules are mainly used in laboratories for three reasons.
- Reduce false rejections of good data
- Increase error detection of bad data
- Distinguish between random and systematic errors

An effective quality control system should possess the ability to identify and reject erroneous data while minimizing false positives by accurately distinguishing valid data. The full list of SPC rules implemented is given below.

1. 1-2s: This is usually a warning rule violated when a single control observation is outside the ±2SD limit. An analytical run usually should not be rejected if it violates this rule as approximately 4.5% of all valid QC values will fall in ±2SD and ±3SD limit. Laboratories universally rejecting values outside the ±2SD limit end up rejecting good runs too frequently. The rule should only be applied on a single level.

1. 1-2.5s: This rule is violated when a data point is outside the ±2.5SD limit. The rule indicates random error and should only be applied on a single level

1. 1-3s: The rule identifies unacceptable random error or possibly the beginning of a large systematic error. Any QC result outside ±3SD violates this rule. The rule should only be applied on a single level.

1. 1-3.5s: The run is considered out of control when one control value exceeds the mean ±3.5SD. This rule is applied on a single level.

1. 1-4s: The run is considered out of control when one control value exceeds the mean ±4SD. This rule is applied on a single level.

1. 1-5s: The run is considered out of control when one control value exceeds the mean ±5SD. This rule is applied on a single level. 

1. 2-2s: This rule detects systematic errors. The rule is violated when two consecutive QC results are greater than ±2SD and are on the same side of the mean.

1. R-4s: The rule identifies random errors. This rule is violated when there is at least a 4SD difference between any two control values across runs (client requirement).

1. 3-1s: The rule is violated when three consecutive results are greater than ±SD and on the same side of the mean across runs. It shows systematic errors.

1. 4-1s: The rule is violated when four consecutive results are greater than ±SD and on the same side of the mean across runs. It shows systematic errors.

1. 7-T: The rule is violated when a group of seven consecutive data points for a single level of control show either a "strict" increasing or decreasing pattern.

1. N-x: The rule is violated when there are N control results on the same side of the mean. N can be 7, 8, 9, 10, or 12. It shows a systematic error.

## 2. Input

### 2.1 Quality Control (QC) Data

The expected input data is in Json format. The maximum simultaneous quality control runs the program can handle is 6. The program is, however, easily scalable to any number of simultaneous runs. Six was the requirement when the program was being developed.

### 2.2 Rules List

A list of SPC rules that need to be checked should be passed as a list of strings. `rule_list : ["1-2s", "1-3s",...]`. The full list of all the available rules are

`["1-2s", "1-2.5s","1-3s","1-3.5s","1-4s","1-5s","2-2s","R-4s","3-1s","4-1s","7-T","7-x","8-x","9-x","10-x","12-x"]`

### 2.3 Level List

A list of levels that need to be checked should be passed as a list of strings. `level_list : [1, 3, ...]`. 

### 2.4 Example of a complete Requests

```json
{
    "data": [
        {
            "index": 1,
            "datas": [
                {
                    "level": 1,
                    "value": 1.2,
                    "mean": 1.2,
                    "sd": 1.2
                },
                {
                    "level": 2,
                    "value": 1.2,
                    "mean": 1.2,
                    "sd": 1.2
                }
            ]
        },
        {
            "index": 2,
            "datas": [
                {
                    "level": 1,
                    "value": 1.2,
                    "mean": 0.2,
                    "sd": 0.2
                },
                {
                    "level": 2,
                    "value": 2.2,
                    "mean": 0.5,
                    "sd": 0.5
                }
            ]
        }
        ],
    "rule_list": ["1-2s", "1-3s"],
    "level_list": [1, 2]
}
```

> The keys in the json file must be kept as shown in the example.

### 3 Output

The program returns a JSON with the provided data and SPC rule check results for the requested rules. Each item of the list will 

```json
[
    {
        "index": 1,
        "result": [
            {
                "level": 1,
                "spcViolation":"1-2s|1-3s"
            },
            {
                "level": 2,
                "spcViolation":""
            }
        ]
    },
    {
        "index": 2,
        "datas": [
            {
                "level": 1,
                "spcViolation":"1-2s|1-3s"
            },
            {
                "level": 2,
                "spcViolation":""
            }
        ]
    }
]
```