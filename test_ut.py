from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import unittest

class Test(unittest.TestCase):

    @classmethod
    def setUp(self):
        global driver
        driver = webdriver.Chrome('./driver/chromedriver.exe')
        driver.maximize_window()
        driver.delete_all_cookies()
        driver.get("http://yandex.ru")

    def tearDown(self):
        driver.close()
        driver.quit()

    def test_avtodispetcher(self):
        window_before = driver.window_handles[0]
        driver.find_element(By.ID, 'text').send_keys('расчет расстояний между городами')
        driver.find_element(By.XPATH, '//div[@class="search2__button"]').click()
        driver.implicitly_wait(5)
        driver.find_element(By.XPATH, '//a[starts-with(@href, "https://www.avtodispetcher.ru")]').click()
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        assert driver.title == 'Расчет расстояний между городами'
        print('Произведен вход на сайт www.avtodispetcher.ru')
        driver.implicitly_wait(5)
        driver.execute_script("window.scrollBy(0,500)", "")
        driver.find_element(By.NAME, 'from').send_keys('Тула')
        driver.find_element(By.NAME, 'to').send_keys('Санкт-Петербург')
        driver.find_element(By.NAME, 'fc').clear()
        driver.find_element(By.NAME, 'fc').send_keys('9')
        driver.find_element(By.NAME, 'fp').clear()
        driver.find_element(By.NAME, 'fp').send_keys('46')
        driver.find_element(By.XPATH, '//div[@class="submit_button"]//input').click()
        driver.implicitly_wait(5)
        print('Данные о маршруте "г. Тула - г. Санкт-Петербург": ')
        distance = driver.find_element(By.XPATH, '//span[@id="totalDistance"]')
        assert distance.text == '897'
        print('Расстояние:' + distance.text + 'км')
        EC.text_to_be_present_in_element((By.ID, 'f_fp'), '3726')
        print('Цена: 3726 руб.')
        driver.execute_script("window.scrollBy(0,500)", "")
        driver.implicitly_wait(5)
        el = driver.find_element(By.ID, 'triggerFormD')
        hover = ActionChains(driver).move_to_element(el)
        hover.perform()
        el.click()
        driver.find_element(By.NAME, 'v')
        driver.find_element(By.NAME, 'v').clear()
        driver.find_element(By.NAME, 'v').send_keys('Великий Новгород')
        print('В маршрут добавлен Великий Новгород')
        driver.implicitly_wait(60)
        subButton = driver.find_element(By.XPATH, '//div[@class="submit_button"]//input')
        driver.execute_script("arguments[0].scrollIntoView();", subButton)
        subButton.click()
        print('Данные о маршруте "г. Тула - г. Великий Новгород - г. Санкт-Петербург": ')
        distance2 = driver.find_element(By.XPATH, '//span[@id="totalDistance"]')
        assert distance2.text == '966'
        print('Новое расстояние: ' + distance2.text + 'км')
        EC.text_to_be_present_in_element((By.ID, 'f_fp'), '4002')
        print('Новая цена: 4002 руб.')
        print('Тест завершен успешно')

if __name__ == "__main__":
    unittest.main()
