from sklearn.model_selection import train_test_split

from mlp import MLP
from data import *
from utils import *


class Interface:

    def __init__(self):
        self.mlp = MLP(layer_sizes=[4, 6, 3],  # Default layer sizes
                       activation_function=sigmoid,
                       activation_derivative=sigmoid_derivative,
                       learning_rate=0.1,
                       use_momentum=False,
                       momentum=0.0)

    def menu(self):
        print("1.Klasyfikacja irysów\n"
              "2.Autoasocjacja\n"
              "3.Konfiguruj MLP\n"  # Add this line to configure MLP
              "4.Wyjscie")
        action = input("Podaj liczbę: ")
        while True:
            if action == "1":
                self.iris_interface()
            elif action == "2":
                self.autoasocjacja_interface()
            elif action == "3":
                self.konfiguruj_mlp()  # Call configure MLP when selected
            elif action == "4":
                break
            else:
                print("Niepoprawna opcja. Wybierz 1, 2, 3 lub 4.")
                action = input("Podaj liczbę: ")

    def konfiguruj_mlp(self):
        """Configures MLP by allowing user to change parameters interactively."""
        while True:
            print("\nAktualna konfiguracja MLP:")
            print(f"1. Ilość neuronów ukrytych: {self.mlp.layers[1].neurons}")
            print(f"2. Funkcja aktywacji: {self.mlp.activation_function.__name__}")
            print(f"3. Współczynnik uczenia: {self.mlp.learning_rate}")
            print(f"4. Używać momentu: {self.mlp.use_momentum}")
            print(f"5. Wartość momentu: {self.mlp.momentum}")
            print(f"6. Liczba epok: {self.mlp.epochs if hasattr(self.mlp, 'epochs') else 'N/A'}")
            print(f"7. Próg błędu: {self.mlp.error_threshold if hasattr(self.mlp, 'error_threshold') else 'N/A'}")
            print(f"8. Interwał logowania: {self.mlp.log_interval if hasattr(self.mlp, 'log_interval') else 'N/A'}")
            print(f"9. Wyjdź do menu")

            choice = input("\nWybierz opcję, aby zmienić (1-8) lub 9, aby wyjść: ")

            if choice == '1':
                # Change layer sizes
                new_layer_sizes = input("Podaj nowe warstwy (np. [4, 6, 3]): ")
                self.mlp.layer_sizes = eval(new_layer_sizes)
                print(f"Nowe warstwy: {self.mlp.layer_sizes}")
            elif choice == '2':
                # Change activation function
                activation_choice = input("Wybierz funkcję aktywacji (sigmoid/tanh): ")
                if activation_choice == 'sigmoid':
                    self.mlp.activation_function = sigmoid
                    self.mlp.activation_derivative = sigmoid_derivative
                elif activation_choice == 'tanh':
                    self.mlp.activation_function = tanh
                    self.mlp.activation_derivative = tanh_derivative
                else:
                    print("Niepoprawny wybór.")
                    continue
                print(f"Nowa funkcja aktywacji: {self.mlp.activation_function.__name__}")
            elif choice == '3':
                # Change learning rate
                new_learning_rate = float(input("Podaj nowy współczynnik uczenia (np. 0.1): "))
                self.mlp.learning_rate = new_learning_rate
                print(f"Nowy współczynnik uczenia: {self.mlp.learning_rate}")
            elif choice == '4':
                # Change momentum usage
                use_momentum = input("Czy używać momentu? (True/False): ").lower() == 'true'
                self.mlp.use_momentum = use_momentum
                print(f"Czy używać momentu: {self.mlp.use_momentum}")
            elif choice == '5':
                # Change momentum value
                new_momentum = float(input("Podaj nową wartość momentu (np. 0.9): "))
                self.mlp.momentum = new_momentum
                print(f"Nowa wartość momentu: {self.mlp.momentum}")
            elif choice == '6':
                # Change number of epochs
                new_epochs = int(input("Podaj nową liczbę epok (np. 1000): "))
                self.mlp.epochs = new_epochs
                print(f"Nowa liczba epok: {self.mlp.epochs}")
            elif choice == '7':
                # Change error threshold
                new_threshold = float(input("Podaj nowy próg błędu (np. 0.00001): "))
                self.mlp.error_threshold = new_threshold
                print(f"Nowy próg błędu: {self.mlp.error_threshold}")
            elif choice == '8':
                # Change log interval
                new_log_interval = int(input("Podaj nowy interwał logowania (np. 10): "))
                self.mlp.log_interval = new_log_interval
                print(f"Nowy interwał logowania: {self.mlp.log_interval}")
            elif choice == '9':
                print("Wychodzę do menu.")
                break
            else:
                print("Niepoprawna opcja. Wybierz 1-9.")

    def iris_interface(self):
        print("Rozpoczynasz konfigurację sieci dla klasyfikacji irysów.\n")

        # Configure the MLP interactively
        self.konfiguruj_mlp()  # Allow the user to configure MLP before proceeding

        # Once configuration is done, proceed with further actions
        action = input("Wybierz akcję:\n1. Wytrenuj sieć\n2. Dokonaj predykcji\nPodaj liczbę: ")

        if action == '1':
            dataset_path = "data/iris/iris.data"
            X, y = load_iris(dataset_path, standarded=True)
            test_size = float(input("Wybierz zbiór danych testowych (np. 0.5 dla 50%): "))
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, stratify=y)

            epochs = self.mlp.epochs
            error_threshold = self.mlp.error_threshold
            log_interval = self.mlp.log_interval

            # Train the neural network
            self.mlp.train(X_train, y_train, epochs=epochs, error_threshold=error_threshold, log_interval=log_interval)

            # Save learning log and plot error curve
            self.mlp.save_log_of_learning(log_interval, "network_log.json")
            plot_error_curve(self.mlp.epoch_errors)

            # Ask if the user wants to save the network
            save_network = input("Czy chcesz zapisać wytrenowaną sieć? (Tak/Nie): ").lower()
            if save_network == 'tak':
                filename = input("Podaj nazwę pliku do zapisania sieci: ")
                self.mlp.save_to_file(filename)
                print(f"Sieć została zapisana w pliku {filename}.")
            else:
                print("Sieć nie została zapisana.")
            print("\nSieć została wytrenowana.")

        elif action == '2':  # Make predictions
            filename = input("Podaj nazwę pliku, z którego chcesz załadować wytrenowaną sieć: ")
            try:
                mlp_restored = MLP.load_from_file(filename, sigmoid, sigmoid_derivative)
                print("\nZaładowano wytrenowaną sieć z pliku.")

                # Predict with the trained model
                predictions = mlp_restored.predict(X_test)

                print("\nDokonano predykcji na zbiorze testowym:")
                print(predictions)
            except FileNotFoundError:
                print(f"Plik {filename} nie istnieje. Upewnij się, że podałeś poprawną nazwę.")

    def autoasocjacja_interface(self):
        return
