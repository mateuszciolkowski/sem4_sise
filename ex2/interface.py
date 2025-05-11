import sys
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import pandas as pd
from mlp import MLP
from data import *
from utils import *


class Interface:

    def __init__(self):
        self.log_inputs = True
        self.log_output_values = True
        self.log_desired_output = True
        self.log_output_errors = True
        self.log_hidden_values = True
        self.mlp = None  # Początkowo brak sieci
        self.menu()

    def menu(self):
        while True:
            print("\n=== Menu Główne ===")
            print("1. Stwórz nową sieć")
            print("2. Wczytaj istniejącą sieć")
            print("3. Wyjście")
            print("==================")

            try:
                action = input("Wybierz opcję (1-3): ")
                if action == "1":
                    self.create_network()
                elif action == "2":
                    self.load_network()
                elif action == "3":
                    print("Do widzenia!")
                    break
                else:
                    print("\nBłąd: Wybierz opcję od 1 do 3.")
            except Exception as e:
                print(f"\nWystąpił błąd: {str(e)}")

    def menu_2(self):
        """Interfejs do konfiguracji i trenowania sieci"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        while True:
            print("\n=== Konfiguracja Sieci ===")
            print("1. Ustawienia sieci")
            print("2. Trenuj sieć Irysów")
            print("3. Testuj sieć Irysów")
            print("4. Trenuj sieć Autoasocjacji")
            print("5. Testuj sieć Autoasocjacji")
            print("6. Zapisz sieć")
            print("7. Wczytaj sieć")
            print("8. Utwórz nową sieć")
            print("9. Ustawienia logowania do plików")
            print("10. Wyjście")
            print("===================")

            try:
                action = input("Wybierz opcję (1-8): ")
                if action == '1':
                    self.configure_network()
                elif action == '2':
                    self.train_iris_network()
                elif action == '3':
                    self.test_iris_network(data_filled=False)
                elif action == '4':
                    self.train_autoassociation_network()
                elif action == '5':
                    self.test_autoassociation_network()
                elif action == '6':
                    self.save_network()
                elif action == '7':
                    self.load_network()
                elif action == '8':
                    self.create_network()
                elif action == '9':
                    self.logging_settings()
                elif action == '10':
                    sys.exit()
                else:
                    print("Nieprawidłowa opcja. Wybierz 1-8.")
            except Exception as e:
                print(f"Wystąpił błąd: {str(e)}")

    def create_network(self):
        print("\n=== Tworzenie nowej sieci ===")
        while True:
            try:
                num_hidden = []
                # Parametry sieci do wprowadzenia
                num_inputs = int(input("Podaj liczbę wejść: "))
                num_layers_count = int(input("Podaj ilosc warstw ukrytych: "))
                for i in range(num_layers_count):
                    num_hidden.append(int(input(f"Podaj liczbę neuronów w warstwie ukrytej nr {i + 1} ukrytych: ")))
                num_outputs = int(input("Podaj liczbę wyjść: "))
                bias = float(input("Podaj wartość biasu (jeśli nie napisz 0.0): "))

                # Tworzymy sieć
                self.mlp = MLP(layer_sizes=[num_inputs] + num_hidden + [num_outputs],
                               activation_function=sigmoid,
                               activation_derivative=sigmoid_derivative,
                               bias=bias)

                break

            except Exception as e:
                print(f"Błąd: {str(e)}")

        self.menu_2()

    def load_network(self):
        print("\n=== Wczytywanie istniejącej sieci ===")
        try:
            filename = input("Podaj nazwę pliku z wytrenowaną siecią: ")
            self.mlp = MLP.load_from_file(filename, sigmoid, sigmoid_derivative)
            print("Pomyślnie załadowano sieć")
            self.menu_2()
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {filename}")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania: {str(e)}")

    def configure_network(self):
        """Konfiguracja sieci (liczba warstw, neuronów, bias itp.)"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        while True:
            print("\n=== Aktualna konfiguracja ===")
            print(f"1. Liczba wejść: {self.mlp.layer_sizes[0]}")
            print("2. Liczba neuronów w warstwach ukrytych:")
            for i, size in enumerate(self.mlp.layer_sizes[1:-1], start=1):
                print(f"   {i}) Warstwa ukryta {i}: {size}")
            print(f"3. Liczba wyjść: {self.mlp.layer_sizes[-1]}")
            print(f"4. Bias: {self.mlp.bias}")
            print("5. Zmień pełną strukturę warstw")
            print("0. Wróć do menu")
            print("===================")

            try:
                choice = input("Wybierz numer parametru do zmiany: ")
                if choice == '1':
                    new_inputs = int(input("Podaj nową liczbę wejść: "))
                    self.mlp.layer_sizes[0] = new_inputs
                elif choice == '2':
                    hidden_count = len(self.mlp.layer_sizes) - 2
                    for i in range(hidden_count):
                        neurons = int(input(f"Podaj nową liczbę neuronów w warstwie ukrytej {i + 1}: "))
                        self.mlp.layer_sizes[i + 1] = neurons
                elif choice == '3':
                    new_outputs = int(input("Podaj nową liczbę wyjść: "))
                    self.mlp.layer_sizes[-1] = new_outputs
                elif choice == '4':
                    self.mlp.bias = float(input("Podaj nową wartość biasu: "))
                elif choice == '5':
                    print("Podaj nową strukturę sieci (np. 4,5,3,2 dla 4 wejść, 2 ukryte warstwy i 2 wyjścia):")
                    structure_str = input("Nowa struktura: ")
                    sizes = [int(x.strip()) for x in structure_str.split(",")]
                    if len(sizes) < 2:
                        print("Sieć musi mieć co najmniej warstwę wejściową i wyjściową!")
                    else:
                        self.mlp.layer_sizes = sizes
                        print("Zmieniono strukturę sieci.")
                elif choice == '0':
                    break
                else:
                    print("Nieprawidłowa opcja. Wybierz ponownie.")
            except Exception as e:
                print(f"Wystąpił błąd: {str(e)}")

    def train_iris_network(self):
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        if self.mlp.layer_sizes[0] != 4 or self.mlp.layer_sizes[-1] != 3:
            print("Sieć nie jest skonfiugrowana pod zbiór irysów wejściowe 4 neurony wyjściowe 3 neurony")
            return

        dataset_path = "data/iris/iris.data"
        X, y = load_iris(dataset_path, standarded=True)

        try:
            test_learning_rate = float(input("Podaj learning rate: "))
            test_use_momentum = input(f"Czy uwzględnić momentum? (tak/nie): ").strip().lower()
            if test_use_momentum in ['tak', 't', 'yes', 'y']:
                test_momentum = float(input("Podaj momentum: "))
            else:
                test_momentum = 0.0
            test_epochs = int(input("Podaj liczbe epok: "))
            test_error_threshold = float(input("Podaj błąd: "))
            test_log_interval = float(input("Podaj interwał błedu: "))
            test_max_no_improvement_epochs = int(input("Podaj liczbe epok do zatrzymanie bez poprawy wyniku: "))

            test_shuffle = input(f"Czy podawać dane w losowej kolejności? (tak/nie): ").strip().lower()
            if test_shuffle in ['tak', 't', 'yes', 'y']:
                test_shuffle = True
            elif test_shuffle in ['nie', 'n', 'no']:
                test_shuffle = False
            test_size = float(input("Podaj procent danych testowych (0.1-0.9): "))

            if 0.1 <= test_size <= 0.9:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)
            else:
                raise ValueError("Wartość musi być z przedziału [0.1, 0.9]")

            generate_plot = input(f"Czy generować krzywą błedu? (tak/nie): ").strip().lower()
            if generate_plot in ['tak', 't', 'yes', 'y']:
                print("\nRozpoczynanie treningu...")
                plot_error_curve(self.mlp.train(X_train, y_train, epochs=test_epochs, shuffle=test_shuffle,
                                                error_threshold=test_error_threshold, use_momentum=test_use_momentum,
                                                momentum=test_momentum,
                                                max_no_improvement_epochs=test_max_no_improvement_epochs,
                                                log_interval=test_log_interval, learning_rate=test_learning_rate))
            elif generate_plot in ['nie', 'n', 'no']:
                print("\nRozpoczynanie treningu...")
                self.mlp.train(X_train, y_train, epochs=test_epochs, shuffle=test_shuffle,
                               error_threshold=test_error_threshold, use_momentum=test_use_momentum,
                               momentum=test_momentum, max_no_improvement_epochs=test_max_no_improvement_epochs,
                               log_interval=test_log_interval, learning_rate=test_learning_rate)
            print("\nTrening zakończony!")

            test_iris_move_forward = input(f"Czy przetestować ? (tak/nie): ").strip().lower()
            if test_iris_move_forward in ['tak', 't', 'yes', 'y']:
                self.test_iris_network(data_filled=True, iris_x_test=X_test, iris_y_test=y_test)
            elif test_iris_move_forward in ['nie', 'n', 'no']:
                return

            # self.mlp.save_log_of_learning(self.mlp.log_interval, "network_log.json")

        except Exception as e:
            print(f"Wystąpił błąd: {str(e)}")

    def test_iris_network(self, data_filled, iris_x_test=None, iris_y_test=None):
        # Sprawdzenie czy sieć jest załadowana
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        # Sprawdzenie czy sieć pasuje do zbioru irysów
        if self.mlp.layer_sizes[0] != 4 or self.mlp.layer_sizes[-1] != 3:
            print("Sieć nie jest skonfigurowana pod zbiór irysów (4 wejścia, 3 wyjścia).")
            return

        try:
            # Czyszczenie logów
            clear_log_file("predict_log.json")
            clear_log_file("weights_log.json")

            if data_filled:
                # Zakładamy, że dane testowe są podane jako argumenty
                X_test = iris_x_test
                y_test = iris_y_test
            else:
                # Wczytanie zbioru z pliku
                dataset_path = "data/iris/iris.data"
                X, y = load_iris(dataset_path, standarded=True)

                test_size = float(input("Podaj procent danych testowych (0.1-0.9): "))
                if not 0.1 <= test_size <= 0.9:
                    raise ValueError("Wartość musi być z przedziału [0.1, 0.9]")

                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)

            # Ustal prawdziwe etykiety — jeśli one-hot, to przekształć
            y_true = np.argmax(y_test, axis=1) if y_test.ndim > 1 else y_test

            # Predykcja z logowaniem
            outputs = self.mlp.predict_with_logging(
                X_test, y_true,
                log_inputs=self.log_inputs,
                log_output_values=self.log_output_values,
                log_desired_output=self.log_desired_output,
                log_output_errors=self.log_output_errors,
                log_hidden_values=self.log_hidden_values
            )

            y_pred = np.argmax(outputs, axis=1)

            # Przykład danych
            class_names = ['setosa', 'versicolor', 'virginica']
            cm = confusion_matrix(y_true, y_pred)  # <- Twoja macierz pomyłek

            # Tworzymy DataFrame z nazwami klas
            cm_df = pd.DataFrame(cm, index=class_names, columns=class_names)

            # Liczba poprawnie sklasyfikowanych obiektów w każdej klasie (elementy na diagonali)
            correct_per_class = np.diag(cm)
            total_correct = correct_per_class.sum()

            # Wyświetlenie wyników
            print("Macierz pomyłek:\n", cm_df)
            print("\nPoprawnie sklasyfikowane obiekty (w rozbiciu na klasy):")
            for name, correct in zip(class_names, correct_per_class):
                print(f"{name}: {correct}")

            print(f"\nŁączna liczba poprawnie sklasyfikowanych obiektów: {total_correct}")

            print("\nRaport klasyfikacji:")
            print(classification_report(
                y_true, y_pred,
                target_names=["setosa", "versicolor", "virginica"],
                zero_division=1
            ))

        except Exception as e:
            print(f"Wystąpił błąd: {e}")

    def train_autoassociation_network(self):
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        if self.mlp.layer_sizes[0] != 4 or self.mlp.layer_sizes[1] != 2 or self.mlp.layer_sizes[-1] != 4 or len(
                self.mlp.layer_sizes) != 3:
            print("Sieć nie jest skonfiugrowana pod sieć typu autoenkoder 4, 2, 4")

        try:
            test_learning_rate = float(input("Podaj learning rate: "))
            test_use_momentum = input(f"Czy uwzględnić momentum? (tak/nie): ").strip().lower()
            if test_use_momentum in ['tak', 't', 'yes', 'y']:
                test_momentum = float(input("Podaj momentum: "))
            else:
                test_momentum = 0.0
            test_epochs = int(input("Podaj liczbe epok: "))
            test_error_threshold = float(input("Podaj błąd: "))
            test_log_interval = float(input("Podaj interwał błedu: "))
            test_max_no_improvement_epochs = int(input("Podaj liczbe epok do zatrzymanie bez poprawy wyniku: "))

            test_shuffle = input(f"Czy podawać dane w losowej kolejności? (tak/nie): ").strip().lower()
            if test_shuffle in ['tak', 't', 'yes', 'y']:
                test_shuffle = True
            elif test_shuffle in ['nie', 'n', 'no']:
                test_shuffle = False

            X, Y = load_auto_association()
            generate_plot = input(f"Czy generować krzywą błedu? (tak/nie): ").strip().lower()
            if generate_plot in ['tak', 't', 'yes', 'y']:
                print("\nRozpoczynanie treningu...")
                plot_error_curve(self.mlp.train(X, Y, epochs=test_epochs, shuffle=test_shuffle,
                                                error_threshold=test_error_threshold,
                                                use_momentum=test_use_momentum,
                                                momentum=test_momentum,
                                                max_no_improvement_epochs=test_max_no_improvement_epochs,
                                                log_interval=test_log_interval, learning_rate=test_learning_rate))
            elif generate_plot in ['nie', 'n', 'no']:
                print("\nRozpoczynanie treningu...")
                self.mlp.train(X, Y, epochs=test_epochs, shuffle=test_shuffle,
                               error_threshold=test_error_threshold, use_momentum=test_use_momentum,
                               momentum=test_momentum, max_no_improvement_epochs=test_max_no_improvement_epochs,
                               log_interval=test_log_interval, learning_rate=test_learning_rate)
            print("\nTrening zakończony!")
            test_move_forward = input(f"Czy przetestować ? (tak/nie): ").strip().lower()

            if test_move_forward in ['tak', 't', 'yes', 'y']:
                self.test_autoassociation_network()
            elif test_move_forward in ['nie', 'n', 'no']:
                return
        except Exception as e:
            print(f"Wystąpił błąd: {e}")
        return

    def test_autoassociation_network(self):
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        if self.mlp.layer_sizes[0] != 4 or self.mlp.layer_sizes[1] != 2 or self.mlp.layer_sizes[-1] != 4 or len(
                self.mlp.layer_sizes) != 3:
            print("Sieć nie jest skonfigurowana pod autoenkoder 4-2-4.")
            return

        print("\nWybierz dane do testowania autoenkodera:")
        print("1. Użyj oryginalnego zbioru danych")
        print("2. Wprowadź własne dane wejściowe")

        try:
            choice = input("Twój wybór (1/2): ").strip()
        except Exception as e:
            print(f"Błąd wejścia: {e}")
            return

        patterns = []

        if choice == "1":
            try:
                X, Y = load_auto_association()
                patterns = Y
            except Exception as e:
                print(f"Błąd ładowania danych: {e}")
                return

        elif choice == "2":
            print("Podaj dane wejściowe (cztery liczby oddzielone spacjami, np. 1 0 0 0):")
            while True:
                try:
                    user_input = input("Wprowadź dane (lub 'q' aby zakończyć): ").strip()
                    if user_input.lower() == 'q':
                        break
                    values = list(map(float, user_input.split()))
                    if len(values) != 4:
                        print("Podaj dokładnie 4 liczby.")
                        continue
                    patterns.append(values)
                except ValueError:
                    print("Nieprawidłowy format liczb. Spróbuj ponownie.")
                except Exception as e:
                    print(f"Wystąpił nieoczekiwany błąd: {e}")
        else:
            print("Nieprawidłowy wybór.")
            return

        for pattern in patterns:
            try:
                clear_log_file("predict_log.json")
                clear_log_file("weights_log.json")
                outputs = self.mlp.predict_with_logging([pattern],
                                                        log_inputs=self.log_inputs,
                                                        log_output_values=self.log_output_values,
                                                        log_desired_output=self.log_desired_output,
                                                        log_output_errors=self.log_output_errors,
                                                        log_hidden_values=self.log_hidden_values)
                formatted_output = [f"{float(val):.5f}" for val in outputs[0]]
                print(f"Wejście: {pattern} -> Wyjście: {formatted_output}")
            except Exception as e:
                print(f"Błąd podczas predykcji dla wzorca {pattern}: {e}")

    def save_network(self):
        """Zapisanie sieci do pliku"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        try:
            filename = input("Podaj nazwę pliku do zapisania: ")
            self.mlp.save_to_file(filename)
            print(f"Sieć została zapisana w pliku: {filename}")
        except Exception as e:
            print(f"Wystąpił błąd przy zapisywaniu sieci: {str(e)}")

    def logging_settings(self):
        while True:
            print("\n=== Ustawienia logowania ===")
            print(f"1. Rejestruj wzorzec wejściowy: {self.log_inputs}")
            print(f"2. Rejestruj wartości wyjściowe neuronów wyjściowych: {self.log_output_values}")
            print(f"3. Rejestruj pożądany wzorzec odpowiedzi: {self.log_desired_output}")
            print(f"4. Rejestruj błędy na poszczególnych wyjściach i całkowity błąd: {self.log_output_errors}")
            print(f"5. Rejestruj wartości i wagi neuronów ukrytych: {self.log_hidden_values}")
            print(f"6. Wyjście")

            choice = input("Wybierz numer ustawienia do zmiany (1-6): ")

            if choice == "6":
                break
            elif choice in {"1", "2", "3", "4", "5"}:
                response = input("Podaj nową wartość (tak / nie): ").strip().lower()
                if response not in {"tak", "nie"}:
                    print("Nieprawidłowa wartość. Podaj 'tak' lub 'nie'.")
                    continue

                new_value = response == "tak"

                if choice == "1":
                    self.log_inputs = new_value
                elif choice == "2":
                    self.log_output_values = new_value
                elif choice == "3":
                    self.log_desired_output = new_value
                elif choice == "4":
                    self.log_output_errors = new_value
                elif choice == "5":
                    self.log_hidden_values = new_value

                print("Zmieniono ustawienie.\n")
            else:
                print("Nieprawidłowy numer. Wybierz od 1 do 6.")