from rest_framework import serializers
from .models import *


class AllProductSerializer(serializers.ModelSerializer):
	class Meta:
		model = Allproduct
		fields = ('id', 'catagoryname', 'name', 'price',
				  'detail', 'instock', 'quantity', 'image')
