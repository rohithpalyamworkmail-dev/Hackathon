import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

class Plots:
    def __init__(self, data: pd.DataFrame):
        self.data = data
    
    def display(self):
        st.subheader("Basic Plots",divider='blue')
        tab1, tab2 = st.tabs(["Basic Plots", "Advanced Plots"])
        
        with tab1:
            col1,col2=st.columns([1,2],border=True)
            with col1:
                st.subheader("Configure Plot Parameters")
                
                # Select columns
                columns = st.multiselect("Select columns to plot", self.data.columns.tolist())
                
                # Select kind of plot
                kind = st.selectbox("Select plot type", ["line", "bar", "barh", "hist", "box", "kde", "density", "area", "pie", "scatter", "hexbin"], index=0)
                
                # Other parameters
                subplots = st.checkbox("Subplots", value=False)
                sharex = st.checkbox("Share X-axis", value=True)
                sharey = st.checkbox("Share Y-axis", value=False)
                layout = st.text_input("Layout (rows, cols)", "")
                figsize = st.text_input("Figure Size (width, height)", "")
                use_index = st.checkbox("Use Index", value=True)
                title = st.text_input("Title", "")
                grid = st.checkbox("Grid", value=False)
                legend = st.checkbox("Legend", value=True)
                logx = st.checkbox("Log X-axis", value=False)
                logy = st.checkbox("Log Y-axis", value=False)
                loglog = st.checkbox("Log Both Axes", value=False)
                xlabel = st.text_input("X-axis Label", "")
                ylabel = st.text_input("Y-axis Label", "")
                rot = st.number_input("Rotation", value=0)
                fontsize = st.number_input("Font Size", value=12)
                stacked = st.checkbox("Stacked (for bar/area)", value=False)
                secondary_y = st.checkbox("Secondary Y-axis", value=False)
                mark_right = st.checkbox("Mark Right Axis", value=True)
                plot_button = st.button("Plot",use_container_width=True)
                    
                with col2:
                    if plot_button and columns:
                        fig, ax = plt.subplots(figsize=eval(figsize) if figsize else (8, 6))
                        self.data[columns].plot(
                            kind=kind,
                            subplots=subplots,
                            sharex=sharex,
                            sharey=sharey,
                            layout=eval(layout) if layout else None,
                            figsize=eval(figsize) if figsize else None,
                            use_index=use_index,
                            title=title,
                            grid=grid,
                            legend=legend,
                            logx=logx,
                            logy=logy,
                            loglog=loglog,
                            xlabel=xlabel,
                            ylabel=ylabel,
                            rot=rot,
                            fontsize=fontsize,
                            stacked=stacked,
                            secondary_y=secondary_y,
                            mark_right=mark_right,
                            ax=ax
                        )
                        st.pyplot(fig)
        
        with tab2:
            self.advanced_plots(col1,col2)
    def advanced_plots(self,col1,col2):
        st.subheader("Advanced Plots",divider='blue')
        col1,col2=st.columns([1,2],border=True)
        options=col1.radio("Select options to perform",["Value Counts","Aggregration Operations"])
        if options=="Value Counts":
            self.value_counts(col1,col2)
        if options=="Aggregration Operations":
            self.aggregations(col1,col2)
    def aggregations(self, col1, col2):
        col2.subheader("Aggregation Operations")
        agg_columns = col2.multiselect("Select Columns for aggregation", self.data.columns.tolist())
        agg_funcs = col2.multiselect("Select Aggregation functions", ["sum", "mean", "median", "min", "max", "count"])
        kind = col2.selectbox("Select Plot type", ["line", "bar", "barh", "hist", "box", "kde", "density", "area", "pie", "scatter", "hexbin"], index=0)
        plot_button = col2.button("Generate Aggregation Plot",use_container_width=True)
        
        if plot_button and agg_columns and agg_funcs:
            agg_data = self.data[agg_columns].agg(agg_funcs)
            fig, ax = plt.subplots()
            agg_data.plot(kind=kind, ax=ax)
            col2.pyplot(fig)
            col2.subheader("This Aggregation DatFrame Is Used To Plot The Plot",divider='grey')
            col2.dataframe(agg_data)
    
    def value_counts(self, col1, col2):
        col2.subheader("Value Counts")
        value_column = col2.multiselect("Select Column for value counts", self.data.columns.tolist())
        kind = col2.selectbox("Select plot Type", ["line", "bar", "barh", "hist", "box", "kde", "density", "area", "pie", "scatter", "hexbin"], index=0)
        plot_button = col2.button("Generate Value Counts Plot",use_container_width=True)
        
        if plot_button and value_column:
            value_counts = self.data[value_column].value_counts()
            fig, ax = plt.subplots()
            value_counts.plot(kind=kind, ax=ax)
            col2.pyplot(fig)
            col2.subheader("This Is The DataFrame Used To Plot")
            col2.dataframe(value_counts)
