from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import numpy as np
import json

from mlp import MLP
from data import *
from utils import *


class Interface:

    def __init__(self):
        self.mlp = MLP(layer_sizes=[4, 6, 3],
                       activation_function=sigmoid,
                       activation_derivative=sigmoid_derivative,
                       learning_rate=0.1,
                       use_momentum=False,
                       momentum=0.0)
        # Domyślne wartości
        self.mlp.epochs = 1000
        self.mlp.error_threshold = 0.00001
        self.mlp.log_interval = 10

    def menu(self):
        while True:
            print("\n=== Menu Główne ===")
            print("1. Klasyfikacja irysów")
            print("2. Autoasocjacja")
            print("3. Wyjście")
            print("==================")
            
            try:
                action = input("Wybierz opcję (1-3): ")
                if action == "1":
                    self.iris_interface()
                elif action == "2":
                    self.autoasocjacja_interface()
                elif action == "3":
                    print("Do widzenia!")
                    break
                else:
                    print("\nBłąd: Wybierz opcję od 1 do 3.")
            except Exception as e:
                print(f"\nWystąpił błąd: {str(e)}")

    def konfiguruj_mlp(self):
        while True:
            try:
                print("\n=== Aktualna konfiguracja MLP ===")
                print(f"1. Ilość neuronów w warstwach: {self.mlp.layer_sizes}")
                print(f"2. Funkcja aktywacji: {self.mlp.activation_function.__name__}")
                print(f"3. Współczynnik uczenia: {self.mlp.learning_rate}")
                print(f"4. Używać momentu: {self.mlp.use_momentum}")
                print(f"5. Wartość momentu: {self.mlp.momentum}")
                print(f"6. Liczba epok: {self.mlp.epochs}")
                print(f"7. Próg błędu: {self.mlp.error_threshold}")
                print(f"8. Interwał logowania: {self.mlp.log_interval}")
                print(f"9. Wartość biasu: {self.mlp.bias}")
                print(f"10. Powrót do menu")
                print("===============================")
    
                choice = input("\nWybierz opcję (1-10): ")
    
                if choice == '1':
                    try:
                        new_layer_sizes = eval(input("Podaj nowe warstwy [liczba_wejść, neurony_ukryte, liczba_wyjść]: "))
                        if not isinstance(new_layer_sizes, list) or len(new_layer_sizes) != 3:
                            raise ValueError("Nieprawidłowy format warstw. Przykład: [4, 6, 3]")
                        self.mlp.layer_sizes = new_layer_sizes
                        print(f"Zaktualizowano warstwy: {self.mlp.layer_sizes}")
                    except Exception as e:
                        print(f"Błąd: {str(e)}")
    
                elif choice == '2':
                    print("\nDostępne funkcje aktywacji:")
                    print("1. Sigmoid (jedyna dostępna funkcja aktywacji)")
                    print("\nAutomatycznie ustawiono funkcję sigmoidalną")
                    self.mlp.activation_function = sigmoid
                    self.mlp.activation_derivative = sigmoid_derivative
                    print(f"Aktualna funkcja aktywacji: {self.mlp.activation_function.__name__}")
    
                elif choice == '3':
                    try:
                        new_rate = float(input("Podaj nowy współczynnik uczenia (0-1): "))
                        if 0 < new_rate <= 1:
                            self.mlp.learning_rate = new_rate
                            print(f"Zaktualizowano współczynnik uczenia: {new_rate}")
                        else:
                            print("Wartość musi być z przedziału (0,1]")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę zmiennoprzecinkową")
    
                elif choice == '4':
                    use_momentum = input("Czy używać momentu? (tak/nie): ").lower()
                    self.mlp.use_momentum = use_momentum == 'tak'
                    print(f"Zaktualizowano używanie momentu: {self.mlp.use_momentum}")
    
                elif choice == '5':
                    try:
                        new_momentum = float(input("Podaj nową wartość momentu (0-1): "))
                        if 0 <= new_momentum <= 1:
                            self.mlp.momentum = new_momentum
                            print(f"Zaktualizowano wartość momentu: {new_momentum}")
                        else:
                            print("Wartość musi być z przedziału [0,1]")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę zmiennoprzecinkową")
    
                elif choice == '6':
                    try:
                        new_epochs = int(input("Podaj nową liczbę epok (>0): "))
                        if new_epochs > 0:
                            self.mlp.epochs = new_epochs
                            print(f"Zaktualizowano liczbę epok: {new_epochs}")
                        else:
                            print("Liczba epok musi być większa od 0")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę całkowitą")
    
                elif choice == '7':
                    try:
                        new_threshold = float(input("Podaj nowy próg błędu (>0): "))
                        if new_threshold > 0:
                            self.mlp.error_threshold = new_threshold
                            print(f"Zaktualizowano próg błędu: {new_threshold}")
                        else:
                            print("Próg błędu musi być większy od 0")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę zmiennoprzecinkową")
    
                elif choice == '8':
                    try:
                        new_interval = int(input("Podaj nowy interwał logowania (>0): "))
                        if new_interval > 0:
                            self.mlp.log_interval = new_interval
                            print(f"Zaktualizowano interwał logowania: {new_interval}")
                        else:
                            print("Interwał musi być większy od 0")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę całkowitą")
    
                elif choice == '9':
                    try:
                        new_bias = float(input("Podaj nową wartość biasu: "))
                        self.mlp.bias = new_bias
                        print(f"Zaktualizowano wartość biasu: {new_bias}")
                    except ValueError:
                        print("Błąd: Wprowadź poprawną liczbę zmiennoprzecinkową")
    
                elif choice == '10':
                    print("Powrót do menu głównego")
                    return None  # Sygnalizuje normalne zakończenie konfiguracji
    
                else:
                    print("Nieprawidłowa opcja. Wybierz 1-10.")
    
            except Exception as e:
                print(f"Wystąpił nieoczekiwany błąd: {str(e)}")
                return True  # Sygnalizuje przerwanie konfiguracji z powodu błędu

    def iris_interface(self):
        print("\n=== Klasyfikacja Irysów ===")
        
        # Wczytaj dane
        dataset_path = "data/iris/iris.data"
        X, y = load_iris(dataset_path, standarded=True)
        
        while True:
            print("\n1. Stwórz i wytrenuj nową sieć")
            print("2. Wczytaj istniejącą sieć")
            print("3. Powrót do menu")
            print("==================")
            
            try:
                action = input("Wybierz akcję (1-3): ")
    
                if action == '1':
                    # Konfiguracja nowej sieci
                    print("\nKonfiguracja nowej sieci:")
                    self.konfiguruj_mlp()
                    
                    try:
                        while True:
                            try:
                                test_size = float(input("Podaj procent danych testowych (0.1-0.9): "))
                                if 0.1 <= test_size <= 0.9:
                                    break
                                print("Wartość musi być z przedziału [0.1, 0.9]")
                            except ValueError:
                                print("Błąd: Wprowadź poprawną liczbę zmiennoprzecinkową")
                        
                        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)
                        
                        # Zapisz dane podziału do pliku
                        split_data = {
                            'X_train': X_train.tolist(),
                            'X_test': X_test.tolist(),
                            'y_train': y_train.tolist(),
                            'y_test': y_test.tolist()
                        }
                        
                        with open('data/iris/split_data.json', 'w') as f:
                            json.dump(split_data, f)
                        
                        print("\nZapisano podział danych do pliku 'data/iris/split_data.json'")
                        
                        print("\nRozpoczęto trenowanie sieci...")
                        self.mlp.train(X_train, y_train, epochs=self.mlp.epochs, 
                                     error_threshold=self.mlp.error_threshold, 
                                     log_interval=self.mlp.log_interval)
                        
                        self.mlp.save_log_of_learning(self.mlp.log_interval, "network_log.json")
                        plot_error_curve(self.mlp.epoch_errors)
                        
                        # Ocena na zbiorze testowym
                        y_true = np.argmax(y_test, axis=1)
                        predictions = self.mlp.predict_with_logging(X_test, y_true)
                        y_pred = np.argmax(predictions, axis=1)
                        
                        print("\nWyniki na zbiorze testowym:")
                        print("\nMacierz pomyłek:")
                        print(confusion_matrix(y_true, y_pred))
                        print("\nRaport klasyfikacji:")
                        print(classification_report(y_true, y_pred, 
                              target_names=["setosa", "versicolor", "virginica"]))
                        
                        save = input("\nCzy chcesz zapisać wytrenowaną sieć? (tak/nie): ").lower()
                        if save == 'tak':
                            filename = input("Podaj nazwę pliku: ")
                            self.mlp.save_to_file(filename)
                            print(f"Sieć została zapisana w pliku: {filename}")
                        
                        print("\nTrenowanie zakończone!")
                        
                    except Exception as e:
                        print(f"Wystąpił błąd podczas trenowania: {str(e)}")

                elif action == '2':
                    try:
                        filename = input("Podaj nazwę pliku z wytrenowaną siecią: ")
                        mlp_restored = MLP.load_from_file(filename, sigmoid, sigmoid_derivative)
                        print("Załadowano sieć pomyślnie")
                        
                        # Wczytaj zapisany podział danych
                        try:
                            with open('data/iris/split_data.json', 'r') as f:
                                split_data = json.load(f)
                                X_test = np.array(split_data['X_test'])
                                y_test = np.array(split_data['y_test'])
                                print("Załadowano zapisany podział danych testowych")
                        except FileNotFoundError:
                            print("Nie znaleziono zapisanego podziału danych, używam całego zbioru")
                            X_test = X
                            y_test = y
                        
                        # Przygotuj dane do predykcji
                        y_true = np.argmax(y_test, axis=1)
                        outputs = mlp_restored.predict_with_logging(X_test, y_true)
                        y_pred = np.argmax(outputs, axis=1)
                        
                        print("\nWyniki predykcji:")
                        print("\nMacierz pomyłek:")
                        print(confusion_matrix(y_true, y_pred))
                        print("\nRaport klasyfikacji:")
                        print(classification_report(y_true, y_pred, 
                              target_names=["setosa", "versicolor", "virginica"]))
                        
                    except FileNotFoundError:
                        print(f"Błąd: Nie znaleziono pliku {filename}")
                    except Exception as e:
                        print(f"Wystąpił błąd podczas predykcji: {str(e)}")

                elif action == '3':
                    break

                else:
                    print("Nieprawidłowa opcja. Wybierz 1-3.")

            except Exception as e:
                print(f"Wystąpił nieoczekiwany błąd: {str(e)}")

    def autoasocjacja_interface(self):
        """Interfejs do trenowania i testowania autoasocjacji"""
        print("\n=== Autoasocjacja ===")
        
        # Zdefiniuj wzorce wejściowe dla autoasocjacji
        auto_association_data = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        
        while True:
            print("\n1. Stwórz i wytrenuj nową sieć")
            print("2. Wczytaj istniejącą sieć")
            print("3. Powrót do menu")
            print("==================")
            
            try:
                action = input("Wybierz akcję (1-3): ")
                if action == '1':
                    # Konfiguracja nowej sieci autoasocjacyjnej
                    print("\nKonfiguracja nowej sieci autoasocjacyjnej:")
                    
                    # Ustaw domyślne parametry dla autoasocjacji
                    self.mlp = MLP(layer_sizes=[4, 2, 4],
                                 activation_function=sigmoid,
                                 activation_derivative=sigmoid_derivative,
                                 learning_rate=0.2,
                                 use_momentum=True,
                                 momentum=0.6,
                                 bias=0.0)
                    
                    # Ustaw domyślne parametry treningu
                    self.mlp.epochs = 1000
                    self.mlp.error_threshold = 0.00001
                    self.mlp.log_interval = 10
                    
                    # Pozwól użytkownikowi zmodyfikować konfigurację
                    self.konfiguruj_mlp()
                    
                    try:
                        print("\nRozpoczęto trenowanie sieci...")
                        
                        # Trenuj autoasocjator
                        self.mlp.train(auto_association_data, auto_association_data,
                                     epochs=self.mlp.epochs,
                                     error_threshold=self.mlp.error_threshold,
                                     log_interval=self.mlp.log_interval)
                        
                        # Zapisz logi treningu i wyświetl krzywą błędu
                        self.mlp.save_log_of_learning(self.mlp.log_interval, "autoencoder_log.json")
                        plot_error_curve(self.mlp.epoch_errors)
                        
                        # Testuj autoasocjator na wzorcach wejściowych
                        print("\nWyuczone wzorce autoasocjacji:")
                        for i, pattern in enumerate(auto_association_data):
                            output = self.mlp.predict_with_logging([pattern])
                            print(f"\nWzorzec {i+1}:")
                            print(f"Wejście:  {pattern}")
                            print(f"Wyjście:  [{', '.join([f'{x:.6f}' for x in output[0]])}]")
                            print(f"Błąd:     {np.mean((pattern - output[0]) ** 2):.6f}")
                        
                        # Opcja zapisu wytrenowanej sieci
                        save = input("\nCzy chcesz zapisać wytrenowaną sieć? (tak/nie): ").lower()
                        if save == 'tak':
                            filename = input("Podaj nazwę pliku: ")
                            self.mlp.save_to_file(filename)
                            print(f"Sieć została zapisana w pliku: {filename}")
                        
                        print("\nTrenowanie zakończone!")
                        
                    except Exception as e:
                        print(f"Wystąpił błąd podczas trenowania: {str(e)}")

                elif action == '2':
                    try:
                        filename = input("Podaj nazwę pliku z wytrenowaną siecią: ")
                        mlp_restored = MLP.load_from_file(filename, sigmoid, sigmoid_derivative)
                        print("Pomyślnie załadowano sieć")
                        
                        # Testuj załadowany autoasocjator
                        print("\nWyuczone wzorce autoasocjacji:")
                        for i, pattern in enumerate(auto_association_data):
                            output = self.mlp.predict_with_logging([pattern])
                            print(f"\nWzorzec {i+1}:")
                            print(f"Wejście:  {pattern}")
                            print(f"Wyjście:  [{', '.join([f'{x:.6f}' for x in output[0]])}]")
                            print(f"Błąd:     {np.mean((pattern - output[0]) ** 2):.6f}")
                        
                        
                    except FileNotFoundError:
                        print(f"Błąd: Nie znaleziono pliku {filename}")
                    except Exception as e:
                        print(f"Wystąpił błąd podczas predykcji: {str(e)}")

                elif action == '3':
                    break

                else:
                    print("Nieprawidłowa opcja. Wybierz 1-3.")

            except Exception as e:
                print(f"Wystąpił nieoczekiwany błąd: {str(e)}")
       