import pandas as pd

class Verification:

    @staticmethod
    def question1_verifcation_pandas():
        # Reading the CSV file using Pandas
        dfc19 = pd.read_csv("Machine Learning Big Data/time_series_covid19_confirmed_global.csv")

        # Creating the list of months
        monthlist = []
        date_list = dfc19.columns[4:]

        for d in range(len(date_list)):
            if (d == len(date_list)-1 or (date_list[d-1])[0:2] != (date_list[d])[0:2]):
                monthlist.append((date_list[d-1])[0:2] + (date_list[d-1])[-2:])

        # Creating the output DataFrame
        dfq1 = dfc19.iloc[:, :4]  # Selecting the first 5 columns

        index_month = 0
        nbrc = 4
        nbrcprevious = 4

        for c in range(4, len(dfc19.columns)):
            if index_month < len(monthlist) and dfc19.columns[c][:2] == monthlist[index_month][:2] and dfc19.columns[c][-2:] == monthlist[index_month][-2:]:
                nbrc += 1
            else:
                print("Verification month " + str(monthlist[index_month][:2]) + str(monthlist[index_month][-2:]))

                # Calculate the mean for the current month
                month_mean = dfc19.iloc[:, nbrcprevious:nbrc + 1].sum(axis=1) / (nbrc - nbrcprevious)
                month_mean = round(month_mean)
                month_name = monthlist[index_month]

                # Add the column of the current month to the output DataFrame
                dfq1[month_name] = month_mean

                nbrcprevious = nbrc

                if index_month < len(monthlist) - 1:
                    index_month += 1

        return dfq1
