import sys

def to_sql(dataframe, **kwargs):
    size = 4096
    total = len(dataframe)
    name = kwargs.get('name')

    def chunker(df):
        return (df[i:i + size] for i in range(0, len(df), size))

    for i, df in enumerate(chunker(dataframe)):
        df.to_sql(**kwargs)
        index = i * size
        percent = (index * 100) / total
        print(f'{name} {percent:.2f}% {index}/{total}', end='\r')

    print()