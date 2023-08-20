import unittest
from app.services.report import astr_report

class TestAstrologicalReport(unittest.TestCase):



    def test_report_output(self):
        self.maxDiff = None
        expected_output = (
            "+- Kerykeion report for Адриан -+\n"
            "+------------+-------+------------+-----------+----------+\n"
            "| Date       | Time  | Location   | Longitude | Latitude |\n"
            "+------------+-------+------------+-----------+----------+\n"
            "| 10/10/2010 | 10:10 | Москва, RU | 37.61556  | 55.75222 |\n"
            "+------------+-------+------------+-----------+----------+\n"
            "+-----------+------+-------+------+----------------+\n"
            "| Planet    | Sign | Pos.  | Ret. | House          |\n"
            "+-----------+------+-------+------+----------------+\n"
            "| Sun       | Lib  | 16.84 | -    | Eleventh_House |\n"
            "| Moon      | Sco  | 20.67 | -    | First_House    |\n"
            "| Mercury   | Lib  | 11.81 | -    | Eleventh_House |\n"
            "| Venus     | Sco  | 13.16 | R    | First_House    |\n"
            "| Mars      | Sco  | 17.26 | -    | First_House    |\n"
            "| Jupiter   | Pis  | 25.99 | R    | Fourth_House   |\n"
            "| Saturn    | Lib  | 8.88  | -    | Eleventh_House |\n"
            "| Uranus    | Pis  | 27.88 | R    | Fourth_House   |\n"
            "| Neptune   | Aqu  | 26.13 | R    | Third_House    |\n"
            "| Pluto     | Cap  | 2.97  | -    | Second_House   |\n"
            "| Mean_Node | Cap  | 6.69  | R    | Second_House   |\n"
            "| True_Node | Cap  | 6.15  | R    | Second_House   |\n"
            "| Chiron    | Aqu  | 26.42 | R    | Third_House    |\n"
            "+-----------+------+-------+------+----------------+\n"
            "+----------------+------+----------+\n"
            "| House          | Sign | Position |\n"
            "+----------------+------+----------+\n"
            "| First_House    | Sco  | 8.96     |\n"
            "| Second_House   | Sag  | 7.12     |\n"
            "| Third_House    | Cap  | 15.02    |\n"
            "| Fourth_House   | Aqu  | 26.64    |\n"
            "| Fifth_House    | Pis  | 28.98    |\n"
            "| Sixth_House    | Ari  | 22.0     |\n"
            "| Seventh_House  | Tau  | 8.96     |\n"
            "| Eighth_House   | Gem  | 7.12     |\n"
            "| Ninth_House    | Can  | 15.02    |\n"
            "| Tenth_House    | Leo  | 26.64    |\n"
            "| Eleventh_House | Vir  | 28.98    |\n"
            "| Twelfth_House  | Lib  | 22.0     |\n"
            "+----------------+------+----------+\n"
        )
        report_output = astr_report('Адриан', 2010, 10, 10, 10, 10, 'Москва')
        

        expected_output_cleaned = expected_output.strip().replace(' +', '+')
        report_output_cleaned = report_output.strip().replace(' +', '+')
        
        self.assertEqual(report_output_cleaned, expected_output_cleaned)


    def test_report_content(self):
        self.maxDiff = None
        report_output = astr_report('Адриан', 2010, 10, 10, 10, 10, 'Москва')
        self.assertIn("+- Kerykeion report for Адриан -+", report_output)
        self.assertIn("Sun       | Lib  | 16.84 | -    | Eleventh_House", report_output)
        self.assertIn("Neptune   | Aqu  | 26.13 | R    | Third_House", report_output)
        self.assertIn("Twelfth_House  | Lib  | 22.0     |", report_output)

    def test_invalid_input(self):
        self.maxDiff = None
        with self.assertRaises(ValueError):
            astr_report('Иван', 2023, 13, 45, 8, 30, 'Москва')

if __name__ == '__main__':
    unittest.main()