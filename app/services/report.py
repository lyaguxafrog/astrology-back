import kerykeion
from kerykeion import Report, AstrologicalSubject

def astr_report(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    human = AstrologicalSubject(name, year, month, day, hour, minute, city, nation='RU')
    report = Report(human)
    
    report_text = f"+- Kerykeion report for {name} -+\n"
    report_text += str(report.get_full_report())  # Преобразование объекта отчета в строку
    return report_text


# print(astr_report('Адриан', 2010,  10, 10, 10, 10, 'Москва'))