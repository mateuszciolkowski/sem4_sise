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

    def create_network_interface(self):
        print("\n=== Tworzenie nowej sieci ===")
        while True:
            try:
                # Parametry sieci do wprowadzenia
                num_inputs = int(input("Podaj liczbę wejść: "))
                num_hidden = int(input("Podaj liczbę neuronów w warstwach ukrytych: "))
                num_outputs = int(input("Podaj liczbę wyjść: "))
                bias = float(input("Podaj wartość biasu: "))

                use_momentum = input("Czy używać momentum? (tak/nie): ").lower()
                use_momentum = use_momentum == "tak"

                if use_momentum:
                    momentum = float(input("Podaj wartość momentum (0-1): "))
                else:
                    momentum = 0.0

                learning_rate = float(input("Podaj współczynnik uczenia (0-1): "))

                # Tworzymy sieć
                self.mlp = MLP(layer_sizes=[num_inputs, num_hidden, num_outputs],
                               activation_function=sigmoid,
                               activation_derivative=sigmoid_derivative,
                               learning_rate=learning_rate,
                               use_momentum=use_momentum,
                               momentum=momentum,
                               bias=bias)

                break  # Przechodzimy do następnego menu

            except Exception as e:
                print(f"Błąd: {str(e)}")

        self.network_configuration_interface()

    def load_network_interface(self):
        print("\n=== Wczytywanie istniejącej sieci ===")
        try:
            filename = input("Podaj nazwę pliku z wytrenowaną siecią: ")
            self.mlp = MLP.load_from_file(filename, sigmoid, sigmoid_derivative)
            print("Pomyślnie załadowano sieć")
            self.network_configuration_interface()
        except FileNotFoundError:
            print(f"Błąd: Nie znaleziono pliku {filename}")
        except Exception as e:
            print(f"Wystąpił błąd podczas wczytywania: {str(e)}")

    def network_configuration_interface(self):
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

    def configure_network(self):
        """Konfiguracja sieci (liczba neuronów, epoki, bias itp.)"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        # Wyświetlanie bieżącej konfiguracji sieci
        print("\n=== Aktualna konfiguracja ===")
        print(f"1. Liczba wejść: {self.mlp.layer_sizes[0]}")
        print(f"2. Liczba neuronów w warstwie ukrytej: {self.mlp.layer_sizes[1]}")
        print(f"3. Liczba wyjść: {self.mlp.layer_sizes[2]}")
        print(f"4. Bias: {self.mlp.bias}")
        print(f"5. Używać momentum: {self.mlp.use_momentum}")
        print(f"6. Wartość momentum: {self.mlp.momentum}")
        print(f"7. Współczynnik uczenia: {self.mlp.learning_rate}")
        print("===================")

        try:
            choice = input("Wybierz numer parametru do zmiany (1-10): ")
            if choice == '1':
                self.mlp.layer_sizes[0] = int(input("Podaj nową liczbę wejść: "))
            elif choice == '2':
                self.mlp.layer_sizes[1] = int(input("Podaj nową liczbę neuronów w warstwie ukrytej: "))
            elif choice == '3':
                self.mlp.layer_sizes[2] = int(input("Podaj nową liczbę wyjść: "))
            elif choice == '4':
                self.mlp.bias = float(input("Podaj nową wartość biasu: "))
            elif choice == '5':
                use_momentum = input("Czy używać momentum? (tak/nie): ").lower()
                self.mlp.use_momentum = use_momentum == "tak"
            elif choice == '6':
                self.mlp.momentum = float(input("Podaj nową wartość momentum (0-1): "))
            elif choice == '7':
                self.mlp.learning_rate = float(input("Podaj nowy współczynnik uczenia: "))
            elif choice == '8':
                self.mlp.epochs = int(input("Podaj nową liczbę epok: "))
            elif choice == '9':
                self.mlp.error_threshold = float(input("Podaj nowy próg błędu: "))
            elif choice == '10':
                self.mlp.log_interval = int(input("Podaj nowy interwał logowania: "))
            else:
                print("Nieprawidłowa opcja. Wybierz 1-10.")
        except Exception as e:
            print(f"Wystąpił błąd: {str(e)}")

    def train_iris_network(self):
        """Trenowanie sieci na zbiorze danych Irysów"""
        if self.mlp is None:
            print("Brak załadowanej sieci. Wróć do menu.")
            return

        # Wczytaj dane Iris
        dataset_path = "data/iris/iris.data"
        X, y = load_iris(dataset_path, standarded=True)

        try:
            # Podział danych na treningowe i testowe
            test_epochs = int(input("Podaj liczbe epok: "))
            test_error_threshold = float(input("Podaj błąd: "))
            test_log_interval = float(input("Podaj interwał błedu: "))
            test_size = float(input("Podaj procent danych testowych (0.1-0.9): "))
            if 0.1 <= test_size <= 0.9:
                X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)
            else:
                raise ValueError("Wartość musi być z przedziału [0.1, 0.9]")

            # Trenuj sieć
            print("\nRozpoczynanie treningu...")
            self.mlp.train(X_train, y_train, epochs=test_epochs,
                           error_threshold=test_error_threshold,
                           log_interval=test_log_interval)

            print("\nTrening zakończony!")
            self.mlp.save_log_of_learning(self.mlp.log_interval, "network_log.json")
            plot_error_curve(self.mlp.epoch_errors)

        except Exception as e:
            print(f"Wystąpił błąd: {str(e)}")

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
