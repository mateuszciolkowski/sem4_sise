from random import shuffle

from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import json

from mlp import MLP
from data import *
from utils import *


class Interface:
    def __init__(self):
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
                    self.create_network_interface()
                elif action == "2":
                    self.load_network_interface()
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
            print("8. Powrót do menu głównego")
            print("===================")

            try:
                action = input("Wybierz opcję (1-8): ")
                if action == '1':
                    self.configure_network()
                elif action == '2':
                    self.train_iris_network()
                elif action == '3':
                    self.test_iris_network()
                elif action == '4':
                    self.train_autoassociation_network()
                elif action == '5':
                    self.test_autoassociation_network()
                elif action == '6':
                    self.save_network()
                elif action == '7':
                    self.load_network_interface()
                elif action == '8':
                    return  # Powrót do menu głównego
                else:
                    print("Nieprawidłowa opcja. Wybierz 1-8.")
            except Exception as e:
                print(f"Wystąpił błąd: {str(e)}")

    def create_network_interface(self):
        print("\n=== Tworzenie nowej sieci ===")
        while True:
            try:
                num_hidden = []
                # Parametry sieci do wprowadzenia
                num_inputs = int(input("Podaj liczbę wejść: "))
                num_layers_count = int(input("Podaj ilosc warstw ukrytych: "))
                for i in range(num_layers_count):
                    num_hidden.append(int(input(f"Podaj liczbę neuronów w warstwie ukrytej nr {i+1} ukrytych: ")))
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

    def load_network_interface(self):
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
        """Trenowanie sieci na zbiorze danych Irysów"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
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
                plot_error_curve(self.mlp.train(X_train, y_train, epochs=test_epochs,shuffle=test_shuffle,
                               error_threshold=test_error_threshold, use_momentum=test_use_momentum,
                               momentum=test_momentum,max_no_improvement_epochs=test_max_no_improvement_epochs,
                               log_interval=test_log_interval, learning_rate=test_learning_rate))
            elif generate_plot in ['nie', 'n', 'no']:
                print("\nRozpoczynanie treningu...")
                self.mlp.train(X_train, y_train, epochs=test_epochs,shuffle=test_shuffle,
                               error_threshold=test_error_threshold, use_momentum=test_use_momentum,
                               momentum=test_momentum,max_no_improvement_epochs=test_max_no_improvement_epochs,
                               log_interval=test_log_interval, learning_rate=test_learning_rate)
            print("\nTrening zakończony!")

            test_iris_move_forward = input(f"Czy przetestować ? (tak/nie): ").strip().lower()
            if test_iris_move_forward in ['tak', 't', 'yes', 'y']:
                y_true = np.argmax(y_test, axis=1)
                self.test_iris_network(X_test, y_true)
            elif test_iris_move_forward in ['nie', 'n', 'no']:
                return

            # self.mlp.save_log_of_learning(self.mlp.log_interval, "network_log.json")

        except Exception as e:
            print(f"Wystąpił błąd: {str(e)}")

    def test_iris_network(self, iris_x_test = None , iris_y_true = None):

    # outputs = mlp.predict(X_test)
    # outputs = mlp_restored.predict_with_logging(X_test, y_true)

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
