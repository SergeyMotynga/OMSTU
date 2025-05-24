from CarDatasetGenerator import CarDatasetGenerator
import os

def main():
    base_dir = r'C:\Users\motyn\Desktop\Repositories\OMSTU\Practicum\laboratory\lab_5'
    data_dir = os.path.join(base_dir, 'data')
    os.makedirs(data_dir, exist_ok=True)

    csv_path = os.path.join(data_dir, 'new_data.csv')
    print("Путь для сохранения new_data.csv:", csv_path)

    generator = CarDatasetGenerator(n_features=7, threshold=28, random_state=42)
    train_df = generator.generate_pairs_dataset(pairs_required=200)
    train_df.to_csv(csv_path, index=False)

    print("new_data.csv создан!")

if __name__ == "__main__":
    main()
