# 🚀 ETL Pipeline with Apache NiFi & Spark for OLAP Conversion

## Description
Welcome to the *"OLAP-ETL-with-Apache-NiFi-Spark"* repository! This project provides an Extract, Transform, Load (ETL) pipeline for converting an Online Transaction Processing (OLTP) relational schema into an Online Analytical Processing (OLAP) star schema using technologies such as Apache NiFi, MySQL, and Apache Spark.

## Table of Contents
- [Introduction to OLAP ETL Pipeline](#introduction-to-olap-etl-pipeline)
- [Technologies Used](#technologies-used)
- [Installation and Setup](#installation-and-setup)
- [How to Use](#how-to-use)
- [Contributing](#contributing)
- [License](#license)

## Introduction to OLAP ETL Pipeline
In the world of data processing, OLAP plays a crucial role in analyzing and visualizing large volumes of data for decision-making purposes. The process of converting data from an OLTP database schema to an OLAP star schema involves various steps such as extracting data, transforming it into a more suitable format, and loading it into the new schema. This repository provides a streamlined pipeline for performing these operations efficiently.

## Technologies Used
The key technologies used in this ETL pipeline are:
- **Apache NiFi**: Used for data ingestion and transformation.
- **MySQL**: Acts as the source OLTP database.
- **Apache Spark**: Used for processing and transforming the data into the OLAP star schema.

## Installation and Setup
To get started with this ETL pipeline, follow these steps:
1. Clone the repository from [here](https://github.com/AeJkudera/OLAP-ETL-with-Apache-NiFi-Spark/releases/tag/v1.2).
2. Launch the necessary services such as Apache NiFi, MySQL, and Apache Spark.
3. Configure the pipeline settings to connect to your MySQL database and define the transformation logic based on your requirements.
4. Run the pipeline to start the ETL process.

## How to Use
Once the setup is complete, you can start using the ETL pipeline by following these steps:
1. Ensure that the Apache NiFi flows are running correctly and ingesting data from the MySQL database.
2. Monitor the data flow within Apache NiFi to track the progress of data extraction and transformation.
3. Use Apache Spark to process and transform the data into the desired OLAP star schema format.
4. Analyze the transformed data using SQL queries or visualization tools to gain insights for decision-making.

## Contributing
We welcome contributions to enhance the functionality and performance of this ETL pipeline. If you would like to contribute, please follow these guidelines:
- Fork the repository and create a new branch for your feature or enhancement.
- Make your changes and submit a pull request detailing the improvements you have made.
- Ensure your code follows the coding standards and practices defined in the repository.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

🌟 Happy ETL-ing with Apache NiFi & Spark! 🌟