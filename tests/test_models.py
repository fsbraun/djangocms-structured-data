import pytest
from django.test import TestCase

from djangocms_taxonomy.models import Category
from tests.test_app.models import TestModel


class CategoryModelTests(TestCase):
    """Test cases for the Category model."""
    
    def setUp(self):
        """Set up test data."""
        self.root_category = Category.objects.create(
            name="Root Category",
            slug="root-category",
            description="A root category",
        )
        
        self.child_category = Category.objects.create(
            name="Child Category",
            slug="child-category",
            parent=self.root_category,
            description="A child category",
        )
        
        self.grandchild_category = Category.objects.create(
            name="Grandchild Category",
            slug="grandchild-category",
            parent=self.child_category,
            description="A grandchild category",
        )
    
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
        category = Category.objects.create(
            name="Test Category Name",
            description="Test",
        )
        self.assertEqual(category.slug, "test-category-name")
    
    def test_get_children(self):
        """Test retrieving child categories."""
        children = self.root_category.children.all()
        self.assertEqual(children.count(), 1)
        self.assertIn(self.child_category, children)
    
    def test_get_descendants_optimized(self):
        """Test optimized descendant retrieval with CTE."""
        descendants = self.root_category.get_descendants()
        self.assertEqual(descendants.count(), 2)
        self.assertIn(self.child_category, descendants)
        self.assertIn(self.grandchild_category, descendants)
    
    def test_get_ancestors_optimized(self):
        """Test optimized ancestor retrieval with CTE."""
        ancestors = self.grandchild_category.get_ancestors()
        self.assertEqual(ancestors.count(), 2)
        self.assertIn(self.root_category, ancestors)
        self.assertIn(self.child_category, ancestors)
    
    def test_root_categories_queryset(self):
        """Test filtering root categories."""
        root_cats = Category.objects.root_categories()
        self.assertEqual(root_cats.count(), 1)
        self.assertIn(self.root_category, root_cats)
    
    def test_leaf_categories_queryset(self):
        """Test filtering leaf categories."""
        leaf_cats = Category.objects.leaf_categories()
        self.assertEqual(leaf_cats.count(), 1)
        self.assertIn(self.grandchild_category, leaf_cats)
    
    def test_category_str(self):
        """Test string representation."""
        self.assertEqual(str(self.root_category), "Root Category")
    
    def test_generic_foreign_key(self):
        """Test generic foreign key attachment."""
        test_model = TestModel.objects.create(
            title="Test Model",
            description="Test",
        )
        
        category = Category.objects.create(
            name="Attached Category",
            slug="attached-category",
            content_type_id=self.get_content_type_id(TestModel),
            object_id=test_model.id,
        )
        
        self.assertEqual(category.content_object, test_model)
    
    @staticmethod
    def get_content_type_id(model):
        """Helper to get content type ID for a model."""
        from django.contrib.contenttypes.models import ContentType
        return ContentType.objects.get_for_model(model).id


@pytest.mark.django_db
class TestCategoryPytest:
    """Pytest-style tests for Category model."""
    
    def test_category_creation_pytest(self):
        """Test category creation with pytest."""
        category = Category.objects.create(
            name="Test Category",
            slug="test-category",
        )
        assert category.name == "Test Category"
        assert category.slug == "test-category"
    
    def test_multiple_categories_pytest(self):
        """Test creating multiple categories."""
        parent = Category.objects.create(
            name="Parent",
            slug="parent",
        )
        child = Category.objects.create(
            name="Child",
            slug="child",
            parent=parent,
        )
        
        assert Category.objects.count() == 2
        assert child.parent == parent
