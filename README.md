(馃敶 Projekt jest w fazie rozwoju)

# Wst臋p
SLASH jest aplikacj膮 webow膮 zbudowan膮 za pomoc膮 Python frameworku Django. G艂贸wnym celem tej aplikacji jest 艣ledzenie wydatk贸w i zobowi膮za艅 finansowych pomi臋dzy u偶ytkownikami grupy.

---
### Funkcjonalno艣ci:
- Rejestracja/Logowanie/Wylogowanie
- CRUD (create/read/update/delete) wydatk贸w
- 艢ledzenie sald u偶ytkownik贸w
- Organizacja przelew贸w pieni臋偶nych
- Tworzenie/usuwanie grup (`馃敶 - niedost臋pne w tej wersji`)

### Logowanie/Rejestracja
![](readme/login.gif)

### Tworzenie wydatku
![](readme/add-expense.gif)

### Edytowanie wydatku
![](readme/edit-expense.gif)

### Rozliczenie
W celu rozliczenia swoich zaleg艂o艣ci u偶ytkownik ma mo偶liwo艣膰 u偶y膰 funkcji "settle-up". 
Po wcisni臋ciu przycisku "Settle-up" 艂aduje si臋 Django formularz z wst臋pnie uzupe艂nionymi danymi na podstawie modelu "TransferToMake".
![](readme/settle-up.gif)

### Szczeg贸艂y frameworku Django
Ten projekt jest wykonany przy u偶yciu widok贸w opartych na klasach (Class based views) i dzieli si臋 na dwie aplikacje: "users" i "groups".

**Aplikacja "users"** odpowiada za:

- Rejestracja/logowanie/wylogowywanie u偶ytkownik贸w
- Tworzenie/aktualizacja profilu
- `users/models.py` posiada model "Profile" (SQL tabela)

**Aplikacja "groups"** odpowiada za:

- CRUD (create/read/update/delete) wydatk贸w
- 艢ledzenie sald u偶ytkownik贸w
- Organizacja przelew贸w pieni臋偶nych
- Tworzenie/usuwanie grup (`馃敶 - niedost臋pne w tej wersji`)
- `groups/models.py` posiada modele przedstawione na rys. 1 poni偶ej

##### rys. 1: baza dannych
![](readme/database.png)
---
## Przetwarzanie wydatk贸w
Kiedy u偶ytkownik dodaje, edytuje lub usuwa wydatek grupowy, wszystkie salda u偶ytkownik贸w tej grupy musz膮 si臋 od艣wierzy膰. Jest to osi膮gane przez model "CashMovement", kt贸ry odpowiada za zmian臋 salda u偶ytkownika po uwzgl臋dnieniu wydatku.

Wraz ze zmianami sald zmieniaj膮 si臋 warto艣ci do przelew贸w, kt贸re s膮 obliczane na podstawie poni偶szej logiki:


1) Oblicz saldo ka偶dego u偶ytkownika i dodaj do biblioteki {'u偶ytkownik': saldo}.
`saldo = wszystkie d艂ugi u偶ytkownika w tej grupie - wszystkie po偶yczki u偶ytkownika w tej grupie`
2) Znajd藕 u偶ytkownika z najwi臋ukszym d艂ugiem i najwi臋ksz膮 po偶yczk膮 w tej bibliotece (punkt 1).
3) Je偶eli warto艣膰 najwi臋kszego d艂ugu `<=` warto艣ci najwi臋kszej po偶yczki stw贸rz "TranserToMake" i usu艅 d艂u偶nika z tej biblioteki, pomniejszaj膮c saldo po偶yczkodawcy w bibliotece o warto艣膰 tego d艂ugu
4) Je偶eli warto艣膰 najwi臋kszego d艂ugu `>` warto艣ci najwi臋kszej po偶yczki stw贸rz "TranserToMake" i usu艅 po偶yczkodawc臋 z tej biblioteki, pomniejszaj膮c saldo tego u偶ytkownika w bibliotece o warto艣膰 tej po偶yczki
5) Powtarzaj punkty 2-4 dop贸ki biblioteka (punk 1) nie b臋dzie pusta
