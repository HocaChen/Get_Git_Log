import plot_curve_by_date
import get_git_add_delete
from datetime import date

if __name__ == '__main__':
    try:
        state_date = date(2022, 8, 22)
        end_date = date(2022, 9, 21)

        plot_curve_by_date.plot_curve(state_date, end_date)
        get_git_add_delete.create_csv_data(state_date, end_date)
    except Exception as e:
        print(str(e))
