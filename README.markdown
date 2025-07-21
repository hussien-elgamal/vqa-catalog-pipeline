# VQA Catalog Pipeline

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Airflow](https://img.shields.io/badge/Apache%20Airflow-2.6+-orange.svg)
![Docker](https://img.shields.io/badge/Docker-20.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 📋 Project Overview

The **VQA Catalog Pipeline** is a data engineering project designed to process Visual Question Answering (VQA) datasets, enabling the preparation of data for AI model training. The pipeline automates the extraction, transformation, and validation of image embeddings, annotations, and catalog data using **Apache Airflow** for orchestration, **Docker** for containerization, and **Python** for data processing. The project leverages the **COCO dataset**, **VQA questions**, and **CLIP model** from OpenAI to generate embeddings and build a structured product catalog.

### Key Features
- **Data Ingestion**: Loads raw COCO images, VQA questions, and annotations.
- **Image Preprocessing**: Resizes images to 256x256 and converts to JPEG format.
- **Embedding Extraction**: Uses OpenAI's CLIP model to generate image embeddings.
- **Catalog Creation**: Builds a product catalog with image metadata and questions.
- **Consistency Checks**: Validates consistency between catalog, embeddings, and annotations.
- **Automation**: Orchestrates tasks using Apache Airflow DAGs.
- **Reproducibility**: Containerized with Docker and version-controlled on GitHub.

## 🗂️ Project Structure

```
vqa-catalog-pipeline/
├── config/                        # Airflow configuration
│   └── airflow.cfg
├── dags/                          # Airflow DAGs
│   ├── catalog_pipeline.py
│   ├── catalog_consistency_check.py
│   ├── vqa_embedding_pipeline.py
│   ├── vqa_full_pipeline.py
├── data/                          # Data storage
│   ├── embeddings/
│   │   ├── annotation/
│   │   │   ├── train_annotations.parquet
│   │   │   ├── val_annotations.parquet
│   │   ├── image/
│   │   │   ├── train_embeddings.parquet
│   │   │   ├── val_embeddings.parquet
│   │   │   ├── test_embeddings.parquet
│   ├── reports/                   # Consistency check reports
│   │   ├── missing_in_annotations.csv
│   │   ├── missing_in_embeddings.csv
│   ├── vqa_ready/                 # Processed datasets
│   │   ├── train_data.parquet
│   │   ├── val_data.parquet
│   ├── vqa_questions_cleaned/      # Cleaned VQA questions
│   │   ├── v2_OpenEnded_mscoco_train2014_questions.json
│   │   ├── v2_OpenEnded_mscoco_val2014_questions.json
│   │   ├── v2_OpenEnded_mscoco_test2015_questions.json
│   ├── train2014_preprocessed/    # Preprocessed images
│   │   └── train2014_preprocessed.zip
│   ├── catalog_stage.csv
│   ├── catalog_raw.json
│   ├── catalog_final.parquet
├── .env                           # Environment variables
├── Dockerfile                     # Docker image configuration
├── docker-compose.yaml            # Docker Compose for Airflow
├── requirements.txt               # Python dependencies
├── README.md                      # This file
```

## 🚀 Getting Started

### Prerequisites
- **Python** 3.9+
- **Docker** and **Docker Compose**
- **Git** for version control
- Access to **MEGA** for downloading preprocessed images (optional)
- Sufficient storage for COCO datasets and embeddings (~50GB)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/hussien-elgamal/vqa-catalog-pipeline.git
   cd vqa-catalog-pipeline
   ```

2. **Set Up Environment Variables**:
   - Create a `.env` file in the root directory with necessary configurations (e.g., Airflow settings, MEGA credentials).
   - Example:
     ```
     AIRFLOW_UID=50000
     MEGA_EMAIL=your_email
     MEGA_PASSWORD=your_password
     ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Build and Run Docker Containers**:
   ```bash
   docker-compose up -d
   ```

5. **Access Airflow Web UI**:
   - Open `http://localhost:8080` in your browser.
   - Default credentials: `airflow` / `airflow`

6. **Download Preprocessed Images** (Optional):
   - Use `megadl` to download `train2014_preprocessed.zip` from MEGA and extract it to `data/train2014_preprocessed/`.

### Running the Pipeline
1. Trigger the `vqa_full_pipeline` DAG in the Airflow UI to execute the entire workflow:
   - `vqa_embedding_pipeline`: Generates image and annotation embeddings.
   - `generate_vqa_catalog`: Creates the product catalog.
   - `catalog_consistency_check`: Validates data consistency.

2. Monitor logs and reports in `data/reports/` for any inconsistencies.

## ⚙️ Pipeline Stages

1. **Data Ingestion**:
   - Downloads COCO images (`train2014`, `val2014`, `test2015`) and VQA questions/annotations.
2. **Image Preprocessing**:
   - Resizes images to 256x256 and converts to JPEG using PIL.
3. **Question Cleaning**:
   - Converts questions to lowercase and removes extra spaces.
4. **Embedding Extraction**:
   - Uses CLIP model to generate image embeddings, stored as `.parquet` files.
5. **Catalog Generation**:
   - Merges images and questions to create `catalog_final.parquet`.
6. **Consistency Check**:
   - Ensures all images in the catalog have corresponding embeddings and annotations.
7. **Output**:
   - Processed datasets in `data/vqa_ready/` and reports in `data/reports/`.

## 🧪 Technologies Used
- **Python Libraries**: Pandas, PyArrow, TQDM, Transformers, Torch
- **Machine Learning**: OpenAI CLIP model
- **Data Storage**: Parquet, JSON, CSV
- **Orchestration**: Apache Airflow
- **Containerization**: Docker, Docker Compose
- **Version Control**: Git
- **File Transfer**: rclone, megadl

## 📊 Outputs
- **Catalog**: `catalog_final.parquet` with product IDs, image IDs, paths, and titles.
- **Embeddings**: `train_embeddings.parquet`, `val_embeddings.parquet`.
- **Annotations**: `train_annotations.parquet`, `val_annotations.parquet`.
- **Training Data**: `train_data.parquet`, `val_data.parquet`.
- **Reports**: `missing_in_annotations.csv`, `missing_in_embeddings.csv`.

## 🛠️ Troubleshooting
- **Missing Files**: Ensure all data paths in DAGs match your local setup.
- **Airflow Errors**: Check logs in the Airflow UI or `docker-compose logs`.
- **MEGA Download Issues**: Verify credentials in `.env` and `megadl` installation.

## 🤝 Contributing
Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## 📜 License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 📧 Contact
For questions or support, contact [Hussien Elgamal](mailto:hussienelgamal8@gmail.com) or open an issue on GitHub.
