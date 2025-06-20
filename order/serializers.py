from rest_framework import serializers
from order.models import Cart, CartItem, Order, OrderItem
from pet.models import Pet
from pet.serializers import PetImageSerializer
from order.services import OrderService


class EmptySerializer(serializers.Serializer):
    pass


class SimplePetSerializer(serializers.ModelSerializer):
    images = PetImageSerializer(many=True, read_only=True) 
    class Meta:
        model = Pet
        fields = ['id', 'name', 'cost','images']


class AddCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['id', 'pet_id']

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        pet_id = self.validated_data['pet_id']

        # Check if the pet is already in the cart
        if CartItem.objects.filter(cart_id=cart_id, pet_id=pet_id).exists():
            raise serializers.ValidationError("This pet is already in your cart.")

        # Create new cart item
        self.instance = CartItem.objects.create(cart_id=cart_id, pet_id=pet_id)
        return self.instance

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError(
                f"Pet with id {value} does not exists")
        return value

class UpdateCartItemSerializer(serializers.ModelSerializer):
    pet_id = serializers.IntegerField()

    class Meta:
        model = CartItem
        fields = ['pet_id']

    def validate_pet_id(self, value):
        if not Pet.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Pet does not exist.")
        return value


class CartItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = CartItem
        fields = ['id', 'pet', 'total_price']

    def get_total_price(self, cart_item: CartItem):
        return cart_item.pet.cost


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['id', 'user', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart: Cart):
        return sum([item.pet.cost for item in cart.items.all()])

class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No cart found with this id')

        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError('Cart is empty')

        return cart_id

    def create(self, validated_data):
        user_id = self.context['user_id']
        cart_id = validated_data['cart_id']

        try:
            order = OrderService.create_order(user_id=user_id, cart_id=cart_id)
            return order
        except ValueError as e:
            raise serializers.ValidationError(str(e))

    def to_representation(self, instance):
        return OrderSerializer(instance).data


class OrderItemSerializer(serializers.ModelSerializer):
    pet = SimplePetSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'pet', 'price', 'total_price']


class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']