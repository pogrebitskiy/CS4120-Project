"""
This class implements a wrapper for scikit-learn classifiers. It inherits from the BaseClassifier class

By: David Pogrebitskiy and Jacob Ostapenko
Date: 03/31/2023
"""
from models.BaseClassifier import BaseClassifier
import utils
import numpy as np
from typing import Any, Dict
from sklearn.metrics import confusion_matrix
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import RandomizedSearchCV


class SklearnClassifier(BaseClassifier):
    """
    This class implements a wrapper for scikit-learn classifiers. It inherits from the BaseClassifier class.

    Attributes:
        model: The scikit-learn classifier model.
    """

    def __init__(self, model) -> None:
        """
        Initialize the SklearnClassifier.

        Args:
            model (ClassifierMixin): The scikit-learn classifier model.
        """
        super().__init__(model)
        self.best_hyperparams = None

    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> None:
        """
        Train the model.

        Args:
            X_train (ndarray): Training data.
            y_train (ndarray): Target labels.

        Returns:
            None
        """
        self.model.fit(X_train, y_train)

    def hyperparameter_tuning(self, X_train: np.ndarray, y_train: np.ndarray, param_options: dict,
                              n_iter: int = 10, cv: int = 5, random_state: int = 42,
                              verbose: int = 2, n_jobs: int = -1) -> None:
        """
        Perform hyperparameter tuning using RandomizedSearchCV.

        Args:
            X_train (ndarray): Training data.
            y_train (ndarray): Target labels.
            param_options (dict): Dictionary with parameters names (str) as keys and distributions
                                        or lists of parameters to try.
            n_iter (int, optional): Number of parameter settings that are sampled. Defaults to 100.
            cv (int, optional): Determines the cross-validation splitting strategy. Defaults to 5.
            random_state (int, RandomState instance or None, optional): Pseudo random number generator state
            verbose (int, optional): Controls the verbosity. Defaults to 2.
            n_jobs (int, optional): Number of jobs to run in parallel. Defaults to -1.


        Returns:
            RandomizedSearchCV: Fitted RandomizedSearchCV instance.
        """
        random_search = RandomizedSearchCV(self.model, param_options, n_iter=n_iter, cv=cv,
                                           random_state=random_state, verbose=verbose, n_jobs=n_jobs)
        random_search.fit(X_train, y_train)

        # Set the best parameters to the model
        self.model = random_search.best_estimator_
        self.best_hyperparams = random_search.best_params_

    def get_best_hyperparams(self) -> Dict[str, Any]:
        """
        Get the best hyperparameters found during hyperparameter tuning.

        Returns:
            dict: A dictionary of the best hyperparameters.
        """
        return self.best_hyperparams

    def predict(self, X_test: np.ndarray) -> np.ndarray:
        """
        Make predictions.

        Args:
            X_test (ndarray): Test data.

        Returns:
            ndarray: Predicted labels.
        """
        return self.model.predict(X_test)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict[str, Any]:
        """
        Evaluate the model using precision, recall, and f1, accuracy

        Args:
            X_test (ndarray): Test data.
            y_test (ndarray): True labels.

        Returns:
            dict: A dictionary of metrics.
        """
        y_pred = self.predict(X_test)
        metrics = utils.get_prfa(y_test, y_pred)
        return metrics

    def get_confusion_matrix(self, X_test: np.ndarray, y_test: np.ndarray, title: str) -> None:
        """
        Get the confusion matrix.

        Args:
            X_test (ndarray): Test data.
            y_test (ndarray): True labels.
            title (str): Title for the confusion matrix.

        Returns:
            ndarray: The confusion matrix.
        """
        y_pred = self.predict(X_test)
        mat = confusion_matrix(y_test, y_pred)

        # Visualize the confusion matrix
        fig, ax = plt.subplots(figsize=(10, 10))
        sns.heatmap(mat, annot=True, fmt='d', cmap='Blues', ax=ax)
        ax.set_xlabel('Predicted labels')
        ax.set_ylabel('True labels')
        ax.set_title(title)
        plt.show()