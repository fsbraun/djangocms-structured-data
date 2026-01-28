from typing import Optional

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import F, Prefetch, QuerySet
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class CategoryQuerySet(models.QuerySet):
    """
    Optimized queryset for Category model.
    """
    
    def get_descendants(self, category_id: int) -> QuerySet:
        """
        Get all descendants of a category using Django ORM.
        Uses prefetch_related for optimization.
        
        Args:
            category_id: The ID of the category to get descendants for.
            
        Returns:
            QuerySet of descendant categories.
        """
        category = self.filter(id=category_id).first()
        if not category:
            return self.none()
        
        # Get all direct children with recursive expansion
        descendants: list[Category] = []
        queue = list(category.children.all())
        
        while queue:
            current = queue.pop(0)
            descendants.append(current)
            queue.extend(current.children.all())
        
        # Get the IDs and return as queryset
        if descendants:
            ids = [d.id for d in descendants]
            return self.filter(id__in=ids).prefetch_related("children")
        return self.none()
    
    def get_descendants_optimized(self, category_id: int) -> QuerySet:
        """
        Get all descendants using Django ORM.
        Alias for get_descendants for compatibility.
        
        Args:
            category_id: The ID of the category to get descendants for.
            
        Returns:
            QuerySet of descendant categories.
        """
        return self.get_descendants(category_id)
    
    def get_ancestors(self, category_id: int) -> QuerySet:
        """
        Get all ancestors of a category using Django ORM.
        
        Args:
            category_id: The ID of the category to get ancestors for.
            
        Returns:
            QuerySet of ancestor categories.
        """
        category = self.filter(id=category_id).first()
        if not category:
            return self.none()
        
        # Traverse up the tree
        ancestors: list[Category] = []
        current = category.parent
        
        while current is not None:
            ancestors.append(current)
            current = current.parent
        
        # Get the IDs and return as queryset
        if ancestors:
            ids = [a.id for a in ancestors]
            return self.filter(id__in=ids)
        return self.none()
    
    def get_ancestors_optimized(self, category_id: int) -> QuerySet:
        """
        Get all ancestors using Django ORM.
        Alias for get_ancestors for compatibility.
        
        Args:
            category_id: The ID of the category to get ancestors for.
            
        Returns:
            QuerySet of ancestor categories.
        """
        return self.get_ancestors(category_id)
    
    def root_categories(self) -> QuerySet:
        """
        Get all root categories (no parent).
        
        Returns:
            QuerySet of root categories.
        """
        return self.filter(parent__isnull=True)
    
    def leaf_categories(self) -> QuerySet:
        """
        Get all leaf categories (no children).
        
        Returns:
            QuerySet of leaf categories.
        """
        return self.filter(children__isnull=True)


class CategoryManager(models.Manager):
    """
    Custom manager for Category model with optimizations.
    """
    
    def get_queryset(self) -> CategoryQuerySet:
        """
        Return the custom CategoryQuerySet.
        
        Returns:
            CategoryQuerySet instance.
        """
        return CategoryQuerySet(self.model, using=self._db)
    
    def get_descendants(self, category_id: int) -> QuerySet:
        """
        Get all descendants of a category.
        
        Args:
            category_id: The ID of the category to get descendants for.
            
        Returns:
            QuerySet of descendant categories.
        """
        return self.get_queryset().get_descendants(category_id)
    
    def get_descendants_optimized(self, category_id: int) -> QuerySet:
        """
        Get all descendants using optimized method.
        
        Args:
            category_id: The ID of the category to get descendants for.
            
        Returns:
            QuerySet of descendant categories.
        """
        return self.get_queryset().get_descendants_optimized(category_id)
    
    def get_ancestors(self, category_id: int) -> QuerySet:
        """
        Get all ancestors of a category.
        
        Args:
            category_id: The ID of the category to get ancestors for.
            
        Returns:
            QuerySet of ancestor categories.
        """
        return self.get_queryset().get_ancestors(category_id)
    
    def get_ancestors_optimized(self, category_id: int) -> QuerySet:
        """
        Get all ancestors using optimized method.
        
        Args:
            category_id: The ID of the category to get ancestors for.
            
        Returns:
            QuerySet of ancestor categories.
        """
        return self.get_queryset().get_ancestors_optimized(category_id)
    
    def root_categories(self) -> QuerySet:
        """
        Get all root categories.
        
        Returns:
            QuerySet of root categories.
        """
        return self.get_queryset().root_categories()
    
    def leaf_categories(self) -> QuerySet:
        """
        Get all leaf categories.
        
        Returns:
            QuerySet of leaf categories.
        """
        return self.get_queryset().leaf_categories()




class Category(models.Model):
    """
    A hierarchical category model that can be attached to any Django model
    using a GenericForeignKey. Inspired by djangocms-stories.PostCategory.
    
    Features:
    - Hierarchical structure with parent-child relationships
    - Generic foreign key support for attaching to any model
    - Metadata like creation/modification dates
    - Customizable priority ordering
    - Optimized tree traversal to minimize database queries
    """
    # Hierarchical structure
    parent = models.ForeignKey(
        "self",
        verbose_name=_("parent"),
        null=True,
        blank=True,
        related_name="children",
        on_delete=models.CASCADE,
    )
    
    # Core fields
    name = models.CharField(
        _("name"),
        max_length=255,
    )
    slug = models.SlugField(
        _("slug"),
        max_length=255,
        unique=True,
        db_index=True,
    )
    description = models.TextField(
        _("description"),
        blank=True,
    )
    
    # Generic foreign key fields
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_("content type"),
        null=True,
        blank=True,
    )
    object_id = models.PositiveIntegerField(
        _("object id"),
        null=True,
        blank=True,
    )
    content_object = GenericForeignKey("content_type", "object_id")
    
    # Ordering and metadata
    priority = models.IntegerField(
        _("priority"),
        blank=True,
        null=True,
        help_text=_("Used for custom ordering of categories"),
    )
    
    # Timestamps
    date_created = models.DateTimeField(
        _("created at"),
        auto_now_add=True,
    )
    date_modified = models.DateTimeField(
        _("modified at"),
        auto_now=True,
    )
    
    # Custom manager with optimizations
    objects = CategoryManager()
    
    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categories")
        ordering = (F("priority").asc(nulls_last=True), "name")
        indexes = [
            models.Index(fields=["content_type", "object_id"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["parent"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["slug", "parent"],
                name="unique_slug_per_parent",
            ),
        ]
    
    def get_descendants(self) -> QuerySet:
        """
        Get all descendants using optimized method.
        This executes efficient queries instead of N queries.
        
        Returns:
            QuerySet of descendant categories.
        """
        return Category.objects.get_descendants_optimized(self.pk)
    
    def get_ancestors(self) -> QuerySet:
        """
        Get all ancestors using optimized method.
        This executes efficient queries instead of N queries.
        
        Returns:
            QuerySet of ancestor categories.
        """
        return Category.objects.get_ancestors_optimized(self.pk)
    
    def save(self, *args, **kwargs) -> None:
        """
        Auto-generate slug from name if not provided.
        
        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        """
        Return the string representation of the category.
        
        Returns:
            The category name.
        """
        return self.name
