import functools
import operator

import pandas as pd


def read_accelerometer(session_file) -> pd.DataFrame:
    df = pd.read_json(session_file, lines=True)
    accelerometer_data = functools.reduce(
        operator.iconcat,
        df["bundle"].apply(pd.Series)["accelerometer_data"].tolist(),
        [],
    )
    df = pd.DataFrame(accelerometer_data).rename(columns={"determined_at": "at"})
    df["at"] = pd.to_datetime(df["at"], unit="ms")
    return df.set_index("at").sort_index()
