#from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase 

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import sys
#import unittest

#class NewVisitorTest(unittest.TestCase):
#class NewVisitorTest(LiveServerTestCase):
class NewVisitorTest(StaticLiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		for arg in sys.argv:
			if 'liveserver' in arg:
				cls.server_url = 'http://' + arg.split('=')[1]
				return
		super().setUpClass()
		cls.server_url = cls.live_server_url

	@classmethod
	def tearDownClass(cls):
		if cls.server_url == cls.live_server_url:
			super().tearDownClass()

	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
		
	def tearDown(self):
		self.browser.refresh()
		self.browser.quit()

	#text_ 외의 이름을 사용해서 사용자 정의 메소드를 만들 수 있음.
	#helper 메소드로 표현함.
	def check_for_row_in_list_table(self, row_text):
		table=self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		#self.browser.get('http://localhost:8000')
		#self.browser.get(self.live_server_url)
		self.browser.get(self.server_url)

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('작업 목록', header_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(inputbox.get_attribute('placeholder'), '작업 아이템 입력')

		inputbox.send_keys('공작깃털 사기')

		inputbox.send_keys(Keys.ENTER)

		edith_list_url = self.browser.current_url
		self.assertRegex(edith_list_url, '/lists/.+')

		#table = self.browser.find_element_by_id('id_list_table')
		#rows = table.find_elements_by_tag_name('tr')
		#self.assertTrue(any(row.text == '1: 공작깃털 사기' for row in  rows),
		#	"신규 작업이 테이블에 표시되지 않는다 -- 해당 텍스트:\n%s" % (table.text,))
		#self.assertIn('1: 공작깃털 사기', [row.text for row in rows])
		self.check_for_row_in_list_table('1: 공작깃털 사기')

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('공작깃털을 이용해서 그물 만들기')
		inputbox.send_keys(Keys.ENTER)
		#페이지 갱신됨
		#table = self.browser.find_element_by_id('id_list_table')
		#rows = table.find_elements_by_tag_name('tr')
		#self.assertIn('1: 공작깃털 사기', [row.text for row in rows])
		#self.assertIn('2: 공작깃털을 이용해서 그물 만들기', [row.text for row in rows])
		self.check_for_row_in_list_table('2: 공작깃털을 이용해서 그물 만들기')
		self.check_for_row_in_list_table('1: 공작깃털 사기')

		
		##새로운 브라우저 세션을 이요해서 에디스의 정보가
		##쿠키를 통해 유입되는 것을 방지한다.
		self.browser.quit()
		self.browser = webdriver.Firefox()

		#self.browser.get(self.live_server_url)
		self.browser.get(self.server_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('공작깃털 사기', page_text)
		self.assertNotIn('그물 만들기', page_text)

		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('우유 사기')
		inputbox.send_keys(Keys.ENTER)

		francis_list_url = self.browser.current_url
		self.assertRegex(francis_list_url, '/lists/.+')
		self.assertNotEqual(francis_list_url, edith_list_url)

		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('공작깃털 사기', page_text)
		self.assertIn('우유 사기', page_text)


		self.fail('Finish the test!')

	#테스트 실행자를 통해 실행
	#def test_can_start_a_list_and_retrieve_it_later2(self):
	#	self.browser.get(self.live_server_url)

#파일 직접 호출시 아래 구문 필요
#예를 들어, python functional_test.py 라는 식으로 호출시에는 아래 구문 필요
#if __name__ == '__main__':
#	unittest.main(warnings='ignore')

	def test_layout_and_styling(self):
		
		#self.browser.get(self.live_server_url)
		self.browser.get(self.server_url)

		self.browser.set_window_size(1024, 768)

		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x']+inputbox.size['width'] / 2,
			512,
			delta=10)
		
		# 그녀는 새로운 리스트를 시작하고 입력 상자가
		# 가운데 배치된 것을 확인한다
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=10
		)