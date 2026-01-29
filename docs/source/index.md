# Django CMS Taxonomy Documentation

```{toctree}
:maxdepth: 2
:hidden:

tutorials/index
how-to/index
reference/index
explanation/index
```

Django CMS Taxonomy provides a flexible, hierarchical category system for Django models using Common Table Expressions (CTEs) for efficient tree queries and multilingual support via django-parler.

## Documentation Structure

This documentation follows the [Diátaxis](https://diataxis.fr/) framework, organizing information into four sections:

- **[Tutorials](tutorials/index)**: Learning-oriented guides to get started with Django CMS Taxonomy
- **[How-to Guides](how-to/index)**: Problem-solving guides for specific tasks
- **[Reference](reference/index)**: Technical reference documentation
- **[Explanation](explanation/index)**: Conceptual explanations and architecture

## Quick Start

Get up and running with Django CMS Taxonomy in minutes:

```bash
pip install djangocms-taxonomy
```

Add to your Django settings:

```python
INSTALLED_APPS = [
    # ...
    "djangocms_taxonomy",
]
```

Then check out the [Getting Started Tutorial](tutorials/getting-started.md).

## Key Features

- **Hierarchical Categories**: Build multi-level category trees with parent-child relationships
- **CTE Optimization**: Efficient recursive queries using Common Table Expressions
- **Multilingual Support**: Full translation support for category names and descriptions via django-parler
- **Generic Relations**: Associate categories with any Django model
- **Admin Integration**: Beautiful Django admin interface with collapsible fieldsets
- **Reusable Mixins**: Model, form, and admin mixins for easy integration
