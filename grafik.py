from prettytable import PrettyTable
def build_timetable_table():
    table = PrettyTable()
    table.field_names = ["godziny","Poniedziałek","Wtorek","Środa","Czwartek","Piątek","Sobota","Niedziela"]
    table.add_row(["6.00 - 23.00","Sala treningowa","Sala treningowa","Sala treningowa","Sala treningowa","Sala treningowa","Sala treningowa",
                   "Sala treningowa"])
    table.add_row(["6.00 - 7.00","yoga","","yoga","","yoga","",""])
    table.add_row(["7.00 - 8.00","","yoga","","yoga", "","yoga",""])
    table.add_row(["8.00 - 9.00","","","","","","",""])
    table.add_row(["9.00 - 10.00","zdrowy kręgosłup","","zdrowy kręgosłup","","","zdrowy kręgosłup",""])
    table.add_row(["10.00 - 11.00","","","","","","",""])
    table.add_row(["11.00 - 12.00","","","","","","",""])
    table.add_row(["12.00 - 13.00",	"kawa","kawa","kawa","kawa","kawa","kawa","kawa"])
    table.add_row(["13.00 - 14.00","","","","","","",""])
    table.add_row(["14.00 - 15.00","","","stretching","","stretching","","stretching"])
    table.add_row(["15.00 - 16.00","","stretching","","stretching","","stretching",""])
    table.add_row(["17.00 - 18.00","","","","","","",""])
    table.add_row(["18.00 - 19.00","yoga","yoga","yoga","yoga","yoga","yoga",""])
    table.add_row(["19.00 - 20.00","","","","","","",""])
    table.add_row(["20.00 - 21.00","fitness","fitness","fitness","fitness","fitness","fitness",""])
    table.add_row(["21.00 - 22.00","","","","","","",""])
    table.add_row(["22.00 - 23.00","","","","","","",""])
    return table
