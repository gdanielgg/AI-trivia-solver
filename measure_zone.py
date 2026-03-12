import pyautogui
import time

print("Muta mouse-ul in coltul STANGA-SUS al intrebarii.")
print("Ai 5 secunde sa ajungi acolo!")
time.sleep(5)

x, y = pyautogui.position()
print(f"--> NOTEAZA ACESTE NUMERE: X={x}, Y={y}")

print("\nAcum muta mouse-ul in coltul DREAPTA-JOS al intrebarii.")
print("Ai 5 secunde!")
time.sleep(5)

x2, y2 = pyautogui.position()
latime = x2 - x
inaltime = y2 - y

print(f"--> NOTEAZA SI ASTA: Latime={latime}, Inaltime={inaltime}")
input("Apasa Enter ca sa inchizi...")
