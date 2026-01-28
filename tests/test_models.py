import pytest
from django.test import TestCase

from djangocms_taxonomy.models import Category, CategoryRelation
from tests.test_app.models import TestModel


class CategoryModelTests(TestCase):
    """Test cases for the Category model."""

    def setUp(self):
        """Set up test data."""
        self.root_category = Category.objects.create(slug="root-category")
        self.root_category.set_current_language("en")
        self.root_category.name = "Root Category"
        self.root_category.description = "A root category"
        self.root_category.save()

        self.child_category = Category.objects.create(
            slug="child-category",
            parent=self.root_category,
        )
        self.child_category.set_current_language("en")
        self.child_category.name = "Child Category"
        self.child_category.description = "A child category"
        self.child_category.save()

        self.grandchild_category = Category.objects.create(
            slug="grandchild-category",
            parent=self.child_category,
        )
        self.grandchild_category.set_current_language("en")
        self.grandchild_category.name = "Grandchild Category"
        self.grandchild_category.description = "A grandchild category"
        self.grandchild_category.save()

    def test_category_creation(self):
        """Test that a category can be created."""
        self.assertEqual(self.root_category.name, "Root Category")
        self.assertEqual(self.root_category.slug, "root-category")
        self.assertIsNone(self.root_category.parent)

    def test_category_hierarchy(self):
        """Test parent-child relationships."""
        self.assertEqual(self.child_category.parent, self.root_category)
        self.assertEqual(self.grandchild_category.parent, self.child_category)

    def test_auto_slug_generation(self):
        """Test that slugs are auto-generated from names."""
        category = Category()
        category.set_current_language("en")
        category.name = "Test Category Name"
        category.description = "Test"
        category.save()

        self.assertEqual(category.slug, "test-category-name")

    def test_get_children(self):
        """Test retrieving child categories."""
        children = self.root_category.children.all()
        self.assertEqual(children.count(), 1)
        self.assertIn(self.child_category, children)

    def test_root_categories_queryset(self):
        """Test filtering root categories."""
        root_cats = Category.objects.roots()
        self.assertEqual(root_cats.count(), 1)
        self.assertIn(self.root_category, root_cats)

    def test_leaf_categories_queryset(self):
        """Test filtering leaf categories."""
        leaf_cats = Category.objects.leaves()
        self.assertEqual(leaf_cats.count(), 1)
        self.assertIn(self.grandchild_category, leaf_cats)

    def test_category_str(self):
        """Test string representation."""
        self.assertEqual(str(self.root_category), "Root Category")

    def test_generic_m2m_relation(self):
        """Test generic many-to-many relationship via CategoryRelation."""
        test_model = TestModel.objects.create(
            title="Test Model",
            description="Test",
        )

        # Create relation
        relation = CategoryRelation.objects.create(
            category=self.root_category,
            content_object=test_model,
        )

        self.assertEqual(relation.content_object, test_model)
        self.assertEqual(relation.category, self.root_category)


@pytest.mark.django_db
class TestCategoryPytest:
    """Pytest-style tests for Category model."""

    def test_category_creation_pytest(self):
        """Test category creation with pytest."""
        category = Category.objects.create(slug="test-category")
        category.set_current_language("en")
        category.name = "Test Category"
        category.save()

        assert category.name == "Test Category"
        assert category.slug == "test-category"

    def test_multiple_categories_pytest(self):
        """Test creating multiple categories."""
        parent = Category.objects.create(slug="parent")
        parent.set_current_language("en")
        parent.name = "Parent"
        parent.save()

        child = Category.objects.create(slug="child", parent=parent)
        child.set_current_language("en")
        child.name = "Child"
        child.save()

        assert Category.objects.count() == 2
        assert child.parent == parent

    def test_translations(self):
        """Test multilingual translations."""
        category = Category.objects.create(slug="test")

        # English translation
        category.set_current_language("en")
        category.name = "Test"
        category.description = "English description"
        category.save()

        # German translation
        category.set_current_language("de")
        category.name = "Prüfung"
        category.description = "Deutsche Beschreibung"
        category.save()

        # Verify both translations exist
        category.set_current_language("en")
        assert category.name == "Test"
        assert category.description == "English description"

        category.set_current_language("de")
        assert category.name == "Prüfung"
        assert category.description == "Deutsche Beschreibung"

        # Slug remains the same across languages
        assert category.slug == "test"
