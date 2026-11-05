```
Data Ingestion
├─ Batch
├─ Incremental
│  └─ CDC (specialized incremental)
├─ API-Based
│  └─ REST API
└─ File-Based
   ├─ SFTP
   └─ Object Storage (S3 / Azure Blob / GCS)
```

---

## High‑Level Data Ingestion Types (Corrected)

### 1. **Batch Ingestion**

**Definition:**  
Data is extracted, transported, and loaded **as a discrete snapshot** at a scheduled interval (e.g., nightly, weekly).

**Key Characteristics**

- Full or partial table reloads
- Time‑based execution
- Deterministic boundaries
- Higher latency accepted

**Typical Use Cases**

- Financial close data
- Slowly changing reference data
- Legacy systems without change tracking

---

### 2. **Incremental Ingestion**

**Definition:**  
Only **new or modified records since the last successful load** are ingested.

**Key Characteristics**

- Delta‑based
- Requires watermark or high‑water mark (timestamp, ID)
- Lower data movement than batch
- Still schedule‑driven

**Important Clarification**

- **CDC is a specialized subtype of incremental ingestion**, not equivalent.

**Typical Use Cases**

- Operational reporting
- Large fact tables
- Systems without native CDC but with reliable timestamps

---

### 3. **Change Data Capture (CDC)**

**Definition:**  
Ingestion driven by **transaction‑level change events** (INSERT / UPDATE / DELETE) from the source system.

**Key Characteristics**

- Log‑based or trigger‑based
- Event‑level fidelity
- Preserves operation type
- Near‑real‑time or micro‑batch

**Common Implementations**

- Database transaction logs
- Debezium / SQL Server CDC / Oracle GoldenGate

**Architectural Note** CDC is the **highest‑fidelity ingestion pattern**, but also the highest operational complexity.

---

### 4. **API‑Based Ingestion**

**Definition:**  
Data is pulled or pushed via **application‑level programmatic interfaces**, not files.

#### 4a. **REST API**

**Definition:**  
A stateless, HTTP‑based API exposing data through endpoints, typically JSON.

**Key Characteristics**

- Pagination & rate limits
- Authentication (OAuth, keys)
- Often logical (not physical) data models
- Incremental supported via parameters

**Typical Use Cases**

- SaaS platforms
- Operational systems
- External partners

✅ **Correction:** REST APIs are **not** file drops.

---

### 5. **File‑Based Ingestion (File Drops)**

**Definition:**  
Data is delivered as **physical files** placed in a known landing location.

#### 5a. **SFTP**

**Definition:**  
Secure, managed file transfer over SSH.

**Characteristics**

- Push‑based
- Batch‑oriented
- Manual or scheduled delivery
- Minimal metadata

**Use Cases**

- Vendor feeds
- Payroll, benefits, banking integrations

---

#### 5b. **Object Storage (e.g., S3 Blob / Azure Blob / GCS)**

**Definition:**  
Files are delivered to **cloud object storage** and consumed asynchronously.

**Characteristics**

- Event‑driven ingestion possible
- Scales well for large volumes
- Supports structured & semi‑structured data
- Often used with data lake architectures

✅ **Terminology Correction:**  
“S3 Blob” → **Amazon S3 (Object Storage)**  
“Blob” is Azure’s term; the generic category is **object storage**.

---

## Final Corrected Taxonomy

```
Data Ingestion
├─ Batch
├─ Incremental
│  └─ CDC (specialized incremental)
├─ API-Based
│  └─ REST API
└─ File-Based
   ├─ SFTP
   └─ Object Storage (S3 / Azure Blob / GCS)
```

---

## Key Corrections Summary

|Issue|Correction|
|---|---|
|REST API listed twice|REST API is **API‑based only**, not file‑based|
|CDC = Incremental|CDC is **a subtype**, not a synonym|
|“S3 Blob” term|Use **Object Storage (S3 / Azure Blob)**|
|Ingestion types mixed with transport|Separated **method** vs **delivery mechanism**|

---

If you want, next logical extensions:

- Add **latency classes** (batch vs near‑real‑time vs streaming)
- Add **failure‑mode profiles** by ingestion type
- Map ingestion type → **testing strategy**
- Formalize this into **architecture standards language**

Say the word.