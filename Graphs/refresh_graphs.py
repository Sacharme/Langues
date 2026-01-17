"""
Utility script to refresh all graphs from CSV data.
Run this script after manually editing CSV files to regenerate the corresponding graphs.
"""

import os
import sys
import csv
from datetime import datetime
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.dates as mdates
import numpy as np

# Get the base directory (parent of Graphs folder)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Configuration for each language/category
CONFIGS = {
    'Spanish': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Spanish'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Spanish'),
        'categories': {
            'vocabulaire': {'file': 'vocabulaire', 'goal': 75, 'name': 'Vocabulary'},
            'reguliers': {'file': 'conjugaison_reguliers', 'goal': 80, 'name': 'Regular Conjugation'},
            'irreguliers': {'file': 'conjugaison_irreguliers', 'goal': 70, 'name': 'Irregular Conjugation'},
            'tout': {'file': 'tout', 'goal': 70, 'name': 'All (Verbs + Vocabulary)'}
        },
        'title_prefix': 'Spanish Progress'
    },
    'Portuguese': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Portuguese'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Portuguese'),
        'categories': {
            'vocabulaire': {'file': 'vocabulaire', 'goal': 75, 'name': 'Vocabulary'},
            'reguliers': {'file': 'conjugaison_reguliers', 'goal': 80, 'name': 'Regular Conjugation'},
            'irreguliers': {'file': 'conjugaison_irreguliers', 'goal': 70, 'name': 'Irregular Conjugation'},
            'tout': {'file': 'tout', 'goal': 70, 'name': 'All (Verbs + Vocabulary)'}
        },
        'title_prefix': 'Portuguese Progress'
    },
    'Russian Alphabet': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Russian Alphabet'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Russian Alphabet'),
        'categories': {
            'alphabet': {'file': 'alphabet', 'goal': 95, 'name': 'Alphabet'}
        },
        'title_prefix': 'Russian Alphabet Progress'
    },
    'Arabic Alphabet': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Arabic Alphabet'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Arabic Alphabet'),
        'categories': {
            'alphabet': {'file': 'alphabet', 'goal': 95, 'name': 'Alphabet'}
        },
        'title_prefix': 'Arabic Alphabet Progress'
    },
    'Greek Alphabet': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Greek Alphabet'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Greek Alphabet'),
        'categories': {
            'alphabet': {'file': 'alphabet', 'goal': 95, 'name': 'Alphabet'}
        },
        'title_prefix': 'Greek Alphabet Progress'
    },
    'Korean Alphabet': {
        'data_dir': os.path.join(BASE_DIR, 'Data', 'Korean Alphabet'),
        'graphs_dir': os.path.join(BASE_DIR, 'Graphs', 'Korean Alphabet'),
        'categories': {
            'alphabet': {'file': 'alphabet', 'goal': 95, 'name': 'Alphabet'}
        },
        'title_prefix': 'Korean Alphabet (Hangul) Progress'
    }
}


def generate_3d_graph(csv_file, graph_file, goal, title):
    """Generates a 3D progress graph from CSV data"""
    if not os.path.exists(csv_file):
        print(f"  [!] CSV file not found: {csv_file}")
        return False
    
    dates = []
    attempts = []
    percentages = []
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                dates.append(datetime.strptime(row['date'], '%Y-%m-%d'))
                attempts.append(int(row['attempts']))
                percentages.append(float(row['percentage']))
            except (ValueError, KeyError) as e:
                print(f"  [!] Error parsing row: {row} - {e}")
                continue
    
    if not dates:
        print(f"  [!] No valid data found in: {csv_file}")
        return False
    
    # Create graphs directory if it doesn't exist
    os.makedirs(os.path.dirname(graph_file), exist_ok=True)
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Convert dates to numbers for the graph
    date_nums = mdates.date2num(dates)
    
    # Progress points
    ax.scatter(attempts, date_nums, percentages, c='blue', s=100, marker='o', label='Scores')
    
    # Line connecting points
    if len(dates) > 1:
        ax.plot(attempts, date_nums, percentages, c='blue', alpha=0.5)
    
    # Fix Z-axis limits (0 to 100%)
    ax.set_zlim(0, 100)
    
    # Goal plane (horizontal plane at goal percentage)
    if attempts and dates:
        x_min, x_max = min(attempts), max(attempts)
        x_margin = max(1, (x_max - x_min) * 0.1)
        y_min, y_max = min(date_nums), max(date_nums)
        y_margin = max(0.5, (y_max - y_min) * 0.1)
        
        x_range = [x_min - x_margin, x_max + x_margin]
        y_range = [y_min - y_margin, y_max + y_margin]
        X, Y = np.meshgrid(x_range, y_range)
        Z = np.full_like(X, goal, dtype=float)
        ax.plot_surface(X, Y, Z, alpha=0.4, color='red', edgecolor='darkred', linewidth=2)
    
    ax.set_xlabel('Number of attempts')
    ax.set_ylabel('Date')
    ax.set_zlabel('Success rate (%)')
    ax.set_title(f'{title} (Goal: {goal}%)')
    
    # Format Y-axis to display dates
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: mdates.num2date(x).strftime('%d/%m')))
    
    plt.tight_layout()
    plt.savefig(graph_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    return True


def refresh_all_graphs():
    """Refreshes all graphs for all languages"""
    print("=" * 50)
    print("Refreshing all graphs...")
    print("=" * 50)
    
    total_refreshed = 0
    total_errors = 0
    
    for language, config in CONFIGS.items():
        print(f"\n{language}:")
        
        for category_key, category_info in config['categories'].items():
            csv_file = os.path.join(config['data_dir'], f"{category_info['file']}.csv")
            graph_file = os.path.join(config['graphs_dir'], f"{category_info['file']}_progress.png")
            title = f"{config['title_prefix']} - {category_info['name']}"
            goal = category_info['goal']
            
            if generate_3d_graph(csv_file, graph_file, goal, title):
                print(f"  [OK] {category_info['name']} graph refreshed")
                total_refreshed += 1
            else:
                total_errors += 1
    
    print("\n" + "=" * 50)
    print(f"Done! {total_refreshed} graphs refreshed, {total_errors} errors")
    print("=" * 50)


def refresh_language(language):
    """Refreshes graphs for a specific language"""
    if language not in CONFIGS:
        print(f"Unknown language: {language}")
        print(f"Available languages: {', '.join(CONFIGS.keys())}")
        return
    
    config = CONFIGS[language]
    print(f"\nRefreshing {language} graphs...")
    
    for category_key, category_info in config['categories'].items():
        csv_file = os.path.join(config['data_dir'], f"{category_info['file']}.csv")
        graph_file = os.path.join(config['graphs_dir'], f"{category_info['file']}_progress.png")
        title = f"{config['title_prefix']} - {category_info['name']}"
        goal = category_info['goal']
        
        if generate_3d_graph(csv_file, graph_file, goal, title):
            print(f"  [OK] {category_info['name']} graph refreshed")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Refresh specific language
        language = sys.argv[1]
        refresh_language(language)
    else:
        # Refresh all graphs
        refresh_all_graphs()
