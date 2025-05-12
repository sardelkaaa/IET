from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView

@extend_schema(exclude=True)
class HiddenSchemaView(SpectacularAPIView):
    pass
