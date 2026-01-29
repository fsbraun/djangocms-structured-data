# Models API

Reference documentation for Django CMS Taxonomy models.

## Category

The main Category model for managing hierarchical categories.

```{autoclass} djangocms_taxonomy.models.Category
:members:
:undoc-members:
```

### Fields

- **id** (`AutoField`): Primary key
- **parent** (`ForeignKey`): Reference to parent category (null for root categories)
- **slug** (`SlugField`): URL-friendly slug, auto-generated from name
- **name** (`TranslatedField`): Multilingual category name
- **description** (`TranslatedField`): Multilingual category description
- **created_at** (`DateTimeField`): Creation timestamp
- **updated_at** (`DateTimeField`): Last update timestamp

### Methods

See {doc}`../reference/models` for the complete model API.

## CategoryRelation

Intermediary model for generic many-to-many relationships between categories and other models.

```{autoclass} djangocms_taxonomy.models.CategoryRelation
:members:
:undoc-members:
```

### Fields

- **category** (`ForeignKey`): Reference to Category
- **content_type** (`ForeignKey`): ContentType of related model
- **object_id** (`PositiveIntegerField`): ID of related object
- **order** (`PositiveIntegerField`): Order of category (for sorting)
- **created_at** (`DateTimeField`): Creation timestamp

## CategoryQuerySet

Custom QuerySet with tree traversal methods.

```{autoclass} djangocms_taxonomy.models.CategoryQuerySet
:members:
:undoc-members:
```

### Methods

- **with_tree_fields()**: Annotate queryset with CTE tree fields (depth, path)
- **roots()**: Get only root categories (those without parents)
- **leaves()**: Get only leaf categories (those without children)
