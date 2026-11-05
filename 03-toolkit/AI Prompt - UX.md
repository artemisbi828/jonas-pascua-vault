- dropdown forms should be fuzzy search on strings
- draw.io


### The Design Brief

### 1. Core Principles
- **Mobile-First**: Styles default to mobile; use `min-width` media queries for expansion.
- **Semantic HTML**: `<header>`, `<main>`, `<article>`, `<footer>` (No "div soup").
- **Accessibility**: Interactive elements must have `aria-label` or visible text.

### 2. Implementation Rules
| Context | Standard |
| :--- | :--- |
| **HTML** | Use ID for JS hooks (`#js-submit`), Classes for styling (`.btn-primary`). <!-- Separation of concerns: styling vs behavior --> |
| **CSS** | **Vanilla**: Use CSS Variables (`--primary-color`). **Tailwind**: Utility-first, avoid `@apply` abuse. |
| **JS** | **Event Delegation**: Attach listeners to containers, not individual items (`list.addEventListener`). |
| **State** | Minimize DOM reads. Source of truth = JS Object/State, then render to DOM. |


---
#status/deferred/quick-paste-merge-later 
**Project:** Brand Identity Package for "slideSMS"
**Base Asset:** Selected top-left gradient logo (abstract 'S' ribbon forming a speech bubble).

**Objectives:**
Develop a cohesive brand package based on the selected master logo that communicates a modern, user-friendly, and trustworthy messaging tool.

**Requirements:**

1.  **Logo System:** Define the master logo and necessary complementary variations (e.g., single-color, reverse, horizontal lockup) for various contexts.
2.  **Color Palette:** Extract the top 3 core colors (primary, secondary, tertiary) from the logo's gradient. The primary color should be highly marketable and suitable for calls-to-action (leaning towards orange as requested).
3.  **Typography:** Select a modern, highly legible font family suited for a text-messaging interface.
4.  **Brand Voice Rules:** Define the conversational tone and strictly enforce sentence case for all written materials.
5.  **Technical Specs:** Provide a CSS stylesheet snippet and a JSON object for color integration.
6.  **Asset Checklist:** List the required PNG dimensions for a standard web application deployment.
7.  **Resources:** Recommend affordable stock photography websites to support future marketing.

-----

Here is your complete brand package based on that brief.

# slideSMS Brand Package - Premium Edition

## 1. Brand Voice & Typography Guidelines

We want slideSMS to feel like a helpful partner, not a faceless corporation.

**The Tone:** Conversational, direct, and friendly. We don't use jargon. We speak simply.

**The Golden Rule of Text: Sentence case.**
We use sentence case everywhere—in headlines, buttons, and body text. This means we only capitalize the first letter of a sentence or proper nouns. It looks cleaner, more modern, and is easier to read quickly in an app interface.

  * **Yes:** Send a message
  * *No:* Send A Message
  * **Yes:** Sign up for free today
  * *No:* SIGN UP FOR FREE TODAY

**The Font Family: Inter**
For a text messaging app, legibility is everything. We choose **Inter**. It is designed specifically for computer screens. It's tall, readable, neutral, and very modern.

  * *Usage:* Use Inter Regular (400 weight) for body text and messages. Use Inter SemiBold (600 weight) for headlines and buttons.

---

## 2. Color Palette - Refined

### Primary Colors

**Primary Gradient** (for CTAs and accents):
```css
--color-primary-gradient: linear-gradient(135deg, #FF8A5B 0%, #FF6B9D 100%);
```
- Softer, more sophisticated than solid orange
- Use for buttons, highlights, important elements

**Secondary Blue**:
```css
--color-secondary-blue: #4E3FF3;
```
- Deep, trustworthy
- Use for headers, navigation, links

**Accent Colors**:
```css
--color-accent-cyan: #00D4FF;      /* Bright, energetic highlights */
--color-accent-purple: #9D4EDD;    /* Depth, sophistication */
--color-accent-pink: #FF6B9D;      /* Warmth, connection */
```

### Neutral Palette
```css
--color-bg-dark: #0A0A0F;          /* Rich black backgrounds */
--color-bg-medium: #1A1A2E;        /* Card backgrounds */
--color-bg-light: #F4F6F9;         /* Light mode sections */
--color-text-dark: #1A1A2E;        /* Main text on light backgrounds */
--color-text-medium: #5A5A75;      /* Secondary text */
--color-text-light: #A8A8B8;       /* Subtle text */
--color-white: #FFFFFF;
```

### CSS Stylesheet Snippet

Here are your variables ready to drop into your main CSS file.

```css
/* Import Inter font from Google Fonts - MUST be first */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

:root {
  /* Primary Gradient (softer than solid orange) */
  --color-primary-start: #FF8A5B;
  --color-primary-end: #FF6B9D;
  
  /* Secondary & Accents */
  --color-secondary-blue: #4E3FF3;
  --color-accent-cyan: #00D4FF;
  --color-accent-purple: #9D4EDD;
  --color-accent-pink: #FF6B9D;
  
  /* Backgrounds */
  --color-bg-dark: #0A0A0F;
  --color-bg-medium: #1A1A2E;
  --color-bg-light: #F4F6F9;
  
  /* Text */
  --color-text-dark: #1A1A2E;
  --color-text-medium: #5A5A75;
  --color-text-light: #A8A8B8;
  --color-white: #FFFFFF;
  
  /* Spacing */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 32px;
  --space-lg: 64px;
  --space-xl: 96px;
  --space-2xl: 128px;
  --space-3xl: 192px;
  
  /* Typography */
  --font-family-base: 'Inter', sans-serif;
  --text-xs: 12px;
  --text-sm: 14px;
  --text-base: 16px;
  --text-lg: 20px;
  --text-xl: 28px;
  --text-2xl: 40px;
  --text-3xl: 56px;
  --text-4xl: 72px;
  --text-5xl: 96px;
  
  /* Font Weights */
  --font-regular: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
  
  /* Shadows */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.08);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.12);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.16);
  --shadow-glow: 0 0 40px rgba(255, 107, 157, 0.3);
  
  /* Container Widths */
  --container-narrow: 800px;
  --container-medium: 1200px;
  --container-wide: 1400px;
}

body {
  font-family: var(--font-family-base);
  color: var(--color-text-dark);
  background-color: var(--color-white);
  text-transform: none; 
}

/* Example Button */
.btn-primary {
  background: linear-gradient(135deg, var(--color-primary-start) 0%, var(--color-primary-end) 100%);
  color: var(--color-white);
  font-weight: 600;
  text-transform: none; 
}
```

---

## 3. Layout & Spacing

### Container Widths
```css
--container-narrow: 800px;    /* Text-heavy sections */
--container-medium: 1200px;   /* Standard content */
--container-wide: 1400px;     /* Hero, features */
```

### Spacing Scale
Use generous spacing between sections for a premium feel:
- `--space-xl: 96px` - Between major sections
- `--space-2xl: 128px` - Hero padding
- `--space-3xl: 192px` - Extra large sections

---

## 4. Animation & Dynamic Elements

### Installed Libraries

**Framer Motion** - Scroll animations, text reveals
```bash
npm install framer-motion
```

**Lucide React** - Monochromatic icons
```bash
npm install lucide-react
```

**React Particles** - Floating particle backgrounds
```bash
npm install react-particles tsparticles-slim
```

### Particle Background Configuration

Used in Hero section for floating constellation effect:
- Small blue particles (#4E3FF3)
- Connecting lines (distance: 150px)
- Slow movement (speed: 0.5)
- Fading opacity (0.1 - 0.5)
- Interactive on hover (grab effect)

### Scroll Animations

**Word-by-word reveal:**
```tsx
{words.map((word, i) => (
  <motion.span
    initial={{ opacity: 0, y: 20 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: i * 0.1 }}
  >
    {word}
  </motion.span>
))}
```

**Scroll-triggered fade-in:**
```tsx
<motion.div
  initial={{ opacity: 0, y: 30 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true }}
/>
```

---

## 5. Component Patterns

### Hero Section
- Full viewport height (`min-height: 100vh`)
- Particle background (floating constellation)
- Large headline (72px desktop, 56px mobile)
- Gradient CTA button with glow effect
- Logo display (80px)

### Feature Cards
- **Light background** for readability
- Clean card design with subtle shadows
- Monochrome Lucide icons (blue)
- Scroll-triggered staggered animations
- Hover lift effect

### Email Capture
- Gradient background (blue to cyan)
- Simple single-field form
- Inline button with gradient
- Scroll animations

---

## 6. Logo Usage

**File Location**: `slidesms/public/logo.png`

**Gradient Colors Extracted**:
- Cyan: `#00D4FF`
- Blue: `#4E3FF3`
- Purple: `#9D4EDD`
- Pink: `#FF6B9D`
- Orange: `#FF8A5B`

---

## 7. Design Principles

### Readability First
- **High contrast**: Always ensure text is readable
- **Light backgrounds for text-heavy sections**: White or light gray
- **Dark backgrounds sparingly**: Only for visual breaks, not primary content

### Premium Feel
- **Generous white space**: Don't crowd elements
- **Subtle animations**: Enhance, don't distract
- **Quality over quantity**: Fewer, better-designed sections

### Accessibility
- **Color contrast**: Minimum 4.5:1 ratio (WCAG AA)
- **Focus states**: Visible keyboard navigation
- **Alt text**: Descriptive for all images

---

*Updated: 2025-11-25 - Premium Edition with Particle Effects*

---
# Design Patterns
# Design Patterns & Code Style Guide

> Based on slidesms_v1 preferences and best practices across the Artemis BI ecosystem

## Table of Contents
- [Philosophy](#philosophy)
- [Naming Conventions](#naming-conventions)
- [Error Handling](#error-handling)
- [Data Validation](#data-validation)
- [Type Safety](#type-safety)
- [Documentation](#documentation)

---

## Philosophy

### Core Principles
1. **Clarity over Cleverness**: Code should be immediately understandable
2. **Fail Gracefully**: Always provide fallback values and clear error messages
3. **Type Everything**: Use type hints (Python) or TypeScript for all functions
4. **Test Early, Test Often**: Validate inputs at boundaries
5. **Document Intent**: Comments explain *why*, not *what*

### Design Patterns from slidesms
- **Parser Pattern**: Separate parsing logic from business logic
- **Interface-First**: Define clear interfaces/contracts between modules
- **Centralized Validation**: Single source of truth for validation rules
- **Consistent Returns**: Return structured objects, not raw data

---

## Naming Conventions

### Files & Modules
```
✅ Good
contactParser.ts / contact_parser.py
csvHelpers.ts / csv_helpers.py
htmlScraper.ts / html_scraper.py

❌ Avoid
cp.ts
helper.py
utils.py (too generic)
```

**Pattern**: 
- TypeScript: camelCase for files
- Python: snake_case for files
- Both: Descriptive names that indicate purpose

### Functions & Methods
```typescript
// ✅ TypeScript (slidesms pattern)
static parseName(rawName: string): NameParts
static parsePhone(rawPhone: string, defaultCountry: CountryCode): PhoneParts
static inferColumns(headers: string[]): ColumnMapping
```

```python
# ✅ Python (matching pattern)
def parse_name(raw_name: str) -> NameParts:
def parse_phone(raw_phone: str, default_country: str = 'US') -> PhoneParts:
def infer_columns(headers: List[str]) -> ColumnMapping:
```

**Pattern**: 
- Verb-first naming: `parse`, `validate`, `format`, `extract`
- Clear parameter names: `raw_*` for input, `*_str` for strings
- Return type in name when helpful: `format_for_excel_row()`

### Classes
```typescript
// ✅ TypeScript
export class ContactParser { }
export class JiraScraper extends WebScraper { }
```

```python
# ✅ Python
class ContactParser:
    """Parser for contact information."""
    pass

class JiraScraper(WebScraper):
    """JIRA-specific HTML scraper."""
    pass
```

**Pattern**: PascalCase, descriptive nouns, clear inheritance

### Variables & Constants
```typescript
// ✅ Variables (camelCase)
const phoneNumber = "555-1234";
const parsedContacts = [];
const isValid = true;

// ✅ Constants (UPPER_SNAKE_CASE)
const DEFAULT_COUNTRY = 'US';
const MAX_RETRIES = 3;
```

```python
# ✅ Variables (snake_case)
phone_number = "555-1234"
parsed_contacts = []
is_valid = True

# ✅ Constants (UPPER_SNAKE_CASE)
DEFAULT_COUNTRY = 'US'
MAX_RETRIES = 3
```

---

## Error Handling

### Graceful Degradation (slidesms pattern)
```typescript
// ✅ Return structured fallbacks, not exceptions
static parsePhone(rawPhone: string, defaultCountry: CountryCode = 'US') {
    if (!rawPhone) {
        return {
            phone: null,
            country_code: null,
            phone_formatted: null
        };
    }

    try {
        const phoneNumber = parsePhoneNumber(rawPhone, defaultCountry);
        if (phoneNumber && phoneNumber.isValid()) {
            return {
                phone: phoneNumber.nationalNumber,
                country_code: '+' + phoneNumber.countryCallingCode,
                phone_formatted: phoneNumber.formatInternational()
            };
        }
    } catch (e) {
        // Log but don't throw
    }

    // Fallback: strip non-digits
    const stripped = rawPhone.replace(/\D/g, '');
    return {
        phone: stripped || null,
        country_code: null,
        phone_formatted: null
    };
}
```

```python
# ✅ Python equivalent
def parse_phone(raw_phone: str, default_country: str = 'US') -> PhoneParts:
    """Parse phone number with graceful fallback."""
    if not raw_phone:
        return PhoneParts(
            phone=None,
            country_code=None,
            phone_formatted=None
        )
    
    try:
        # Attempt proper parsing
        phone_number = phonenumbers.parse(raw_phone, default_country)
        if phonenumbers.is_valid_number(phone_number):
            return PhoneParts(
                phone=str(phone_number.national_number),
                country_code=f'+{phone_number.country_code}',
                phone_formatted=phonenumbers.format_number(
                    phone_number, 
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
            )
    except Exception as e:
        # Log but continue
        pass
    
    # Fallback: strip non-digits
    stripped = re.sub(r'\D', '', raw_phone)
    return PhoneParts(
        phone=stripped if stripped else None,
        country_code=None,
        phone_formatted=None
    )
```

### Error Messages
```typescript
// ✅ Clear, actionable errors
throw new Error('Invalid request. Contacts array is required.');
throw new Error('Invalid contact data. Phone is required.');

// ❌ Vague errors
throw new Error('Bad data');
throw new Error('Error');
```

---

## Data Validation

### Input Validation Pattern (slidesms)
```typescript
// ✅ Validate at boundaries
export const parseCSV = (file: File): Promise<ParseResult> => {
    return new Promise((resolve, reject) => {
        Papa.parse(file, {
            header: true,
            skipEmptyLines: true,
            complete: (results) => {
                const validContacts: Contact[] = [];
                const invalidRows: any[] = [];
                const seenPhones = new Set<string>();
                let duplicates = 0;

                data.forEach((row) => {
                    const parsed = ContactParser.parse(row);
                    
                    // Validation: Must have at least a valid phone
                    if (parsed.phone) {
                        if (seenPhones.has(parsed.phone)) {
                            duplicates++;
                        } else {
                            seenPhones.add(parsed.phone);
                            validContacts.push(parsed);
                        }
                    } else {
                        invalidRows.push(row);
                    }
                });

                resolve({
                    valid: validContacts,
                    invalid: invalidRows,
                    duplicates,
                    total: data.length
                });
            }
        });
    });
};
```

**Key Principles:**
1. Separate valid from invalid data
2. Track duplicates explicitly
3. Return structured results with counts
4. Never silently discard data

---

## Type Safety

### TypeScript (slidesms)
```typescript
export interface ParsedContact {
    firstname: string | null;
    lastname: string | null;
    alias: string | null;
    title: string | null;
    suffix: string | null;
    phone: string | null;
    country_code: string | null;
    phone_formatted: string | null;
    email: string | null;
    domain: string | null;
    original: any;
}

export interface ParseResult {
    valid: Contact[];
    invalid: any[];
    duplicates: number;
    total: number;
}
```

### Python (matching pattern)
```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any

@dataclass
class ParsedContact:
    """Parsed contact information."""
    firstname: Optional[str] = None
    lastname: Optional[str] = None
    alias: Optional[str] = None
    title: Optional[str] = None
    suffix: Optional[str] = None
    phone: Optional[str] = None
    country_code: Optional[str] = None
    phone_formatted: Optional[str] = None
    email: Optional[str] = None
    domain: Optional[str] = None
    original: Optional[Dict[str, Any]] = None

@dataclass
class ParseResult:
    """CSV parsing result with validation stats."""
    valid: List[ParsedContact]
    invalid: List[Dict[str, Any]]
    duplicates: int
    total: int
```

---

## Documentation

### Module-Level Docstrings
```python
"""
Contact parser utilities.

Provides functions to parse and validate contact information from various
input formats (CSV, raw text, JSON). Handles name parsing, phone number
validation, and email extraction with graceful fallbacks.

Example:
    >>> from shared_utils.utils.contact_parser import ContactParser
    >>> result = ContactParser.parse_name("Dr. John Smith Jr.")
    >>> print(result.firstname)
    'John'
"""
```

### Function Docstrings (Google Style)
```python
def parse_phone(raw_phone: str, default_country: str = 'US') -> PhoneParts:
    """
    Parse and validate phone number with international formatting.
    
    Attempts to parse the phone number using libphonenumber. If parsing fails,
    falls back to stripping non-digit characters. Never raises exceptions.
    
    Args:
        raw_phone: Raw phone number string (any format)
        default_country: ISO country code for parsing (default: 'US')
    
    Returns:
        PhoneParts object with phone, country_code, and formatted fields.
        Fields will be None if parsing fails completely.
    
    Example:
        >>> parse_phone("(555) 123-4567")
        PhoneParts(phone='5551234567', country_code='+1', 
                   phone_formatted='+1 555-123-4567')
        
        >>> parse_phone("invalid")
        PhoneParts(phone=None, country_code=None, phone_formatted=None)
    """
```

---

## Summary

**From slidesms we prioritize:**
1. ✅ Clear naming that reveals intent
2. ✅ Structured return types with null safety
3. ✅ Graceful error handling with fallbacks
4. ✅ Validation at boundaries
5. ✅ Strong typing with interfaces/dataclasses
6. ✅ Comprehensive documentation

**Apply these patterns to all new code in shared-utils and client projects.**

