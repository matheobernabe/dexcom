import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from typing import Tuple, List

class GraphManager:
    def __init__(self, data_manager):
        self.data_manager = data_manager

    def generate_daily_graph(self) -> Tuple[plt.Figure, List[float]]:
        """Génère un graphique journalier des glycémies"""
        df = self.data_manager.get_glucose_history(hours=24)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        # Tracé des glycémies
        ax.plot(df['timestamp'], df['glucose_level'], '-b', label='Glucose')
        
        # Zones de glycémie
        ax.axhspan(70, 180, color='g', alpha=0.1, label='Plage cible')
        ax.axhline(y=70, color='r', linestyle='--', label='Hypo')
        ax.axhline(y=180, color='r', linestyle='--', label='Hyper')
        
        # Ajout des doses d'insuline
        insulin_df = self.data_manager.get_insulin_history(hours=24)
        if not insulin_df.empty:
            insulin_df['timestamp'] = pd.to_datetime(insulin_df['timestamp'])
            ax.scatter(insulin_df['timestamp'], 
                      [40] * len(insulin_df),  # Placer les marqueurs en bas
                      marker='^', 
                      color='r',
                      label='Insuline')
            
            # Ajouter les doses d'insuline comme annotations
            for idx, row in insulin_df.iterrows():
                ax.annotate(f"{row['units']}U", 
                          (row['timestamp'], 40),
                          xytext=(0, 10),
                          textcoords='offset points',
                          ha='center')
        
        ax.set_title('Suivi Glycémique sur 24h')
        ax.set_xlabel('Heure')
        ax.set_ylabel('Glucose (mg/dL)')
        ax.legend()
        
        # Calculer les statistiques
        stats = self._calculate_statistics(df)
        
        return fig, stats

    def _calculate_statistics(self, df: pd.DataFrame) -> List[float]:
        """Calcule les statistiques importantes"""
        if df.empty:
            return [0, 0, 0, 0]
            
        time_in_range = len(df[(df['glucose_level'] >= 70) & 
                              (df['glucose_level'] <= 180)]) / len(df) * 100
        average_glucose = df['glucose_level'].mean()
        max_glucose = df['glucose_level'].max()
        min_glucose = df['glucose_level'].min()
        
        return [time_in_range, average_glucose, max_glucose, min_glucose]