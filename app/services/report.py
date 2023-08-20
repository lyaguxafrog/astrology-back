import kerykeion
from kerykeion import Report, AstrologicalSubject

def astr_report(name: str, year: int, month: int, day: int, hour: int, minute: int, city: str):
    human = AstrologicalSubject(name, year, month, day, hour, minute, city, nation='RU')
    report = Report(human)
    

    report_text = str(report.get_full_report())  # Преобразование объекта отчета в строку
    return report_text

