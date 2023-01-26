import unittest

from wikiracing import WikiRacer


class WikiRacerTest(unittest.TestCase):
    racer = WikiRacer()

    def test_1(self):

        path = self.racer.find_path('Дружба', 'Рим')
        self.assertEqual(path, ['Дружба', 'Якопо Понтормо', 'Рим'])
        if path == ['Дружба', 'Якопо Понтормо', 'Рим']:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_2(self):
        path = self.racer.find_path('Мітохондріальна ДНК', 'Вітамін K')
        self.assertEqual(path, ['Мітохондріальна ДНК', 'Бактерії',
                                'Вітамін K'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_3(self):
        path = self.racer.find_path('Марка (грошова одиниця)',
                                    'Китайський календар')
        self.assertEqual(path, ['Марка (грошова одиниця)', '2017',
                                'Китайський календар'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_4(self):
        path = self.racer.find_path('Фестиваль', 'Пілястра')
        self.assertEqual(path, ['Фестиваль', 'Бароко', 'Пілястра'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_5(self):
        path = self.racer.find_path('Дружина (військо)', '6 жовтня')
        self.assertEqual(path, ['Дружина (військо)', 'Друга світова війна',
                                '6 жовтня'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_6(self):
        path = self.racer.find_path('Азорські острови', 'Егейське море')
        self.assertEqual(path, ['Азорські острови', 'Архіпелаг',
                                'Егейське море'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_7(self):
        path = self.racer.find_path('Андроїд', 'Математична модель')
        self.assertEqual(path, ['Андроїд', 'Робототехніка',
                                'Математична модель'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_8(self):
        path = self.racer.find_path('Адольф Гітлер', 'Київ')
        self.assertEqual(path, ['Адольф Гітлер', '1934', 'Київ'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_9(self):
        path = self.racer.find_path('Джеймс Клерк Максвелл',
                                    'Світова спадщина ЮНЕСКО')
        self.assertEqual(path, ['Джеймс Клерк Максвелл', 'Единбург',
                                'Світова спадщина ЮНЕСКО'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")

    def test_10(self):
        path = self.racer.find_path('Бразиліа', 'Антилія')
        self.assertEqual(path, ['Бразиліа', 'Бразилія', 'Антилія'])
        if path is not None:
            print(f"[+] Passed\n Your path is - {path}")
        else:
            print(f"[-] Not Passed")


if __name__ == '__main__':
    unittest.main()
