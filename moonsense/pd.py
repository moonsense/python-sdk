"""
Copyright 2021 Moonsense, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import functools
import operator
import pandas as pd


def read_accelerometer(session_file) -> pd.DataFrame:
    """
    Read accelerometer data from a session file

    :param session_file: path to session file
    """
    df = pd.read_json(session_file, lines=True)
    accelerometer_data = functools.reduce(
        operator.iconcat,
        df["bundle"].apply(pd.Series)["accelerometer_data"].dropna().tolist(),
        [],
    )
    df = pd.DataFrame(accelerometer_data).rename(columns={"determined_at": "at"})
    df["at"] = pd.to_datetime(df["at"], unit="ms")
    return df.set_index("at").sort_index()
