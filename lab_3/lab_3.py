from spyre import server
import pandas as pd
import matplotlib.pyplot as plt


def read_csv_file():
    tuple_NNAA_to_LW = {1: 22, 2: 24, 3: 23, 4: 25, 5: 3, 6: 4, 7: 8, 8: 19, 9: 20, 10: 21, 11: 9, 12: 0, 13: 10,
                        14: 11, 15: 12, 16: 13, 17: 14, 18: 15, 19: 16, 20: 0, 21: 17, 22: 18, 23: 6, 24: 1, 25: 2,
                        26: 7, 27: 5}
    frames = []

    for index_f in range(1, 28):
        with open(
                fr'data/vhi_data_province_{index_f}_2024-01-18_19-28-34.csv',
                "r") as dataset:
            df = dataset.readlines()
            df = [line.strip().split(',') for line in df]

            df = pd.DataFrame(df[2:], columns=['year', 'Week', 'SMN', 'SMT', 'VCI', 'TCI', 'VHI', 'empty'])
            df = df.astype(
                {'year': int, 'Week': int, 'SMN': float, 'SMT': float, 'VCI': float, 'TCI': float, 'VHI': float,
                 'empty': str})
            df['index_region'] = tuple_NNAA_to_LW[index_f]

            frames.append(df)

    result_df = pd.concat(frames, ignore_index=True)
    return result_df


class StockExample(server.App):
    df = read_csv_file()
    title = "Historical Stock Prices"

    inputs = [
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": [
                {"label": "Cherkasy", "value": 1},
                {"label": "Chernihiv", "value": 2},
                {"label": "Chernivtsi", "value": 3},
                {"label": "Crimea", "value": 4},
                {"label": "Dnipro", "value": 5},
                {"label": "Donets'k", "value": 6},
                {"label": "Ivano-Frankivs'k ", "value": 7},
                {"label": "Kharkiv", "value": 8},
                {"label": "Kherson", "value": 9},
                {"label": "Khmel'nyts'kyy", "value": 10},
                {"label": "Kyiv", "value": 11},
                {"label": "Kyiv City", "value": 12},
                {"label": "Kirovohrad", "value": 13},
                {"label": "Luhans'k", "value": 14},
                {"label": "L'viv", "value": 15},
                {"label": "Mykolayiv", "value": 16},
                {"label": "Odessa", "value": 17},
                {"label": "Poltava", "value": 18},
                {"label": "Rivne", "value": 19},
                {"label": "Sevastopol'", "value": 20},
                {"label": "Sumy", "value": 21},
                {"label": "Ternopil'", "value": 22},
                {"label": "Transcarpathia", "value": 23},
                {"label": "Vinnytsya", "value": 24},
                {"label": "Volyn", "value": 25},
                {"label": "Zaporizhzhya", "value": 26},
                {"label": "Zhytomyr", "value": 27}
            ],
            "key": 'region',
            "action_id": "update_data"
        },
        {
            "type": 'dropdown',
            "label": 'Region',
            "options": [
                {"label": "VHI", "value": "VHI"},
                {"label": "SMN", "value": "SMN"},
                {"label": "SMT", "value": "SMT"},
                {"label": "VCI", "value": "VCI"},
                {"label": "TCI", "value": "TCI"}
            ],
            "key": 'ticker',
            "action_id": "update_data"
        },
        {
            "type": "text",
            "id": "year",
            "label": "Year (1982-2023) (format: from-to)",
            "value": "1982-2000",
            "key": "year",
            "action_id": "update_data"
        },
        {
            "type": "text",
            "id": "week",
            "label": "Week (1-53) (format: from-to)",
            "value": "1-3",
            "key": "week",
            "action_id": "update_data"
        },

    ]

    controls = [
        {
            "type": "button",
            "id": "update_data",
            "label": "Upload Data"
        }
    ]

    tabs = ["Plot", "Table"]

    outputs = [
        {
            "type": "plot",
            "id": "plot",
            "control_id": "update_data",
            "tab": "Plot",
        },
        {
            "type": "table",
            "id": "table_id",
            "control_id": "update_data",
            "tab": "Table",
            "on_page_load": True
        },

    ]

    def getData(self, params):
        df = read_csv_file()
        region = int(params['region'])
        self.weeks = [int(week) for week in params["week"].split("-")]
        ticker = params['ticker']
        years = [int(year) for year in params["year"].split("-")]

        # Print values for debugging
        print(f"Region: {type(region)}, Years: {type(years[1])}, Ticker: {type(ticker)}")

        # Filter data
        result_df = df[(df['index_region'] == region) & (df['year'] >= years[0]) & (df['year'] <= years[1]) & ((df['Week'] >= self.weeks[0]) & (df['Week'] <= self.weeks[1]))]



        # result_df = pd.concat([df_weeks[ticker], df_weeks['year'], df_weeks['Week']], axis=1, ignore_index=False)

        return result_df

    def getPlot(self, params):
        data = self.getData(params)

        fig, ax = plt.subplots()

        # Combine year and week values for x-tick labels
        x_ticks_labels = [f"{int(year)} {int(week)}" for year, week in zip(data['year'], data['Week'])]

        # Plot the data
        ax.plot(range(len(data)), data[params['ticker']], marker='o')

        # Set labels and title
        ax.set_xlabel('Year and Week')
        ax.set_ylabel(params['ticker'])
        ax.set_title(f"{params['ticker']} for region {params['region']}")

        # Set x-tick labels
        ax.set_xticks(range(len(data)))
        ax.set_xticklabels(x_ticks_labels, rotation=45, ha="right")

        # Optionally display the grid
        ax.grid(True)

        return fig



app = StockExample()
app.launch(port=8091)