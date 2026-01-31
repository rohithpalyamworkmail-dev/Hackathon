import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
from scipy.stats import pointbiserialr, chi2_contingency
from sklearn.feature_selection import *
import matplotlib.pyplot as plt
from feature_engine.selection import *

class FeatureSelection:
    def __init__(self, dataset):
        self.dataset = dataset

    def pearson(self):
        st.write("### Pearson Correlation Matrix")
        corr_matrix = self.dataset.corr(method='pearson', numeric_only=True)
        st.dataframe(corr_matrix)
        st.write("Heatmap:")
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    def spearman(self):
        st.write("### Spearman Correlation Matrix")
        corr_matrix = self.dataset.corr(method='spearman', numeric_only=True)
        st.dataframe(corr_matrix)
        st.write("Heatmap:")
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    def kendall(self):
        st.write("### Kendall Correlation Matrix")
        corr_matrix = self.dataset.corr(method='kendall', numeric_only=True)
        st.dataframe(corr_matrix)
        st.write("Heatmap:")
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    def point(self):
        st.write("### Point-Biserial Correlation")
        binary_columns = [col for col in self.dataset.columns if len(self.dataset[col].unique()) == 2]
        continuous_columns = [col for col in self.dataset.columns if col not in binary_columns]

        if not binary_columns:
            st.warning("No binary columns found for Point-Biserial Correlation.")
            return

        results = {}
        for bin_col in binary_columns:
            for cont_col in continuous_columns:
                try:
                    corr, _ = pointbiserialr(self.dataset[bin_col], self.dataset[cont_col])
                    results[(bin_col, cont_col)] = corr
                except Exception as e:
                    st.error(f"Error processing {bin_col} and {cont_col}: {e}")

        st.write("Point-Biserial Correlation Results:")
        result_df = pd.DataFrame.from_dict(results, orient='index', columns=['Correlation'])
        st.dataframe(result_df)
        fig, ax = plt.subplots()
        sns.heatmap(result_df, annot=True, cmap='coolwarm', ax=ax, cbar=False)
        st.pyplot(fig)

    def cramers(self):
        st.write("### Cramér's V (Association Between Categorical Variables)")
        categorical_columns = self.dataset.select_dtypes(include=['object', 'category']).columns

        if len(categorical_columns) < 2:
            st.warning("Not enough categorical columns for Cramér's V calculation.")
            return

        results = {}
        for col1 in categorical_columns:
            for col2 in categorical_columns:
                if col1 != col2:
                    contingency_table = pd.crosstab(self.dataset[col1], self.dataset[col2])
                    chi2, _, _, _ = chi2_contingency(contingency_table)
                    n = contingency_table.sum().sum()
                    r, k = contingency_table.shape
                    cramers_v = np.sqrt(chi2 / (n * (min(r, k) - 1)))
                    results[(col1, col2)] = cramers_v

        st.write("Cramér's V Results:")
        result_df = pd.DataFrame.from_dict(results, orient='index', columns=['Cramér\'s V'])
        st.dataframe(result_df)
        fig, ax = plt.subplots()
        sns.heatmap(result_df, annot=True, cmap='coolwarm', ax=ax, cbar=False)
        st.pyplot(fig)

    def variance_threshold(self):
        st.write("### Variance Threshold Method")

        threshold=st.number_input("Threshold value")
        if threshold:
            st.write(f"Variance Threshold: {threshold}")
            
            numeric_data = self.dataset.select_dtypes(include=['number'])
            if numeric_data.empty:
                st.warning("No numeric columns found for Variance Threshold.")
                return
            
            selector = VarianceThreshold(threshold=threshold)
            try:
                selector.fit(numeric_data)
                mask = selector.get_support()
                selected_features = numeric_data.columns[mask]
                st.write("Selected Features:")
                st.write(list(selected_features))
                st.write("Removed Features:")
                st.write(list(numeric_data.columns[~mask]))
            except Exception as e:
                st.error(f"Error during variance threshold selection: {e}")




class StatisticalFunctions:
    def __init__(self, dataset):
        self.dataset = dataset
        self.score_functions = {
            'f_classif': f_classif,
            'f_regression': f_regression,
            'mutual_info_classif': mutual_info_classif,
            'mutual_info_regression': mutual_info_regression,
            'r_regression': r_regression,
            'chi2': chi2
        }

    def generic_univariate_select(self):
        score_func_name = st.selectbox("Select a score function", self.score_functions.keys())
        mode = st.selectbox("Select the mode", ['percentile', 'k_best', 'fpr', 'fdr', 'fwe'])
        param = st.text_input("Parameter for the mode (percentile, k, alpha)", "Enter Here")
        param = float(param) if param != "Enter Here" else 5e-2

        features = st.multiselect("Select feature columns", self.dataset.columns)
        target = st.selectbox("Select target column (optional)", [None] + list(self.dataset.columns))

        if st.checkbox("Confirm to apply Generic Univariate Select"):
            if not features:
                st.error("Please select at least one feature column.")
                return

            x = self.dataset[features]
            y = self.dataset[target] if target else None
            score_func = self.score_functions[score_func_name]

            transformer = GenericUnivariateSelect(score_func=score_func, mode=mode, param=param)
            X_new = transformer.fit_transform(x, y)

            st.header("Transformed Data Frame")
            transformed_df = X_new
            st.dataframe(transformed_df)

            # Calling common_attributes
            self.common_attributes(transformer)
        else:
            st.warning("Please confirm to apply Generic Univariate Select.")

    def common_attributes(self, transformer):
        st.subheader("Attributes for the Current Result")
        if hasattr(transformer, 'scores_'):
            st.info("Scores")
            st.write(transformer.scores_)
        if hasattr(transformer, 'pvalues_'):
            st.info("P-Values")
            st.write(transformer.pvalues_)
        st.info("Number of Features In")
        st.write(transformer.n_features_in_)
        st.info("Feature Names In")
        st.write(transformer.feature_names_in_)

    def select_fdr(self):
        self._apply_selection_method("Select FDR", SelectFdr)

    def select_fpr(self):
        self._apply_selection_method("Select FPR", SelectFpr)

    def select_fwe(self):
        self._apply_selection_method("Select FWE", SelectFwe)

    def select_k_best(self):
        st.header("Select K Best")
        self._apply_selection_method_with_param("k", SelectKBest, default_param=10)

    def select_percentile(self):
        st.header("Select Percentile")
        self._apply_selection_method_with_param("percentile", SelectPercentile, default_param=10)

    def _apply_selection_method(self, header, selector_class):
        st.header(header)
        score_func_name = st.selectbox("Select a score function", self.score_functions.keys())
        alpha = st.slider(f"Select the alpha value for {header}", min_value=0.01, max_value=0.5, value=0.05, step=0.01)

        features = st.multiselect("Select feature columns", self.dataset.columns)
        target = st.selectbox("Select target column (optional)", [None] + list(self.dataset.columns))

        if st.checkbox(f"Confirm to apply {header}"):
            if not features:
                st.error("Please select at least one feature column.")
                return

            x = self.dataset[features]
            y = self.dataset[target] if target else None
            score_func = self.score_functions[score_func_name]

            transformer = selector_class(score_func=score_func, alpha=alpha)
            X_new = transformer.fit_transform(x, y)

            st.header("Transformed Data Frame")
            transformed_df = pd.DataFrame(X_new, columns=[f"Feature_{i}" for i in range(X_new.shape[1])])
            st.dataframe(transformed_df)

            # Calling common_attributes
            self.common_attributes(transformer)

    def _apply_selection_method_with_param(self, param_name, selector_class, default_param):
        param = st.number_input(f"Select the {param_name} value", min_value=1, value=default_param, step=1)

        features = st.multiselect("Select feature columns", self.dataset.columns)
        target = st.selectbox("Select target column (optional)", [None] + list(self.dataset.columns))

        if st.checkbox(f"Confirm to apply {selector_class.__name__}"):
            if not features:
                st.error("Please select at least one feature column.")
                return

            x = self.dataset[features]
            y = self.dataset[target] if target else None
            score_func = self.score_functions['f_classif']  # Default score function for simplicity

            transformer = selector_class(score_func=score_func, **{param_name: param})
            X_new = transformer.fit_transform(x, y)

            st.header("Transformed Data Frame")
            transformed_df = pd.DataFrame(X_new, columns=[f"Feature_{i}" for i in range(X_new.shape[1])])
            st.dataframe(transformed_df)

            # Calling common_attributes
            self.common_attributes(transformer)

class FinalDataSet:
    def __init__(self, dataset):
        self.dataset = dataset

    def drop_features(self):
        st.subheader("Drop Features")
        features_to_drop = st.multiselect(
            "Select features to drop:",
            options=self.dataset.columns,
            help="Choose one or more features to remove from the dataset.",
            key=1
        )
        confirm = st.checkbox("Apply DropFeatures?")
        if confirm and features_to_drop:
            dropper = DropFeatures(features_to_drop=features_to_drop)
            transformed_data = dropper.fit_transform(self.dataset)
            st.write("### Attributes:")
            st.json({
                "features_to_drop_": dropper.features_to_drop_,
                "feature_names_in_": dropper.feature_names_in_,
                "n_features_in_": dropper.n_features_in_,
            })
            return transformed_data
        return self.dataset

    def drop_constant_features(self):
        st.subheader("Drop Constant or Quasi-Constant Features")
        tol = st.slider(
            "Set tolerance for quasi-constant features:",
            min_value=0.0, max_value=1.0, value=1.0,
            help="Threshold for detecting quasi-constant features."
        )
        missing_values = st.selectbox(
            "How to handle missing values?",
            options=["raise", "ignore", "include"],
            index=0
        )
        confirm = st.checkbox("Apply DropConstantFeatures?")
        if confirm:
            dropper = DropConstantFeatures(tol=tol, missing_values=missing_values)
            transformed_data = dropper.fit_transform(self.dataset)
            st.write("### Attributes:")
            st.json({
                "features_to_drop_": dropper.features_to_drop_,
                "variables_": dropper.variables_,
                "feature_names_in_": dropper.feature_names_in_,
                "n_features_in_": dropper.n_features_in_,
            })
            return transformed_data
        return self.dataset

    def drop_duplicate_features(self):
        st.subheader("Drop Duplicate Features")
        missing_values = st.selectbox(
            "How to handle missing values ?",
            options=["raise", "ignore"],
            index=1
        )
        confirm = st.checkbox("Apply DropDuplicateFeatures?")
        if confirm:
            dropper = DropDuplicateFeatures(missing_values=missing_values)
            transformed_data = dropper.fit_transform(self.dataset)
            st.write("### Attributes:")
            st.json({
                "features_to_drop_": list(dropper.features_to_drop_),
                "duplicated_feature_sets_": dropper.duplicated_feature_sets_,
                "variables_": dropper.variables_,
                "feature_names_in_": dropper.feature_names_in_,
                "n_features_in_": dropper.n_features_in_,
            })
            return transformed_data
        return self.dataset

    def drop_correlated_features(self):
        st.subheader("Drop Correlated Features")
        threshold = st.slider(
            "Set correlation threshold :",
            min_value=0.0, max_value=1.0, value=0.8,
            help="Correlation above this threshold will result in feature removal."
        )
        method = st.selectbox(
            "Select correlation method :",
            options=["pearson", "spearman", "kendall"],
            index=0
        )
        missing_values = st.selectbox(
            "How to handle missing values",
            options=["raise", "ignore"],
            index=1
        )
        confirm = st.checkbox("Apply DropCorrelatedFeatures?")
        if confirm:
            dropper = DropCorrelatedFeatures(
                method=method,
                threshold=threshold,
                missing_values=missing_values
            )
            transformed_data = dropper.fit_transform(self.dataset)
            st.write("### Attributes:")
            st.json({
                "features_to_drop_": list(dropper.features_to_drop_),
                "correlated_feature_sets_": dropper.correlated_feature_sets_,
                "correlated_feature_dict_": dropper.correlated_feature_dict_,
                "variables_": dropper.variables_,
                "feature_names_in_": dropper.feature_names_in_,
                "n_features_in_": dropper.n_features_in_,
            })
            return transformed_data
        return self.dataset
    def smart_correlated_selection(self):
        st.subheader("Smart Correlated Feature Selection")
        method = st.selectbox(
            "Select correlation method:",
            options=["pearson", "spearman", "kendall"],
            index=0,
            help="Method for calculating correlation."
        )
        threshold = st.slider(
            "Set correlation threshold",
            min_value=0.0,
            max_value=1.0,
            value=0.8,
            help="Features with correlations above this threshold will be grouped."
        )
        selection_method = st.selectbox(
            "Feature selection method within correlated groups:",
            options=["missing_values", "cardinality", "variance", "model_performance"],
            index=0,
            help="Criteria to select the best feature from a correlated group."
        )
        missing_values = st.selectbox(
            "how to handle missing values?",
            options=["raise", "ignore"],
            index=1,
            help="Specify if missing values should be ignored or raise an error."
        )
        estimator = None
        if selection_method == "model_performance":
            st.warning(
                "You must provide an estimator for the 'model_performance' selection method."
            )
            estimator_name = st.text_input(
                "Enter the name of a Scikit-learn estimator (e.g., RandomForestClassifier):"
            )
            if estimator_name:
                try:
                    from sklearn.ensemble import RandomForestClassifier
                    estimator = eval(estimator_name + "()")
                except Exception as e:
                    st.error(f"Failed to initialize the estimator: {e}")
        
        confirm = st.checkbox("Apply SmartCorrelatedSelection?")
        if confirm:
            try:
                smart_selector = SmartCorrelatedSelection(
                    method=method,
                    threshold=threshold,
                    selection_method=selection_method,
                    missing_values=missing_values,
                    estimator=estimator,
                    scoring="roc_auc" if estimator else None,
                    cv=3
                )
                transformed_data = smart_selector.fit_transform(self.dataset)
                st.write("### Attributes:")
                st.json({
                    "correlated_feature_sets_": list(smart_selector.correlated_feature_sets_),
                    "correlated_feature_dict_": smart_selector.correlated_feature_dict_,
                    "features_to_drop_": list(smart_selector.features_to_drop_),
                    "variables_": smart_selector.variables_,
                    "feature_names_in_": smart_selector.feature_names_in_,
                    "n_features_in_": smart_selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred while applying SmartCorrelatedSelection: {e}")
        return self.dataset
    def select_by_single_feature_performance(self):
        st.subheader("Select Features by Single Feature Performance")
        
        estimator_name = st.text_input(
            "Enter the name of a Scikit-learn estimator(e.g., RandomForestClassifier):",
            help="Provide the name of the estimator to be used for performance evaluation."
        )
        scoring = st.text_input(
            "Enter the scoring metric (default='roc_auc'):",
            value="roc_auc",
            help="Scoring metric to evaluate model performance. See Scikit-learn documentation for valid metrics."
        )
        cv = st.slider(
            "Select number of cross-validation folds :",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        threshold = st.number_input(
            "Set performance threshold",
            min_value=0.0, max_value=1.0, value=0.5,
            help="Threshold above which features will be retained."
        )
        confirm = st.checkbox("Apply SelectBySingleFeaturePerformance?")

        if estimator_name and confirm:
            try:
                from sklearn.ensemble import RandomForestClassifier
                estimator = eval(estimator_name + "()")
                selector = SelectBySingleFeaturePerformance(
                    estimator=estimator,
                    scoring=scoring,
                    cv=cv,
                    threshold=threshold
                )
                transformed_data = selector.fit_transform(self.dataset)
                st.write("### Attributes:")
                st.json({
                    "features_to_drop_": list(selector.features_to_drop_),
                    "feature_performance_": selector.feature_performance_,
                    "feature_performance_std_": selector.feature_performance_std_,
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    def recursive_feature_elimination(self):
        st.subheader("Recursive Feature Elimination")

        estimator_name = st.text_input(
            "Enter the name of a Scikit-learn estimator (Example : RandomForestClassifier):",
            help="Provide the name of the estimator to be used for feature ranking."
        )
        scoring = st.text_input(
            "Enter the scoring metric(default='roc_auc'):",
            value="roc_auc",
            help="Scoring metric to evaluate model performance. See Scikit-learn documentation for valid metrics."
        )
        threshold = st.number_input(
            "Set performance drift threshold  :",
            min_value=0.0, max_value=1.0, value=0.01,
            help="Maximum allowed performance drop when removing a feature."
        )
        cv = st.slider(
            "Select number of cross-validation folds  :",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        confirm = st.checkbox("Apply Recursive Feature Elimination?")

        if estimator_name and confirm:
            try:
                from sklearn.ensemble import RandomForestClassifier
                estimator = eval(estimator_name + "()")
                selector = RecursiveFeatureElimination(
                    estimator=estimator,
                    scoring=scoring,
                    cv=cv,
                    threshold=threshold
                )
                transformed_data = selector.fit_transform(self.dataset)
                st.write("### Attributes:")
                st.json({
                    "initial_model_performance_": selector.initial_model_performance_,
                    "feature_importances_": selector.feature_importances_.to_dict(),
                    "feature_importances_std_": selector.feature_importances_std_.to_dict(),
                    "performance_drifts_": selector.performance_drifts_,
                    "performance_drifts_std_": selector.performance_drifts_std_,
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    
    def recursive_feature_addition(self):
        st.subheader("Recursive Feature Addition")

        estimator_name = st.text_input(
            "Enter the name of a Scikit-learn estimator (e.g. RandomForestClassifier):",
            help="Provide the name of the estimator to be used for feature ranking."
        )
        scoring = st.text_input(
            "Enter the scoring metric default='roc_auc':",
            value="roc_auc",
            help="Scoring metric to evaluate model performance. See Scikit-learn documentation for valid metrics."
        )
        threshold = st.number_input(
            "Set performance increase threshold:",
            min_value=0.0, max_value=1.0, value=0.01,
            help="Minimum performance increase to retain a feature."
        )
        cv = st.slider(
            "select number of cross-validation folds:",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        confirm = st.checkbox("Apply Recursive Feature Addition?")

        if estimator_name and confirm:
            try:
                estimator = eval(estimator_name + "()")  # Create an instance of the estimator
                selector = RecursiveFeatureAddition(
                    estimator=estimator,
                    scoring=scoring,
                    cv=cv,
                    threshold=threshold
                )
                transformed_data = selector.fit_transform(self.dataset)  # Apply recursive feature addition
                st.write("### Attributes:")
                st.json({
                    "initial_model_performance_": selector.initial_model_performance_,
                    "feature_importances_": selector.feature_importances_.to_dict(),
                    "feature_importances_std_": selector.feature_importances_std_.to_dict(),
                    "performance_drifts_": selector.performance_drifts_,
                    "performance_drifts_std_": selector.performance_drifts_std_,
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    def select_by_information_value(self):
        st.subheader("Select Features by Information Value")

        threshold = st.number_input(
            "Set Information Value (IV) threshold: ",
            min_value=0.0, max_value=1.0, value=0.2,
            help="Set the minimum Information Value for features to be retained."
        )
        bins = st.slider(
            "Select number of bins for numerical features:",
            min_value=1, max_value=20, value=5,
            help="Number of bins to discretize numerical features."
        )
        strategy = st.selectbox(
            "Select binning strategy:",
            ["equal_width", "equal_frequency"],
            help="Strategy for creating bins: 'equal_width' or 'equal_frequency'."
        )
        confirm = st.checkbox("Apply SelectByInformationValue?")

        if confirm:
            try:
                selector = SelectByInformationValue(
                    threshold=threshold,
                    bins=bins,
                    strategy=strategy
                )
                transformed_data = selector.fit_transform(self.dataset)  # Apply the feature selection
                st.write("### Attributes:")
                st.json({
                    "information_values_": selector.information_values_,
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    def select_by_shuffling(self):
        st.subheader("Select Features by Shuffling")

        estimator_name = st.text_input(
            "enter the name of a Scikit-learn estimator (e.g., RandomForestClassifier):",
            help="Provide the name of the estimator to be used for feature ranking."
        )
        scoring = st.text_input(
            "enter the scoring metric (default='roc_auc'):",
            value="roc_auc",
            help="Scoring metric to evaluate model performance. See Scikit-learn documentation for valid metrics."
        )
        threshold = st.number_input(
            "set performance decrease threshold: ",
            min_value=0.0, max_value=1.0, value=0.01,
            help="Minimum performance decrease to retain a feature."
        )
        cv = st.slider(
            "select number of cross-validation folds:",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        confirm = st.checkbox("Apply SelectByShuffling?")

        if estimator_name and confirm:
            try:
                estimator = eval(estimator_name + "()")  # Create an instance of the estimator
                selector = SelectByShuffling(
                    estimator=estimator,
                    scoring=scoring,
                    cv=cv,
                    threshold=threshold
                )
                transformed_data = selector.fit_transform(self.dataset)  # Apply feature selection
                st.write("### Attributes:")
                st.json({
                    "initial_model_performance_": selector.initial_model_performance_,
                    "performance_drifts_": selector.performance_drifts_,
                    "performance_drifts_std_": selector.performance_drifts_std_,
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    def select_by_target_mean_performance(self):
        st.subheader("Select Features by Target Mean Performance")

        # User input for different parameters
        variables = st.text_input(
            "enter the variables to evaluate  (comma separated):",
            help="Specify the list of variables to evaluate for feature selection."
        )
        bins = st.slider(
            "select number of bins for numerical variables :",
            min_value=2, max_value=20, value=5,
            help="Number of bins for discretizing numerical variables."
        )
        strategy = st.selectbox(
            "select binning strategy :",
            ["equal_width", "equal_frequency"],
            help="Strategy for binning numerical variables ('equal_width' or 'equal_frequency')."
        )
        scoring = st.text_input(
            "Enter the scoring metric ( default='roc_auc' ):",
            value="roc_auc",
            help="Metric to evaluate the performance of the estimator."
        )
        threshold = st.number_input(
            "set performance threshold: ",
            min_value=0.0, max_value=1.0, value=0.01,
            help="Threshold value to determine whether a feature is retained."
        )
        cv = st.slider(
            "select number of cross-validation folds:",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        regression = st.checkbox(
            "is the target for regression?",
            value=True,
            help="Check this box if the target is for regression tasks."
        )
        confirm = st.checkbox("Apply SelectByTargetMeanPerformance?")

        if confirm:
            try:
                # Prepare the list of variables
                selected_variables = variables.split(",") if variables else None

                # Initialize and apply the feature selection
                selector = SelectByTargetMeanPerformance(
                    variables=selected_variables,
                    bins=bins,
                    strategy=strategy,
                    scoring=scoring,
                    threshold=threshold,
                    cv=cv,
                    regression=regression
                )
                transformed_data = selector.fit_transform(self.dataset)  # Apply feature selection

                # Display the results
                st.write("### Attributes:")
                st.json({
                    "feature_performance_": selector.feature_performance_,
                    "feature_performance_std_": selector.feature_performance_std_,
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                })
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
    
    def select_by_mrmr(self):
        st.subheader("Select Features by MRMR (Minimum Redundancy, Maximum Relevance)")

        # Input fields for MRMR parameters
        variables = st.text_input(
            "enter the variables to evaluate (comma separated):",
            help="Specify the list of variables to evaluate for feature selection."
        )
        method = st.selectbox(
            "select the method to estimate relevance and redundancy:",
            ["MIQ", "MID", "FCD", "FCQ", "RFCQ"],
            help="Method to estimate relevance and redundancy."
        )
        max_features = st.number_input(
            "set the maximum number of features to select:",
            min_value=1, max_value=100, value=20,
            help="Number of features to select."
        )
        n_neighbors = st.slider(
            "select number of neighbors for MI estimation:",
            min_value=1, max_value=10, value=3,
            help="Number of neighbors to use for MI estimation."
        )
        scoring = st.text_input(
            "enter the scoring metric  (default='roc_auc'):",
            value="roc_auc",
            help="Metric to evaluate the performance of the estimator."
        )
        cv = st.slider(
            "Select number of cross-validation folds:",
            min_value=2, max_value=10, value=3,
            help="Number of folds for cross-validation."
        )
        regression = st.checkbox(
            "IS the target for regression?",
            value=True,
            help="Check this box if the target is for regression tasks."
        )
        confirm = st.checkbox("Apply MRMR Feature Selection?")

        if confirm:
            try:
                selected_variables = variables.split(",") if variables else None

                # Initialize the MRMR selector with the user inputs
                selector = MRMR(
                    variables=selected_variables,
                    method=method,
                    max_features=max_features,
                    n_neighbors=n_neighbors,
                    scoring=scoring,
                    cv=cv,
                    regression=regression
                )
                
                # Apply MRMR feature selection
                transformed_data = selector.fit_transform(self.dataset)

                # Display feature selection results
                st.write("### MRMR Feature Selection Results:")
                st.json({
                    "relevance_": selector.relevance_.tolist(),
                    "features_to_drop_": list(selector.features_to_drop_),
                    "variables_": selector.variables_,
                    "feature_names_in_": selector.feature_names_in_,
                    "n_features_in_": selector.n_features_in_,
                },key=50)
                return transformed_data
            except Exception as e:
                st.error(f"An error occurred: {e}")
        return self.dataset
