import unittest
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import InvalidSessionIdException
from selenium.common.exceptions import StaleElementReferenceException
from time import sleep
import random

capabilities = dict(
      platformName='Android',
      automationName='uiautomator2',
      appPackage='com.gosty.tryoutapp',
      appActivity='com.gosty.tryoutapp.ui.splash.SplashActivity',
      language='en',
      locale='US'
)

appium_server_url = 'http://localhost:4723'

class TestAppium(unittest.TestCase):
      def setUp(self) -> None:
            self.driver = webdriver.Remote(appium_server_url, capabilities)


      def tearDown(self) -> None:
            if self.driver:
                  self.driver.quit()
                  

      def login(self) -> None:
            self.driver.implicitly_wait(15)
            # login session
            login_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_login")
            login_btn.click()
            sleep(2)    
            google_acc = self.driver.find_element(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
            google_acc.click()
            self.driver.implicitly_wait(100)

            validate_home = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_rule_title")
            assert validate_home.is_displayed()

      def scroll(self, times, multiplier = 1) -> None:
            x = self.driver.get_window_rect()['width']
            y = self.driver.get_window_rect()['height']

            for i in range(times):
                  self.driver.swipe(x/2, multiplier*3*y/4, x/2, multiplier*1.5*y/4)

      def score_nav_btn(self) -> None:
            score_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/navigation_score")
            if score_btn.is_displayed():
                  score_btn.click()
                  self.driver.implicitly_wait(10)
                  print("Berada di halaman score")
            else :     
                  self.assertFalse(score_btn.is_displayed())

      def test_tc_26(self) -> None:
            self.login()
            mulaitest_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_start")
            mulaitest_btn.click()
            self.driver.implicitly_wait(15)
            validatetipesoalpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_title")
            if "Ada 2 (dua) tipe soal nih" in validatetipesoalpage.text:
                  print("Berhasil masuk ke halaman pilih soal")
            else:
                  print("Gagal masuk ke halaman pilih soal")

            dataketidakpastian_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_data_dan_ketidakpastian")

            if dataketidakpastian_btn.is_displayed():
                  dataketidakpastian_btn.click()
                  sleep(5)
            else:
                  print("Button tidak ditemukan")


            try:
                  next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_forward")
                  submit_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_submit")
                  # click next button until can submit
                  while submit_btn.is_enabled() == False :
                        next_btn.click()
                        sleep(0.5)

                  if submit_btn.is_enabled():
                        submit_btn.click()
                        sleep(1)
                  else :
                        print("Button belum dapat di klik")

                  confirm_btn = self.driver.find_element(MobileBy.ID, "android:id/button1")
                  confirm_btn.click()
                  self.driver.implicitly_wait(15)
            except Exception as e:
                  assert e

            validatefinishedpage_text = self.driver.find_element(MobileBy.ID,"com.gosty.tryoutapp:id/tvErrorTitle")
            if "Bravo" in validatefinishedpage_text.text:
                  print("Berhasil menyelesaikan test")
                  keberanda_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnViewScore")
                  keberanda_btn.click()
                  sleep(2)
            else:
                  print("Jawaban tidak tersubmit. Gagal menyelesaikan test")

            score_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/navigation_score")
            if score_btn.is_displayed():
                  score_btn.click()
                  self.driver.implicitly_wait(15)
            else :     
                  assert score_btn.is_displayed()
            
            scores_rv = self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.gosty.tryoutapp:id/rvScore")')
            scores_itm = scores_rv.find_elements(MobileBy.CLASS_NAME, "android.view.ViewGroup")[0]

            try:
                  while scores_itm.is_displayed():
                        scores_itm.click()
                        sleep(7)
            except StaleElementReferenceException as e:
                  self.assertTrue(False, e.msg)

      def test_tc_17(self) -> None:
            self.login()
            mulaitest_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_start")
            mulaitest_btn.click()
            self.driver.implicitly_wait(15)
            validatetipesoalpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_title")
            if "Ada 2 (dua) tipe soal nih" in validatetipesoalpage.text:
                  print("Berhasil masuk ke halaman pilih soal")
            else:
                  print("Gagal masuk ke halaman pilih soal")

            dataketidakpastian_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_data_dan_ketidakpastian")

            if dataketidakpastian_btn.is_displayed():
                  dataketidakpastian_btn.click()
                  sleep(5)
            else:
                  print("Button tidak ditemukan")

            try:
                  next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_forward")
                  submit_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_submit")
                  # click next button until can submit
                  while submit_btn.is_enabled() == False :
                        self.scroll(2)
                        multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
                        multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
                        ans_btn = random.choice(multichoice_btns[1:])
                        ans_btn.click()
                        next_btn.click()
                        sleep(0.5)

                  if submit_btn.is_enabled():
                        self.scroll(2)
                        multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
                        multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
                        ans_btn = random.choice(multichoice_btns[1:])
                        ans_btn.click()
                        sleep(0.5)
                        submit_btn.click()
                        sleep(1)
                  else :
                        print("Tidak dapat submit jawaban")
                  confirm_btn = self.driver.find_element(MobileBy.ID, "android:id/button1")
                  confirm_btn.click()
                  sleep(1)
            except Exception as e:
                  self.assertFalse(e, e.msg)

            validatefinishedpage_text = self.driver.find_element(MobileBy.ID,"com.gosty.tryoutapp:id/tvErrorTitle")
            if "Bravo" in validatefinishedpage_text.text:
                  print("Berhasil menyelesaikan test")
                  keberanda_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnViewScore")
                  keberanda_btn.click()
                  sleep(2)
            else:
                  print("Jawaban tidak tersubmit. Gagal menyelesaikan test")
            # beralih ke score page
            self.score_nav_btn()
            
            scores_rv = self.driver.find_element(MobileBy.ANDROID_UIAUTOMATOR, 'new UiSelector().resourceId("com.gosty.tryoutapp:id/rvScore")')
            scores_itm = scores_rv.find_elements(MobileBy.CLASS_NAME, "android.view.ViewGroup")[0]

            try:
                  if scores_itm.is_displayed():
                        scores_itm.click()
                        self.driver.implicitly_wait(10)
                  
                  next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnNext")
                  tipesoal_text = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tvQuestionType").text
                  
                  if tipesoal_text == "Data dan Ketidakpastian" and next_btn.is_displayed():
                        print(f"Berhasil masuk ke pembahasan soal {tipesoal_text}")
                        while next_btn.is_displayed():
                                    self.scroll(2)
                                    next_btn.click()
                                    sleep(1.5)
            except Exception as e:
                  assert e
                  sleep(1)
            finally:
                  self.driver.back()
                  print("Kembali ke halaman score")
                  sleep(3)
      
      def test_tc_08(self) -> None:
            
            print()
            print("=============================")
            print("[TC_08] Access the application without authentication")

            self.login()
            mulaitest_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_start")
            mulaitest_btn.click()
            self.driver.implicitly_wait(15)
            validatetipesoalpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_title")
            if "Ada 2 (dua) tipe soal nih" in validatetipesoalpage.text:
                  print("Berhasil masuk ke halaman pilih soal")
            else:
                  print("Gagal masuk ke halaman pilih soal")

            dataketidakpastian_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_data_dan_ketidakpastian")

            try:
                  if dataketidakpastian_btn.is_displayed():
                        dataketidakpastian_btn.click()
                        sleep(7)
                  else:
                        print("Button tidak ditemukan")
            except Exception as e:
                  self.assertTrue(False, "Button tidak ditemukan")

            try:
                  next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_forward")
                  submit_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_submit")
                  # click next button until can submit
                  while submit_btn.is_enabled() == False :
                        self.scroll(2)
                        multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
                        multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
                        ans_btn = random.choice(multichoice_btns[1:])
                        ans_btn.click()

                        next_btn.click()
                        sleep(0.5)

                  if submit_btn.is_enabled():
                        submit_btn.click()
                        sleep(1)
                  else :
                        print("Button belum dapat di klik")

                  confirm_btn = self.driver.find_element(MobileBy.ID, "android:id/button1")
                  confirm_btn.click()
                  self.driver.implicitly_wait(15)
            except Exception as e:
                  self.assertTrue(False, "Terjadi error")

            validatefinishedpage_text = self.driver.find_element(MobileBy.ID,"com.gosty.tryoutapp:id/tvErrorTitle")
            if "Bravo" in validatefinishedpage_text.text:
                  print("Berhasil menyelesaikan test")
                  keberanda_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnViewScore")
                  keberanda_btn.click()
                  sleep(2)
            else:
                  print("Jawaban tidak tersubmit. Gagal menyelesaikan test")

            profile_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/navigation_profile")
            if profile_btn .is_displayed():
                  profile_btn .click()
                  self.driver.implicitly_wait(15)

            logout_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnLogout")
            logout_btn.click()
            self.driver.implicitly_wait(5)

            confirmlogout_btn = self.driver.find_element(MobileBy.ID, "android:id/button1")
            confirmlogout_btn.click()
            sleep(2)

            self.driver.back()
            sleep(2)
            try:
                  validate_loginpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/content")
                  self.assertTrue(validate_loginpage.is_displayed(), "Dapat masuk ke aplikasi tanpa autentikasi")
            except:
                  self.assertTrue(False, "Terjadi error")
            
      def test_tc_19(self) -> None:

            print()
            print("=============================")
            print("[TC_19] Cannot go back to the test session when press the back button")
            
            self.login()
            mulaitest_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_start")
            mulaitest_btn.click()
            self.driver.implicitly_wait(15)
            validatetipesoalpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_title")
            if "Ada 2 (dua) tipe soal nih" in validatetipesoalpage.text:
                  print("Berhasil masuk ke halaman pilih soal")
            else:
                  print("Gagal masuk ke halaman pilih soal")

            dataketidakpastian_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_data_dan_ketidakpastian")

            try:
                  if dataketidakpastian_btn.is_displayed():
                        dataketidakpastian_btn.click()
                        sleep(7)
                  else:
                        print("Button tidak ditemukan")
            except Exception as e:
                  self.assertTrue(False, "Button tidak ditemukan")


            next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_forward")
            # click next button until can submit
            for i in range(4) :
                  self.scroll(2)
                  multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
                  multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
                  ans_btn = random.choice(multichoice_btns[1:])
                  ans_btn.click()

                  next_btn.click()
                  sleep(0.5)

            self.driver.back()

            try:
                  if dataketidakpastian_btn.is_displayed():
                        dataketidakpastian_btn.click()
                        sleep(7)
                  else:
                        print("Button tidak ditemukan")
            except Exception as e:
                  self.assertTrue(False, "Button tidak ditemukan")

            self.driver.implicitly_wait(3)
            current_number = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_total_problem")
            self.assertEqual(current_number.text == "(4/10)", f"Soal berada pada page {current_number.text}")

      def test_tc_22(self) -> None:

            print()
            print("=============================")
            print("[TC_22] Still continue the test although there is no internet")

            self.login()
            mulaitest_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_start")
            mulaitest_btn.click()
            self.driver.implicitly_wait(15)
            validatetipesoalpage = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tv_title")
            if "Ada 2 (dua) tipe soal nih" in validatetipesoalpage.text:
                  print("Berhasil masuk ke halaman pilih soal")
            else:
                  print("Gagal masuk ke halaman pilih soal")

            dataketidakpastian_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_data_dan_ketidakpastian")

            try:
                  if dataketidakpastian_btn.is_displayed():
                        dataketidakpastian_btn.click()
                        sleep(7)
                  else:
                        print("Button tidak ditemukan")
            except Exception as e:
                  self.assertTrue(False, "button tidak ditemukan")


            next_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_forward")
            submit_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btn_submit")
            # click next button until can submit
            self.scroll(2)
            multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
            multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
            ans_btn = random.choice(multichoice_btns[1:])
            ans_btn.click()
            next_btn.click()
            sleep(0.5)
            self.driver.set_network_connection(0)
            # wait for the internet to turning off
            sleep(5)

            for i in range(8):
                  self.scroll(2)
                  multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
                  multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
                  ans_btn = random.choice(multichoice_btns[1:])
                  ans_btn.click()
                  next_btn.click()
                  sleep(0.5)
                  
            self.driver.set_network_connection(6)
            # wait for the internet to turning on
            sleep(5)

            self.scroll(2)
            multichoice_container = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/multiple_choice_container")
            multichoice_btns = multichoice_container.find_elements(MobileBy.CLASS_NAME, "android.widget.LinearLayout")
            ans_btn = random.choice(multichoice_btns[1:])
            ans_btn.click()
            next_btn.click()

            submit_btn.click()
            sleep(1)

            confirm_btn = self.driver.find_element(MobileBy.ID, "android:id/button1")
            confirm_btn.click()
            self.driver.implicitly_wait(15)

            validatefinishedpage_text = self.driver.find_element(MobileBy.ID,"com.gosty.tryoutapp:id/tvErrorTitle")
            if "Bravo" in validatefinishedpage_text.text:
                  print("Berhasil menyelesaikan test")
                  keberanda_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/btnViewScore")
                  keberanda_btn.click()
                  sleep(2)
            else:
                  print("Jawaban tidak tersubmit. Gagal menyelesaikan test")

            score_btn = self.driver.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/navigation_score")
            if score_btn.is_displayed():
                  score_btn.click()
                  self.driver.implicitly_wait(15)
            else :     
                  self.assertTrue(False, "button tidak ditemukan")
            
            scores_itm = self.driver.find_element(MobileBy.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[1]/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[1]")
            kosong_field = scores_itm.find_element(MobileBy.ID, "com.gosty.tryoutapp:id/tvKosong").text
            self.assertEqual(kosong_field == "Kosong : 0", "Ada soal yang tidak terjawab")

if __name__ == '__main__':
      unittest.main()