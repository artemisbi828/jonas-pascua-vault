aka: "also known as"
syn: synonym or alias (alt name, same entity)
eq: equivalence
# Snowflaking


> [!info] "I am a special snowflake"
Opposite of Semantic Logic (true meaning/essence of logic; non-technical)

Marketers/branders create new names (and add entropy to the universe) by creating multiple names for the same semantic meaning. It makes sense WHY they do it, just from the perspective of being a rebel of entropy -- we're on the opposite side. 

Charitable: Semantic differentiation; Lexical positioning; narrative positioning
Middle: Language Inflation, Concept Fragmentation
Cynical: **Semantic Entropy**, Snowflaking, Buzzword-ization 

IMPETUS: Creates
- Cognitive Dissonance --> Creates "Are these the same thing?" meetings
- Data Model Misalignment
- Vocabulary Drift

# UX 
Users are **cognitively economical** (cynical and extreme: lazy)
* low-friction oriented
* mental-model driven - inconsisteency forces relearning
Users like reading gravity
- American: `Top Left` -> `Bottom Right`
- {Japanese, Chinese}: `Top Right` -> `Bottom Left`


# Data Entropy
| Goal               | Useful Terms                     |
| ------------------ | -------------------------------- |
| Match meaning      | synonym, equivalent, paraphrase  |
| Oppose meaning     | antonym, converse                |
| Avoid traps        | homonym, misnomer, ambiguity     |
| Model hierarchy    | hypernym, hyponym, taxonomy      |
| Model structure    | meronym, holonym                 |
| Model independence | orthogonal, cross‑cutting        |
| Stabilize meaning  | canonical, alias, disambiguation |

***

## 1. Similarity & Sameness

### **Synonym**

*   **Definition:** Different words with the *same or very similar meaning*.
*   **Example:** *big* ↔ *large*
*   **Note:** True synonyms are rare; most are **near‑synonyms**.

### **Near‑synonym**

*   **Definition:** Words with overlapping meaning but different nuance, register, or usage.
*   **Example:** *accurate* vs *precise*

### **Paraphrase**

*   **Definition:** Rewording the same meaning using different language.
*   **Example:** “He died” → “He passed away”

### **Equivalent term**

*   **Definition:** Different labels used interchangeably within a specific context or system.
*   **Example:** *Customer ID* = *Client Key* (in a data model)

***

## 2. Difference & Opposition

### **Antonym**

*   **Definition:** Words with opposite meanings.
*   **Example:** *hot* ↔ *cold*

#### Subtypes of Antonyms:

*   **Gradable antonyms:** *hot* ↔ *cold* (spectrum)
*   **Complementary antonyms:** *dead* ↔ *alive* (binary)
*   **Converse / relational antonyms:** *parent* ↔ *child*, *buy* ↔ *sell*

### **Contrast term**

*   **Definition:** Words contrasted to highlight differences, not necessarily opposites.
*   **Example:** *urban* vs *suburban*

***

## 3. Sameness-in-Form, Difference-in-Meaning (⚠️ Traps)

### **Homonym**

*   **Definition:** Same spelling or pronunciation, **different meanings**.
*   **Example:** *bank* (river) vs *bank* (finance)

### **Homograph**

*   **Definition:** Same spelling, different meaning (pronunciation may differ).
*   **Example:** *lead* (metal) vs *lead* (verb)

### **Homophone**

*   **Definition:** Same pronunciation, different spelling/meaning.
*   **Example:** *their* / *there*

### **Polysemy**

*   **Definition:** One word with **related meanings**.
*   **Example:** *mouth* (person) → *mouth* (river)

***

## 4. Incorrect or Misleading Naming

### **Misnomer**

*   **Definition:** A name that *incorrectly describes* the thing.
*   **Example:** *“Starfish”* (not a fish)

### **Oxymoron**

*   **Definition:** A phrase with internally contradictory terms.
*   **Example:** *“original copy”*

### **False cognate**

*   **Definition:** Words that look related across languages but aren’t.
*   **Example:** *actual* (EN) vs *actual* “current” (ES)

### **Category error**

*   **Definition:** Treating something as belonging to the wrong conceptual category.
*   **Example:** Asking “What color is democracy?”

***

## 5. Hierarchy & Parent–Child Relationships (✅ what you explicitly asked for)

### **Hypernym (Supertype / Parent)**

*   **Definition:** A **broad category** that subsumes others.
*   **Example:** *Vehicle* → car, bike, truck

### **Hyponym (Subtype / Child)**

*   **Definition:** A **more specific instance** of a category.
*   **Example:** *Car* is a hyponym of *vehicle*

### **Co‑hyponyms (Siblings)**

*   **Definition:** Share the same parent class.
*   **Example:** *Car* and *Truck* under *Vehicle*

### **Is‑a relationship**

*   **Definition:** Formal expression of class membership.
*   **Example:** *A sedan is a car*

### **Part‑whole relationship (Meronymy)**

*   **Meronym:** part → whole (*wheel* → *car*)
*   **Holonym:** whole → part (*car* → *wheel*)

### **Taxonomy**

*   **Definition:** A structured classification system.
*   **Key trait:** Strict parent‑child hierarchy

### **Ontology**

*   **Definition:** A formal semantic model defining:
    *   entities
    *   attributes
    *   relationships
*   **Key trait:** Multiple relationship types, not just hierarchy

***

## 6. Orthogonality & Independence (✅ also explicitly asked)

### **Orthogonal concepts**

*   **Definition:** Concepts that vary **independently**; knowing one gives no info about the other.
*   **Example:** *Color* vs *Shape*

### **Independent dimensions**

*   **Definition:** Axes that do not constrain each other.
*   **Example:** *Severity* and *Frequency* in metrics

### **Non‑overlapping categories**

*   **Definition:** Mutually exclusive without hierarchy.
*   **Example:** *Physical* vs *Digital* products

### **Cross‑cutting concern**

*   **Definition:** A concept that applies across hierarchies.
*   **Example:** *Security* across all system components

***

## 7. Ambiguity, Drift, and Semantic Instability

### **Ambiguous term**

*   **Definition:** Can be interpreted in more than one valid way.
*   **Example:** *metric*

### **Overloaded term**

*   **Definition:** Used with different meanings in different contexts.
*   **Example:** *pipeline* (data vs DevOps)

### **Semantic drift**

*   **Definition:** Meaning changes over time.
*   **Example:** *awesome* (inspiring fear → positive)

### **Folk taxonomy**

*   **Definition:** Informal or culturally derived classification.
*   **Example:** “Vegetable” vs botanical definition

***

## 8. Precision & Naming Quality (Very useful for data/ontology work)

### **Canonical term**

*   **Definition:** The authoritative or preferred label.
*   **Example:** Chosen standard metric name

### **Alias**

*   **Definition:** Alternative name pointing to the same concept.
*   **Example:** *CustID* as alias of *CustomerKey*

### **Disambiguation**

*   **Definition:** Clarifying which meaning is intended.
*   **Example:** *Date (calendar)* vs *Date (social)*

### **Granularity**

*   **Definition:** Level of detail in classification.
*   **Example:** *Revenue* vs *Revenue by SKU*

