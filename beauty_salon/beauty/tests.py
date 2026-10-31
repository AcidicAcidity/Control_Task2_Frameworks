from django.test import SimpleTestCase
from django.urls import reverse


class PagesTest(SimpleTestCase):
    def test_home_has_count(self):
        r = self.client.get("/")
        self.assertContains(r, "Всего визитов: <strong>9</strong>")

    def test_cabinets(self):
        self.assertContains(self.client.get("/cabinets/"), "Кабинет 1")

    def test_filter_differs(self):
        a = len(self.client.get("/beauty/?clients=1").context["visits"])
        b = len(self.client.get("/beauty/?clients=3").context["visits"])
        self.assertEqual((a, b), (9, 2))

    def test_empty_filter(self):
        self.assertContains(self.client.get("/beauty/?clients=99"), "не найдено")

    def test_sort_limit(self):
        v = self.client.get("/beauty/?sort=clients_desc&limit=2").context["visits"]
        self.assertEqual([x["clients"] for x in v], [4, 3])

    def test_bad_sort_is_safe(self):
        self.assertEqual(self.client.get("/beauty/?sort=1;DROP TABLE beauty").status_code, 200)

    def test_detail_and_404(self):
        self.assertContains(self.client.get(reverse("beauty:visit_detail", args=["haircut-styling"])), "Кабинет 1")
        self.assertEqual(self.client.get("/beauty/nope/").status_code, 404)

    def test_statistics_before_slug(self):
        r = self.client.get("/beauty/statistics/")
        self.assertContains(r, "Статистика визитов")
        self.assertEqual({x["service_type"] for x in r.context["stats"]}, {"стрижка", "маникюр"})
