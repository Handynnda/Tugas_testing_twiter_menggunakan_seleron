import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# --- GANTI DENGAN KREDENSIAL AKUN TES ANDA ---
USERNAME_ANDA = "hndynnd"
PASSWORD_BENAR = "Faraamanda01"
PASSWORD_SALAH = "PasswordSalah123"
# ---------------------------------------------

def setup_driver():
    """Mengatur dan menginisialisasi Chrome WebDriver dengan options."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def do_login(driver, username, password):
    """Fungsi reusable untuk melakukan proses login."""
    try:
        driver.get("https://x.com/login")
        print("INFO: Membuka/Me-reset halaman login X.com.")

        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
        )
        print(f"INFO: Memasukkan username: {username}")
        username_input.send_keys(username)

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Next')]"))
        )
        next_button.click()
        print("INFO: Mengklik tombol 'Next'.")

        password_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='password']"))
        )
        print("INFO: Memasukkan password...")
        password_input.send_keys(password)

        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
        )
        login_button.click()
        print("INFO: Mengklik tombol 'Log in'.")
        return True
    except TimeoutException as e:
        print(f"FAIL: Elemen login tidak ditemukan atau tidak bisa diklik. Error: {e}")
        return False

def test_scenario_1_login_gagal(driver):
    """Skenario 1: Gagal login dengan password salah."""
    print("\n" + "="*50)
    print("INFO: Memulai Skenario 1: Login Gagal (Password Salah)")
    print("="*50)

    if not do_login(driver, USERNAME_ANDA, PASSWORD_SALAH):
        return

    try:
        error_message = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Wrong password!') or contains(text(), 'The username and password you entered did not match')]"))
        )
        if error_message:
            print(f"PASS: Validasi berhasil. Pesan error ditemukan: '{error_message.text}'")
        else:
            print("FAIL: Pesan error tidak ditemukan.")
    except TimeoutException:
        print("FAIL: Pesan error tidak muncul dalam waktu yang ditentukan.")

def test_scenario_2_login_berhasil(driver):
    """Skenario 2: Berhasil login dengan kredensial yang benar."""
    print("\n" + "="*50)
    print("INFO: Memulai Skenario 2: Login Berhasil")
    print("="*50)

    if not do_login(driver, USERNAME_ANDA, PASSWORD_BENAR):
        return

    try:
        print("INFO: Menunggu halaman Beranda dimuat (maksimal 30 detik)...")
        post_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[@data-testid='SideNav_NewTweet_Button']"))
        )
        if post_button:
            print("PASS: Validasi berhasil. Tombol 'Post' ditemukan, menandakan berhasil login dan berada di halaman Beranda.")
        else:
            print("FAIL: Gagal memvalidasi halaman Beranda.")
    except TimeoutException:
        print("FAIL: Tombol 'Post' tidak ditemukan. Halaman Beranda tidak termuat atau ada halaman verifikasi tambahan.")

def test_scenario_2b_search_android_developer(driver):
    """Skenario tambahan: Mencari 'android developer' setelah login berhasil."""
    print("\n" + "="*50)
    print("INFO: Melanjutkan dengan pencarian 'android developer'")
    print("="*50)
    try:
        # Tunggu search bar muncul
        search_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//input[@data-testid='SearchBox_Search_Input']"))
        )
        search_input.send_keys("android developer")
        search_input.send_keys(Keys.ENTER)
        print("INFO: Kata kunci diketik dan ENTER ditekan.")

        # Tunggu hasil muncul
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//span[text()='Top'] | //span[text()='Latest']"))
        )
        print("PASS: Hasil pencarian muncul. Menunggu 5 detik untuk observasi...")
        time.sleep(5)
    except TimeoutException:
        print("FAIL: Tidak dapat menemukan kolom search atau hasil pencarian.")

def test_scenario_3_logout(driver):
    """Skenario 3: Logout dari aplikasi."""
    print("\n" + "="*50)
    print("INFO: Memulai Skenario 3: Logout")
    print("="*50)

    try:
        print("INFO: Mencari tombol menu akun...")
        account_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='SideNav_AccountSwitcher_Button']"))
        )
        print("INFO: Tombol menu akun ditemukan. Mengklik...")
        account_button.click()
        
        print("INFO: Menunggu animasi menu (1 detik)...")
        time.sleep(1)

        print("INFO: Mencari link/teks 'Keluar' (/logout)...")
        logout_link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[@href='/logout']"))
        )
        print("INFO: Link 'Keluar' ditemukan. Mengklik...")
        logout_link.click()

        # 3. Mencari tombol "Keluar" atau "Log out"
        print("INFO: Mencari tombol konfirmasi 'Keluar' dengan cara paling direct...")
        confirm_logout_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Keluar' or text()='Log out']]"))
        )
        print("INFO: Tombol konfirmasi ditemukan. Mengklik...")
        confirm_logout_button.click()

        print("INFO: Memvalidasi halaman setelah logout...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Sign in to X')]"))
        )
        print("PASS: Validasi berhasil. Berhasil logout dari aplikasi.")
    except TimeoutException:
        print("FAIL: Gagal melakukan proses logout karena elemen tidak ditemukan atau tidak bisa diklik.")

# --- MAIN EXECUTION ---
if __name__ == "__main__":
    driver = setup_driver()
    try:
        test_scenario_1_login_gagal(driver)
        time.sleep(3)
        test_scenario_2_login_berhasil(driver)
        time.sleep(3)
        test_scenario_2b_search_android_developer(driver)
        time.sleep(3)
        test_scenario_3_logout(driver)
        print("\n" + "="*50)
        print("INFO: Semua skenario pengujian telah selesai dijalankan.")
        print("="*50)
    finally:
        time.sleep(5)
        driver.quit()
        print("INFO: Browser telah ditutup.")
