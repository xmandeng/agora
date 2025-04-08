import pandas as pd

if __name__ == "__main__":

    df = pd.DataFrame()
    df["A"] = [1, 2, 3]
    df["B"] = [4, 5, 6]
    df["C"] = [7, 8, 9]

    print(df.head())
