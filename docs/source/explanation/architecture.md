# Architecture

Understanding the architecture of Django CMS Taxonomy.

## Core Components

Django CMS Taxonomy consists of three main components:

### 1. Models Layer

**Category Model**: The hierarchical category system
- Stores category metadata (name, slug, description)
- Manages parent-child relationships
- Supports multilingual fields via django-parler
- Uses CTE queries for efficient tree traversal

**CategoryRelation Model**: Generic many-to-many relationships
- Links categories to any Django model
- Stores ordering information
- Uses ContentType framework for flexibility
- Allows one category to be associated with any model

### 2. Mixin Layer

Three mixins provide reusable functionality:

**CategoryMixin**: Model Integration
- Adds `categories` property to any Django model
- Uses `CategoryRelation` to query related categories
- Transparent integration without database schema changes

**CategoryFormMixin**: Form Integration
- Adds categories field to model forms
- Manages category selection widget
- Saves relations via `save_m2m()` method
- Populates initial values from existing relations

**CategoryAdminMixin**: Admin Integration
- Extends Django admin with category support
- Provides fieldset management
- Uses `save_related()` for category persistence
- Integrates with Django admin's form system

### 3. Admin Layer

**CategoryAdmin**: Built-in admin for categories
- Hierarchical display with indentation
- CTE-based efficient tree traversal
- Multilingual support
- Search and filtering

## Data Flow

### Creating an Object with Categories

```
1. Admin form rendered
   └─ CategoryAdminMixin.get_form()
      └─ CategoryFormMixin added to form
         └─ categories field with FilteredSelectMultiple

2. User selects categories and saves

3. Form validation
   └─ cleaned_data includes selected categories

4. Model instance saved
   └─ ModelAdmin.save_model()

5. Relations saved
   └─ CategoryAdminMixin.save_related()
      └─ CategoryFormMixin.save_m2m()
         └─ CategoryRelation objects bulk_created
```

### Accessing Categories

```
post = BlogPost.objects.get(id=1)
   ↓
post.categories  (CategoryMixin.categories property)
   ↓
Query CategoryRelation for this object
   ↓
Return Category objects
   ↓
Use them in views/templates
```

## Design Principles

### 1. **Flexibility**

Use generic foreign keys (ContentType + object_id) instead of model-specific foreign keys:
- Single Category model works with any Django model
- No need to create separate relation models
- Supports polymorphic relationships

### 2. **Performance**

Use Common Table Expressions for hierarchical queries:
- Efficient tree traversal (single CTE query)
- Avoid N+1 problems with bulk operations
- Prefetch support for optimal performance

### 3. **Multilingual**

Leverage django-parler for translations:
- Support multiple languages out of the box
- Separate translation tables for each language
- Fallback mechanisms built-in

### 4. **Integration**

Provide reusable mixins instead of forcing inheritance:
- Works with existing model hierarchies
- Minimal schema changes
- Compatible with other packages

### 5. **Usability**

Provide sensible defaults in admin:
- Collapsed category fieldset (cleaner UI)
- FilteredSelectMultiple widget (better UX)
- Automatic bulk operations
- Automatic relation management

## Technology Stack

### Core Dependencies

- **Django**: Web framework
- **django-parler**: Multilingual support
- **django-cte**: Common Table Expressions

### Admin Features

- **Django Admin**: Admin interface
- **FilteredSelectMultiple**: Many-to-many widget
- **ContentType Framework**: Generic relations

## Database Schema

### Category Table

```sql
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    parent_id INTEGER REFERENCES category(id) NULL,
    slug VARCHAR(255) UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Translations (via parler)
CREATE TABLE category_translation (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES category(id),
    language_code VARCHAR(10),
    name VARCHAR(255),
    description TEXT
);
```

### CategoryRelation Table

```sql
CREATE TABLE categoryrelation (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES category(id),
    content_type_id INTEGER REFERENCES contenttypes(id),
    object_id INTEGER,
    order INTEGER,
    created_at TIMESTAMP
);
```

## Query Optimization

### CTE for Tree Queries

```sql
WITH RECURSIVE tree AS (
    SELECT id, parent_id, depth FROM category WHERE parent_id IS NULL
    UNION ALL
    SELECT c.id, c.parent_id, t.depth + 1
    FROM category c
    INNER JOIN tree t ON c.parent_id = t.id
)
SELECT * FROM tree;
```

This single query efficiently retrieves entire category hierarchy.

### Bulk Operations

CategoryRelation objects are created in batch:
- Single INSERT statement for all relations
- No N query loops
- Efficient database usage
