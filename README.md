# Functional Data Processing Pipeline

## Course Project Documentation

**Repository:** Functional-Data-Processing-Pipeline  
**Language Used:** Python  
**Paradigms Implemented:**
- Pure Functional Programming
- Imperative Programming

---

## Team Members

| Name | ID |
|-----|----|
| Sara Omar Mohamed Abdelaziz | 20220198 |
| Omar Ahmed Ayad Mohamed | 20220311 |
| Sama Sameh Abdelal Ibrahim | 20220212 |
| Omar Ayman Assem Sayed | 20220316 |
| Rehab Abdelghany Mohamed Mohamed | 20220152 |
| Sama Haitham Ezzat Eissa | 20220213 |
| Youssef Wael Attallah | 20220579 |

---

## 1. Project Overview

This project implements a **data processing pipeline** twice using two different programming paradigms:

- **Functional Programming Paradigm**
- **Imperative Programming Paradigm**

The system processes structured datasets (CSV / JSON), cleans and transforms the data, performs statistical analysis, and outputs meaningful results. The goal is to highlight the conceptual and practical differences between the two paradigms while solving the same problem.

---

## 2. Task Motivation

The motivation behind this project is to:

- Understand the **core differences** between functional and imperative programming.
- Compare their **strengths and weaknesses** in real-world data processing tasks.
- Develop better problem‑solving skills by applying different paradigms to the same task.

---

## 3. Task Requirements

The project satisfies the following requirements:

- The same task is implemented twice:
  - Once using **pure functional programming** principles.
  - Once using an **imperative programming** approach.
- The implementation is done using **Python**.
- Both implementations:
  - Load and process datasets.
  - Handle missing and inconsistent data.
  - Perform transformations and analysis.

---

## 2. Input Data Description

The input dataset is provided as a **CSV file** containing sales records with the following fields:

- **Date:** Sales date (multiple formats supported)
- **Region:** Sales region (`North`, `South`, `East`, `West`)
- **Sales:** Current sales value
- **PreviousSales:** Previous sales value
- **Product:** Product name

The dataset intentionally includes:

- Missing values
- Multiple date formats
- Both decimal and integer numeric values

This design makes the dataset suitable for testing **data cleaning, normalization, and transformation techniques**.

---

## 3. Imperative Implementation

### 3.1 Paradigm Overview

The imperative version follows a **step-by-step execution model**:

- Uses explicit loops (`for` statements)
- Relies on mutable data structures (lists and dictionaries)
- Modifies data **in-place**

Each function explicitly defines **how** the computation is performed.

---

### 3.2 Imperative Data Flow

1. Load CSV data using loops
2. Handle missing values by mutating row dictionaries
3. Standardize dates and numeric values in-place
4. Filter rows using conditional logic
5. Compute sales growth and append new fields
6. Aggregate total sales by region
7. Compute statistical summaries
8. Write results to output files

---

### 3.3 Key Characteristics

- Clear execution order
- Easy to trace using print statements
- Efficient for large datasets
- Higher risk of unintended side effects due to mutation

---

## 4. Declarative / Functional Implementation

### 4.1 Paradigm Overview

The declarative (functional) version emphasizes **what should be computed**, not **how**:

- Uses recursion instead of loops
- Avoids mutation (immutable tuples and copied dictionaries)
- Uses higher-order functions (e.g., `recursive_map`, `recursive_filter`)
- Functions are mostly pure

---

### 4.2 Functional Data Flow

Each stage returns a **new data structure**, preserving immutability:

```
Input Tuple
   ↓
handle_missing
   ↓
standardize_dates
   ↓
standardize_numbers
   ↓
filter_rows
   ↓
compute_sales_growth
   ↓
aggregate_sum_by_key / analyze_statistics
```

---

### 4.3 Key Characteristics

- No in-place modification of data
- Easier reasoning and testing
- High readability for functional concepts
- Increased memory usage due to data copying
- Recursion depth limitations in Python

---

## 5. Aggregation and Analysis

### 5.1 Aggregation

The pipeline groups records by **Region** and computes **total sales per region**.

Example output format:

```json
{
  "key": "North",
  "Sales": 123450.75
}
```

---

### 5.2 Statistical Analysis

For numeric columns such as **Sales** and **SalesGrowth**, the pipeline computes:

- Count
- Mean
- Median
- Variance
- Minimum
- Maximum

These statistics provide insights into sales distribution and growth trends.

---

## 6. Imperative vs Declarative Comparison

| Aspect | Imperative | Declarative / Functional |
|------|-----------|-------------------------|
| Control Flow | Explicit loops | Recursion & composition |
| Data Mutation | Mutable | Immutable |
| Readability | Step-by-step | Expression-based |
| Debugging | Easier | Requires tracing recursion |
| Performance | Generally faster | Slight overhead |
| Maintainability | Medium | High |

---

## 7. Use Case Considerations

**Imperative approach is suitable for:**
- Performance-critical pipelines
- Developers new to functional concepts

**Declarative approach is suitable for:**
- Educational purposes
- Safer data transformations
- Complex transformation pipelines

---

## 8. Conclusion

This project demonstrates how the same **data-processing task** can be implemented using two distinct programming paradigms. While the imperative version offers simplicity and performance, the declarative version provides clarity, immutability, and improved reasoning.

By implementing both approaches, the project highlights the trade-offs involved and provides a solid foundation for understanding **paradigm-driven software design** in real-world data processing systems.

---

### 4.2 Data Cleaning

- Handle missing values:
  - Fill missing numerical values with defaults.
  - Remove invalid or incomplete records.
- Standardize data formats:
  - Dates converted to a unified format.
  - Numerical values rounded to fixed precision.

📷 *Screenshot: Missing data handling logic*

---

### 4.3 Data Transformation

The pipeline applies several transformations:

- **Filtering:**
  - Example: Filter records where `Sales > 1000`.
- **Derived Columns:**
  - Example: Compute sales growth or revenue change.
- **Aggregation:**
  - Example: Total sales per region or category.

📷 *Screenshot: Transformation functions (map / filter / reduce)*

---

## 5. Data Analysis

The system performs statistical analysis, including:

- Mean
- Median
- Variance
- Summary statistics for key numerical columns

In the functional implementation, these operations are expressed as **pure functions** without side effects.

📷 *Screenshot: Statistical summary functions*

---

## 6. Functional Programming Implementation

### Key Characteristics

- Emphasis on **pure functions**.
- No shared mutable state.
- Heavy use of:
  - Function composition
  - Recursion instead of loops
  - `map`, `filter`, and `reduce`

### Advantages

- Easier testing and reasoning.
- Predictable behavior.
- Clear separation between logic and I/O.

### Challenges

- More complex for beginners.
- Recursion depth limitations.

📷 *Screenshot: Functional pipeline implementation*

---

## 7. Imperative Programming Implementation

### Key Characteristics

- Step‑by‑step execution.
- Uses loops (`for`, `while`) and mutable variables.
- Direct control flow.

### Advantages

- Easier to understand for beginners.
- Straightforward debugging.

### Challenges

- More prone to side effects.
- Harder to reason about large codebases.

📷 *Screenshot: Imperative version of the pipeline*

---

## 8. Output Results

- Cleaned datasets are saved to output files.
- Statistical summaries are printed to the console.
- Optional visualizations can be generated (bar charts, line graphs).

📷 *Screenshot: Sample output results*

---

## 9. Grading Criteria Coverage

| Paradigm | Score |
|--------|-------|
| Imperative Programming | 5 / 5 |
| Functional Programming | 5 / 5 |

All required features were successfully implemented in both paradigms.

---

## 10. Conclusion

This project demonstrates how the **same data processing problem** can be solved using two fundamentally different programming paradigms. Through this comparison, we gained a deeper understanding of how programming styles influence code structure, maintainability, and problem‑solving strategies.

---

## 11. How to Run the Project

```bash
# Clone the repository
git clone https://github.com/omar3yad/Functional-Data-Processing-Pipeline.git

# Navigate to project directory
cd Functional-Data-Processing-Pipeline

# Run the functional version
python functional_pipeline.py

# Run the imperative version
python imperative_pipeline.py
```

---

**Prepared by:** The Project Team
