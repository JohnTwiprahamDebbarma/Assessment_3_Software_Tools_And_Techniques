import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def analyze_lcom_results(output_dir):
    print(f"Looking for LCOM results in: {output_dir}")
    if not os.path.exists(output_dir):
        print(f"Error: Output directory '{output_dir}' does not exist!")
        return None
    print("Files in output directory:")
    for file in os.listdir(output_dir):
        print(f"- {file}")
    
    # Look for TypeMetrics.csv
    metrics_file = os.path.join(output_dir, "TypeMetrics.csv")
    if not os.path.exists(metrics_file):
        # Try to find any CSV file if TypeMetrics.csv is not found
        csv_files = [f for f in os.listdir(output_dir) if f.endswith('.csv')]
        if csv_files:
            metrics_file = os.path.join(output_dir, csv_files[0])
            print(f"Found CSV file: {metrics_file}")
        else:
            print("Error: No CSV files found in the output directory!")
            return None
    
    # Load LCOM results from CSV
    try:
        df = pd.read_csv(metrics_file)
        print(f"Successfully loaded LCOM data with {len(df)} classes")
        
        # Print column names to verify structure
        print("CSV columns:", df.columns.tolist())
        
        # Create a ClassName column as a combination of package and type name for better readability
        try:
            df['ClassName'] = df['Package Name'] + '.' + df['Type Name']
        except KeyError:
            # If columns are different, try to identify the right ones
            if 'Type Name' in df.columns:
                df['ClassName'] = df['Type Name']
            else:
                # Find any column that might contain class names
                for col in df.columns:
                    if 'class' in col.lower() or 'type' in col.lower() or 'name' in col.lower():
                        df['ClassName'] = df[col]
                        break
                if 'ClassName' not in df.columns:
                    df['ClassName'] = df.iloc[:, 0]  # Use first column as fallback
        
        # Sort by LCOM1 (or another metric of choice)
        df_sorted = df.sort_values(by='LCOM1', ascending=False)
        
        print("==== LCOM Analysis Results ====")
        print("\nTop 10 classes with highest LCOM1 values:")
        print(df_sorted[['ClassName', 'LCOM1']].head(10))
        
        # Show other metrics if available
        if 'LCOM5' in df.columns:
            print("\nTop 10 classes with highest LCOM5 values:")
            print(df_sorted.sort_values(by='LCOM5', ascending=False)[['ClassName', 'LCOM5']].head(10))
        
        if 'YALCOM' in df.columns:
            print("\nTop 10 classes with highest YALCOM values:")
            print(df_sorted.sort_values(by='YALCOM', ascending=False)[['ClassName', 'YALCOM']].head(10))
        
        # Classes with concerning cohesion (high LCOM values)
        print("\n==== Classes with High LCOM Values ====")
        
        # Adaptive thresholds based on the data distribution
        lcom1_threshold = df['LCOM1'].quantile(0.9)  # Top 10% of values
        print(f"Using LCOM1 threshold of {lcom1_threshold}")
        
        # Create filter conditions based on available columns
        filter_conditions = (df['LCOM1'] > lcom1_threshold)
        
        if 'LCOM5' in df.columns and not df['LCOM5'].isna().all():
            lcom5_threshold = df['LCOM5'].quantile(0.9)
            filter_conditions = filter_conditions | (df['LCOM5'] > lcom5_threshold)
        
        concerning_classes = df[filter_conditions]
        
        if not concerning_classes.empty:
            print("\nClasses that may need functional decomposition:")
            metrics_cols = [col for col in df.columns if 'LCOM' in col]
            print(concerning_classes[['ClassName'] + metrics_cols])
        else:
            print("\nNo classes with critically high LCOM values found.")
        
        # Create visualizations
        print("\nGenerating visualizations...")
        try:
            # Select the top 15 classes for visualization
            top_classes = df_sorted.head(15)
            
            # Create a heatmap of the LCOM metrics
            plt.figure(figsize=(12, 8))
            
            # Use shortened class names for better readability
            class_names = top_classes['ClassName'].apply(lambda x: x.split('.')[-1] if '.' in str(x) else x)
            
            # Prepare the data for heatmap - only select LCOM metric columns
            heatmap_cols = [col for col in df.columns if 'LCOM' in col]
            heatmap_data = top_classes[heatmap_cols].copy()
            heatmap_data.index = class_names
            
            sns.heatmap(
                heatmap_data, 
                annot=True, 
                cmap="YlOrRd"
            )
            plt.title("LCOM Metrics for Top 15 Classes")
            plt.savefig("lcom_heatmap.png", bbox_inches='tight')
            print("Saved LCOM metrics heatmap to lcom_heatmap.png")
            
            # Create a bar chart for LCOM1
            plt.figure(figsize=(14, 8))
            
            # Create a new DataFrame with shortened class names
            bar_data = pd.DataFrame({
                'ClassName': class_names,
                'LCOM1': top_classes['LCOM1'].values
            })
            
            sns.barplot(x='ClassName', y='LCOM1', data=bar_data)
            plt.title("LCOM1 Values for Top 15 Classes")
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            plt.savefig("lcom1_barchart.png")
            print("Saved LCOM1 bar chart to lcom1_barchart.png")
            
        except Exception as e:
            print(f"Warning: Error creating visualizations: {e}")
            import traceback
            traceback.print_exc()
        
        # Save the results to a CSV file for further analysis
        df_sorted.to_csv("lcom_results.csv", index=False)
        print("Saved LCOM results to lcom_results.csv")
        
        return df_sorted
    except Exception as e:
        print(f"Error analyzing LCOM results: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    import sys
    
    # Allow specifying the output directory as a command line argument
    if len(sys.argv) > 1:
        output_dir = sys.argv[1]
    else:
        output_dir = "lcom_output"
    
    lcom_results = analyze_lcom_results(output_dir)
    
    if lcom_results is not None:
        print("\nAnalysis complete. Visualizations saved as lcom_heatmap.png and lcom1_barchart.png")
    else:
        print("\nAnalysis failed. Please check the error messages above.")
