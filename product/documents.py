from django_elasticsearch_dsl import Document, Index, fields
from django_elasticsearch_dsl.registries import registry
from product.models import Product

# Define an index
product_index = Index('products')

# Configure how the index should be created
product_index.settings(
    number_of_shards=1,
    number_of_replicas=0
)

@product_index.doc_type
class ProductDocument(Document):
    class Django:
        model = Product
        fields = [
            'title',
            'description',
            'price',
            'image',
        ]
